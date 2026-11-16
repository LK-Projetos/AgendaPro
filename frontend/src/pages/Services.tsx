import { useState, type FormEvent } from 'react'
import { api, ApiError } from '../api'
import { Empty, ErrorBox, Field, Loading, Modal, useToast } from '../components'
import { brl } from '../format'
import { errText, useLoad } from '../hooks'
import type { Service, ServiceInput } from '../types'

type Form = { name: string; description: string; duration_minutes: string; price: string }

function validate(f: Form) {
  const e: Record<string, string> = {}
  if (f.name.trim().length < 2) e.name = 'Informe o nome (mínimo 2 caracteres).'
  const d = Number(f.duration_minutes)
  if (!Number.isInteger(d) || d < 15 || d > 480 || d % 15) e.duration_minutes = 'Duração: 15 a 480 min, em múltiplos de 15.'
  const p = Number(f.price.replace(',', '.'))
  if (f.price.trim() === '' || Number.isNaN(p) || p < 0) e.price = 'Informe um preço válido (≥ 0).'
  return e
}

export default function Services() {
  const { data, error, loading, reload } = useLoad(api.services.list)
  const [editing, setEditing] = useState<Service | 'new' | null>(null)
  const toast = useToast()

  async function remove(s: Service) {
    if (!confirm(`Excluir o serviço "${s.name}"?`)) return
    try {
      await api.services.remove(s.id)
      toast('ok', 'Serviço excluído.')
      reload()
    } catch (e) {
      toast('err', errText(e))
    }
  }

  return (
    <section>
      <div className="bar">
        <h1>Serviços</h1>
        <button className="primary" onClick={() => setEditing('new')}>
          + Novo serviço
        </button>
      </div>
      {loading && !data ? (
        <Loading />
      ) : error ? (
        <ErrorBox text={error} retry={reload} />
      ) : data && data.length === 0 ? (
        <Empty text="Nenhum serviço cadastrado." />
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Serviço</th>
                <th>Duração</th>
                <th>Preço</th>
                <th aria-label="Ações" />
              </tr>
            </thead>
            <tbody>
              {data?.map((s) => (
                <tr key={s.id}>
                  <td data-label="Serviço">
                    {s.name}
                    {s.description && <small className="muted block">{s.description}</small>}
                  </td>
                  <td data-label="Duração">{s.duration_minutes} min</td>
                  <td data-label="Preço">{brl(s.price)}</td>
                  <td className="actions">
                    <button onClick={() => setEditing(s)}>Editar</button>
                    <button className="danger" onClick={() => remove(s)}>
                      Excluir
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {editing && (
        <ServiceForm
          service={editing === 'new' ? null : editing}
          onClose={() => setEditing(null)}
          onSaved={() => {
            setEditing(null)
            reload()
          }}
        />
      )}
    </section>
  )
}

function ServiceForm({ service, onClose, onSaved }: { service: Service | null; onClose: () => void; onSaved: () => void }) {
  const [f, setF] = useState<Form>({
    name: service?.name ?? '',
    description: service?.description ?? '',
    duration_minutes: String(service?.duration_minutes ?? 30),
    price: service ? String(service.price) : '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [formError, setFormError] = useState('')
  const [saving, setSaving] = useState(false)
  const toast = useToast()

  async function submit(ev: FormEvent) {
    ev.preventDefault()
    const v = validate(f)
    setErrors(v)
    setFormError('')
    if (Object.keys(v).length) return
    const body: ServiceInput = {
      name: f.name,
      description: f.description,
      duration_minutes: Number(f.duration_minutes),
      price: Number(f.price.replace(',', '.')),
    }
    setSaving(true)
    try {
      if (service) await api.services.update(service.id, body)
      else await api.services.create(body)
      toast('ok', service ? 'Serviço atualizado.' : 'Serviço cadastrado.')
      onSaved()
    } catch (e) {
      if (e instanceof ApiError && Object.keys(e.fields).length) setErrors(e.fields)
      else if (e instanceof ApiError && e.code === 'CONFLICT') setErrors({ name: e.message })
      else setFormError(errText(e))
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal title={service ? 'Editar serviço' : 'Novo serviço'} onClose={onClose}>
      <form onSubmit={submit} noValidate>
        <Field label="Nome" error={errors.name}>
          <input value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} autoFocus />
        </Field>
        <Field label="Descrição (opcional)">
          <input value={f.description} onChange={(e) => setF({ ...f, description: e.target.value })} />
        </Field>
        <div className="row">
          <Field label="Duração (min)" error={errors.duration_minutes}>
            <input
              type="number"
              step={15}
              min={15}
              value={f.duration_minutes}
              onChange={(e) => setF({ ...f, duration_minutes: e.target.value })}
            />
          </Field>
          <Field label="Preço (R$)" error={errors.price}>
            <input inputMode="decimal" value={f.price} onChange={(e) => setF({ ...f, price: e.target.value })} />
          </Field>
        </div>
        {formError && <p className="error">{formError}</p>}
        <footer>
          <button type="button" onClick={onClose}>
            Cancelar
          </button>
          <button className="primary" disabled={saving}>
            {saving ? 'Salvando…' : 'Salvar'}
          </button>
        </footer>
      </form>
    </Modal>
  )
}
