import { useState, type FormEvent } from 'react'
import { api, ApiError } from '../api'
import { Empty, ErrorBox, Field, Loading, Modal, useToast } from '../components'
import { phoneMask } from '../format'
import { errText, useLoad } from '../hooks'
import type { Client, ClientInput } from '../types'

const EMPTY: ClientInput = { name: '', email: '', phone: '' }

function validate(f: ClientInput) {
  const e: Record<string, string> = {}
  if (f.name.trim().length < 2) e.name = 'Informe o nome (mínimo 2 caracteres).'
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email.trim())) e.email = 'E-mail inválido.'
  const d = f.phone.replace(/\D/g, '')
  if (d.length < 10 || d.length > 11) e.phone = 'Telefone deve ter 10 ou 11 dígitos (com DDD).'
  return e
}

export default function Clients() {
  const [q, setQ] = useState('')
  const { data, error, loading, reload } = useLoad(() => api.clients.list(q), [q])
  const [editing, setEditing] = useState<Client | 'new' | null>(null)
  const toast = useToast()

  async function remove(c: Client) {
    if (!confirm(`Excluir o cliente "${c.name}"?`)) return
    try {
      await api.clients.remove(c.id)
      toast('ok', 'Cliente excluído.')
      reload()
    } catch (e) {
      toast('err', errText(e))
    }
  }

  return (
    <section>
      <div className="bar">
        <h1>Clientes</h1>
        <button className="primary" onClick={() => setEditing('new')}>
          + Novo cliente
        </button>
      </div>
      <input
        type="search"
        placeholder="Buscar por nome ou e-mail"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        aria-label="Buscar clientes"
      />
      {loading && !data ? (
        <Loading />
      ) : error ? (
        <ErrorBox text={error} retry={reload} />
      ) : data && data.length === 0 ? (
        <Empty text={q ? 'Nenhum cliente encontrado.' : 'Nenhum cliente cadastrado.'} />
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>E-mail</th>
                <th>Telefone</th>
                <th aria-label="Ações" />
              </tr>
            </thead>
            <tbody>
              {data?.map((c) => (
                <tr key={c.id}>
                  <td data-label="Nome">{c.name}</td>
                  <td data-label="E-mail">{c.email}</td>
                  <td data-label="Telefone">{phoneMask(c.phone)}</td>
                  <td className="actions">
                    <button onClick={() => setEditing(c)}>Editar</button>
                    <button className="danger" onClick={() => remove(c)}>
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
        <ClientForm
          initial={editing === 'new' ? EMPTY : editing}
          id={editing === 'new' ? null : editing.id}
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

function ClientForm({
  initial,
  id,
  onClose,
  onSaved,
}: {
  initial: ClientInput
  id: number | null
  onClose: () => void
  onSaved: () => void
}) {
  const [f, setF] = useState<ClientInput>({ name: initial.name, email: initial.email, phone: initial.phone })
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
    setSaving(true)
    try {
      if (id) await api.clients.update(id, f)
      else await api.clients.create(f)
      toast('ok', id ? 'Cliente atualizado.' : 'Cliente cadastrado.')
      onSaved()
    } catch (e) {
      if (e instanceof ApiError && Object.keys(e.fields).length) setErrors(e.fields)
      else if (e instanceof ApiError && e.code === 'CONFLICT') setErrors({ email: e.message })
      else setFormError(errText(e))
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal title={id ? 'Editar cliente' : 'Novo cliente'} onClose={onClose}>
      <form onSubmit={submit} noValidate>
        <Field label="Nome" error={errors.name}>
          <input value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} autoFocus />
        </Field>
        <Field label="E-mail" error={errors.email}>
          <input type="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} />
        </Field>
        <Field label="Telefone" error={errors.phone}>
          <input
            inputMode="tel"
            placeholder="(11) 99999-0000"
            value={f.phone}
            onChange={(e) => setF({ ...f, phone: e.target.value })}
          />
        </Field>
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
