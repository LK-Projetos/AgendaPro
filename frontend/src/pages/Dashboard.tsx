import { api } from '../api'
import { Empty, ErrorBox, Loading } from '../components'
import { brl, dateTime } from '../format'
import { useLoad } from '../hooks'

export default function Dashboard() {
  const { data, error, loading, reload } = useLoad(api.dashboard)
  if (loading && !data) return <Loading />
  if (error || !data) return <ErrorBox text={error ?? 'Sem dados.'} retry={reload} />

  const cards: [string, string | number, string?][] = [
    ['Agendamentos hoje', data.today_count],
    ['Próximos 7 dias', data.next7_count],
    ['Agendamentos ativos', data.scheduled_total],
    ['Cancelados', data.cancelled_total, `${data.cancellation_rate}% do total`],
    ['Receita prevista', brl(data.expected_revenue), 'agendamentos futuros ativos'],
    ['Clientes', data.total_clients],
    ['Serviços', data.total_services],
  ]
  return (
    <section>
      <h1>Dashboard</h1>
      <div className="cards">
        {cards.map(([label, value, hint]) => (
          <div className="card" key={label} data-testid={`kpi-${label}`}>
            <span className="muted">{label}</span>
            <strong>{value}</strong>
            {hint && <small className="muted">{hint}</small>}
          </div>
        ))}
      </div>
      <h2>Próximos agendamentos</h2>
      {data.next_appointments.length === 0 ? (
        <Empty text="Nenhum agendamento futuro." />
      ) : (
        <ul className="list">
          {data.next_appointments.map((a) => (
            <li key={a.id}>
              <div>
                <strong>{dateTime(a.start_at)}</strong> · {a.service.name}
              </div>
              <span className="muted">{a.client.name}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
