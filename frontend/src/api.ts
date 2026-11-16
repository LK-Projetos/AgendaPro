import type {
  Appointment,
  AppointmentInput,
  Client,
  ClientInput,
  Dashboard,
  Service,
  ServiceInput,
} from './types'

export class ApiError extends Error {
  status: number
  code: string
  fields: Record<string, string>
  constructor(status: number, code: string, message: string, fields: Record<string, string> = {}) {
    super(message)
    this.status = status
    this.code = code
    this.fields = fields
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  let res: Response
  try {
    res = await fetch(`/api${path}`, {
      method,
      headers: body === undefined ? undefined : { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new ApiError(0, 'NETWORK', 'Não foi possível conectar ao servidor. Verifique se a API está em execução.')
  }
  if (res.status === 204) return undefined as T
  let data: any = null
  try {
    data = await res.json()
  } catch {
    /* corpo vazio ou inválido */
  }
  if (!res.ok) {
    throw new ApiError(
      res.status,
      data?.code ?? 'ERROR',
      data?.message ?? `Erro inesperado (${res.status}).`,
      data?.details?.fields ?? {},
    )
  }
  return data as T
}

export const api = {
  dashboard: () => request<Dashboard>('GET', '/dashboard'),
  clients: {
    list: (q = '') => request<Client[]>('GET', `/clients${q ? `?q=${encodeURIComponent(q)}` : ''}`),
    create: (d: ClientInput) => request<Client>('POST', '/clients', d),
    update: (id: number, d: ClientInput) => request<Client>('PUT', `/clients/${id}`, d),
    remove: (id: number) => request<void>('DELETE', `/clients/${id}`),
  },
  services: {
    list: () => request<Service[]>('GET', '/services'),
    create: (d: ServiceInput) => request<Service>('POST', '/services', d),
    update: (id: number, d: ServiceInput) => request<Service>('PUT', `/services/${id}`, d),
    remove: (id: number) => request<void>('DELETE', `/services/${id}`),
  },
  appointments: {
    list: (qs = '') => request<Appointment[]>('GET', `/appointments${qs}`),
    create: (d: AppointmentInput) => request<Appointment>('POST', '/appointments', d),
    update: (id: number, d: AppointmentInput) => request<Appointment>('PUT', `/appointments/${id}`, d),
    reschedule: (id: number, start_at: string) =>
      request<Appointment>('POST', `/appointments/${id}/reschedule`, { start_at }),
    cancel: (id: number) => request<Appointment>('POST', `/appointments/${id}/cancel`),
    remove: (id: number) => request<void>('DELETE', `/appointments/${id}`),
  },
}
