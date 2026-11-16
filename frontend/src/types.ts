export interface Client {
  id: number
  name: string
  email: string
  phone: string
}
export interface ClientInput {
  name: string
  email: string
  phone: string
}
export interface Service {
  id: number
  name: string
  description: string | null
  duration_minutes: number
  price: number
}
export interface ServiceInput {
  name: string
  description: string
  duration_minutes: number
  price: number
}
export type AppointmentStatus = 'SCHEDULED' | 'CANCELLED'
export interface Appointment {
  id: number
  client: { id: number; name: string }
  service: { id: number; name: string; duration_minutes: number; price: number }
  start_at: string
  end_at: string
  status: AppointmentStatus
  notes: string | null
}
export interface AppointmentInput {
  client_id: number
  service_id: number
  start_at: string
  notes: string
}
export interface Dashboard {
  total_clients: number
  total_services: number
  today_count: number
  next7_count: number
  scheduled_total: number
  cancelled_total: number
  cancellation_rate: number
  expected_revenue: number
  next_appointments: Appointment[]
}
