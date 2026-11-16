import { useState, type FormEvent } from 'react'
import { api, ApiError } from '../api'
import { Empty, ErrorBox, Field, Loading, Modal, useToast } from '../components'
import { brl, dateTime, timeOnly, toInputValue } from '../format'
import { errText, useLoad } from '../hooks'
import type { Appointment } from '../types'

type Status = '' | 'SCHEDULED' | 'CANCELLED'

export default function Appointments() {
  const [status, setStatus] = useState<Status>('')
  const [day, setDay] = useState('')
  const qs = new URLSearchParams()
  if (status) qs.set('status', status)
  if (day) {
    qs.set('date_from', day)
    qs.set('date_to', day)
  }
  const query = qs.toString() ? `?${qs}` : ''
  const { data, error, loading, reload } = useLoad(() => api.appointments.list(query), [query])
  const [editing, setEditing] = useState<Appointment | 'new' | null>(null)
  const [rescheduling, setRescheduling] = useState<Appointment | null>(null)
  const toast = useToast()

  async function cancel(a: Appointment) {
    if (!confirm(`Cancelar o agendamento de ${a.client.name} em ${dateTime(a.start_at)}?`)) return
    try {
      await api.appointments.cancel(a.id)
      toast('ok', 'Agendamento cancelado.')
      reload()
    } catch (e) {
      toast('err', errText(e))
    }
  }
  async function remove(a: Appointment) {
    if (!confirm('Excluir definitivamente este agendamento?')) return
    try {
      await api.appointments.remove(a.id)
      toast('ok', 'Agendamento excluído.')
      reload()
    } catch (e) {
      toast('err', errText(e))
    }
  }

  return (
    <section>
      <div className="bar">
        <h1>Agendamentos</h1>
        <button className="primary" onClick={() => setEditing('new')}>
          + Novo agendamento
        </button>
      </div>
      <div className="filters">
        <label>
          Status
          <select value={status} onChange={(e) => setStatus(e.target.value as Status)}>
            <option value="">Todos</option>
            <option value="SCHEDULED">Agendados</option>
            <option value="CANCELLED">Cancelados</option>
          </select>
        </label>
        <label>
          Dia
          <input type="date" value={day} onChange={(e) => setDay(e.target.value)} />
        </label>
        {(status || day) && (
          <button
            onClick={() => {
              setStatus('')
              setDay('')
            }}
          >
            Limpar filtros
          </button>
        )}
      </div>
      {loading && !data ? (
        <Loading />
      ) : error ? (
        <ErrorBox text={error} retry={reload} />
      ) : data && data.length === 0 ? (
        <Empty text="Nenhum agendamento encontrado." />
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Quando</th>
                <th>Cliente</th>
                <th>Serviço</th>
                <th>Status</th>
                <th aria-label="Ações" />
              </tr>
            </thead>
            <tbody>
              {data?.map((a) => (
                <tr key={a.id} className={a.status === 'CANCELLED' ? 'cancelled' : ''}>
                  <td data-label="Quando">
                    {dateTime(a.start_at)}
                    <small className="muted block">até {timeOnly(a.end_at)}</small>
                  </td>
                  <td data-label="Cliente">{a.client.name}</td>
                  <td data-label="Serviço">
                    {a.service.name}
                    <small className="muted block">{brl(a.service.price)}</small>
                  </td>
                  <td data-label="Status">
                    <span className={`badge ${a.status}`}>{a.status === 'SCHEDULED' ? 'Agendado' : 'Cancelado'}</span>
                  </td>
                  <td className="actions">
                    {a.status === 'SCHEDULED' && (
                      <>
                        <button onClick={() => setEditing(a)}>Editar</button>
                        <button onClick={() => setRescheduling(a)}>Remarcar</button>
                        <button className="danger" onClick={() => cancel(a)}>
                          Cancelar
                        </button>
                      </>
                    )}
                    <button className="danger ghost" onClick={() => remove(a)}>
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
        <AppointmentForm
          appt={editing === 'new' ? null : editing}
          onClose={() => setEditing(null)}
          onSaved={() => {
            setEditing(null)
            reload()
          }}
        />
      )}
      {rescheduling && (
        <RescheduleForm
          appt={rescheduling}
          onClose={() => setRescheduling(null)}
          onSaved={() => {
            setRescheduling(null)
            reload()
          }}
        />
      )}
    </section>
  )
}

function useSubmitError() {
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [formError, setFormError] = useState('')
  function handle(e: unknown) {
    if (e instanceof ApiError && Object.keys(e.fields).length) setErrors(e.fields)
    else setFormError(errText(e)) // inclui conflito de horário
  }
  const reset = () => {
    setErrors({})
    setFormError('')
  }
  return { errors, setErrors, formError, handle, reset }
}

function AppointmentForm({ appt, onClose, onSaved }: { appt: Appointment | null; onClose: () => void; onSaved: () => void }) {
  const clients = useLoad(() => api.clients.list(), [])
  const services = useLoad(api.services.list, [])
  const [clientId, setClientId] = useState(appt ? String(appt.client.id) : '')
  const [serviceId, setServiceId] = useState(appt ? String(appt.service.id) : '')
  const [start, setStart] = useState(appt ? toInputValue(appt.start_at) : '')
  const [notes, setNotes] = useState(appt?.notes ?? '')
  const [saving, setSaving] = useState(false)
  const { errors, setErrors, formError, handle, reset } = useSubmitError()
  const toast = useToast()

  async function submit(ev: FormEvent) {
    ev.preventDefault()
    reset()
    const v: Record<string, string> = {}
    if (!clientId) v.client_id = 'Selecione o cliente.'
    if (!serviceId) v.service_id = 'Selecione o serviço.'
    if (!start) v.start_at = 'Informe data e hora.'
    setErrors(v)
    if (Object.keys(v).length) return
    const body = { client_id: Number(clientId), service_id: Number(serviceId), start_at: start, notes }
    setSaving(true)
    try {
      if (appt) await api.appointments.update(appt.id, body)
      else await api.appointments.create(body)
      toast('ok', appt ? 'Agendamento atualizado.' : 'Agendamento criado.')
      onSaved()
    } catch (e) {
      handle(e)
    } finally {
      setSaving(false)
    }
  }

  const missing = !clients.loading && !services.loading && (!clients.data?.length || !services.data?.length)

  return (
    <Modal title={appt ? 'Editar agendamento' : 'Novo agendamento'} onClose={onClose}>
      {missing ? (
        <p className="error">Cadastre ao menos um cliente e um serviço antes de agendar.</p>
      ) : (
        <form onSubmit={submit} noValidate>
          <Field label="Cliente" error={errors.client_id}>
            <select value={clientId} onChange={(e) => setClientId(e.target.value)}>
              <option value="">Selecione…</option>
              {clients.data?.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Serviço" error={errors.service_id}>
            <select value={serviceId} onChange={(e) => setServiceId(e.target.value)}>
              <option value="">Selecione…</option>
              {services.data?.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.duration_minutes} min · {brl(s.price)})
                </option>
              ))}
            </select>
          </Field>
          <Field label="Data e hora" error={errors.start_at}>
            <input type="datetime-local" step={900} value={start} onChange={(e) => setStart(e.target.value)} />
          </Field>
          <Field label="Observações (opcional)" error={errors.notes}>
            <input value={notes} onChange={(e) => setNotes(e.target.value)} maxLength={500} />
          </Field>
          {formError && (
            <p className="error" role="alert">
              {formError}
            </p>
          )}
          <footer>
            <button type="button" onClick={onClose}>
              Cancelar
            </button>
            <button className="primary" disabled={saving}>
              {saving ? 'Salvando…' : 'Salvar'}
            </button>
          </footer>
        </form>
      )}
    </Modal>
  )
}

function RescheduleForm({ appt, onClose, onSaved }: { appt: Appointment; onClose: () => void; onSaved: () => void }) {
  const [start, setStart] = useState(toInputValue(appt.start_at))
  const [saving, setSaving] = useState(false)
  const { errors, setErrors, formError, handle, reset } = useSubmitError()
  const toast = useToast()

  async function submit(ev: FormEvent) {
    ev.preventDefault()
    reset()
    if (!start) return setErrors({ start_at: 'Informe data e hora.' })
    setSaving(true)
    try {
      await api.appointments.reschedule(appt.id, start)
      toast('ok', 'Agendamento remarcado.')
      onSaved()
    } catch (e) {
      handle(e)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal title="Remarcar agendamento" onClose={onClose}>
      <form onSubmit={submit} noValidate>
        <p className="muted">
          {appt.client.name} · {appt.service.name} ({appt.service.duration_minutes} min)
          <br />
          Atual: {dateTime(appt.start_at)}
        </p>
        <Field label="Novo horário" error={errors.start_at}>
          <input type="datetime-local" step={900} value={start} onChange={(e) => setStart(e.target.value)} autoFocus />
        </Field>
        {formError && (
          <p className="error" role="alert">
            {formError}
          </p>
        )}
        <footer>
          <button type="button" onClick={onClose}>
            Cancelar
          </button>
          <button className="primary" disabled={saving}>
            {saving ? 'Salvando…' : 'Remarcar'}
          </button>
        </footer>
      </form>
    </Modal>
  )
}
