import { expect, test, type Page } from '@playwright/test'
import path from 'node:path'

// E2E reais: navegador Chrome + front (Vite) + API FastAPI + SQLite isolado (e2e/.tmp/e2e.db) com seed fictício.
// Nenhuma chamada é simulada. Os testes rodam em sequência e compartilham o estado do banco isolado.
test.describe.configure({ mode: 'serial' })

const SHOTS = path.resolve(process.cwd(), '../docs/evidencias/capturas')
const shot = (page: Page, name: string) => page.screenshot({ path: path.join(SHOTS, `${name}.png`), fullPage: true })

const CLIENT = 'Cliente E2E'
const CLIENT_EDITED = 'Cliente E2E Editado'
const SERVICE = 'Serviço E2E'

/** Data local daqui a n dias, no formato de <input type="datetime-local"> */
function at(daysAhead: number, hhmm: string) {
  const d = new Date()
  d.setDate(d.getDate() + daysAhead)
  const p = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${hhmm}`
}
const DAY = 40 // longe dos dados do seed

const nav = (page: Page, name: string) => page.getByRole('navigation').getByRole('button', { name, exact: true }).click()
const dialog = (page: Page) => page.getByRole('dialog')
const row = (page: Page, text: string | RegExp) => page.locator('tbody tr', { hasText: text })

async function newAppointment(page: Page, start: string) {
  await page.getByRole('button', { name: '+ Novo agendamento' }).click()
  const d = dialog(page)
  await d.getByLabel('Cliente').selectOption({ label: CLIENT_EDITED })
  await d.getByLabel('Serviço').selectOption({ index: (await d.getByLabel('Serviço').locator('option').allTextContents()).findIndex((t) => t.startsWith(SERVICE)) })
  await d.getByLabel('Data e hora').fill(start)
  await d.getByRole('button', { name: 'Salvar' }).click()
}

test.beforeEach(async ({ page }) => {
  await page.goto('/')
})

test('01 dashboard carrega indicadores reais do banco', async ({ page }) => {
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
  await expect(page.getByTestId('kpi-Clientes').locator('strong')).toHaveText('6')
  await expect(page.getByTestId('kpi-Serviços').locator('strong')).toHaveText('4')
  await expect(page.getByTestId('kpi-Cancelados').locator('strong')).toHaveText('2')
  await expect(page.getByRole('heading', { name: 'Próximos agendamentos' })).toBeVisible()
  await shot(page, '01-dashboard')
})

test('02 telas principais abrem (agendamentos, clientes, serviços)', async ({ page }) => {
  await nav(page, 'Agendamentos')
  await expect(page.getByRole('heading', { name: 'Agendamentos' })).toBeVisible()
  await expect(page.locator('tbody tr')).toHaveCount(10)
  await shot(page, '02-agendamentos')
  await nav(page, 'Clientes')
  await expect(row(page, 'Ana Exemplo')).toBeVisible()
  await shot(page, '03-clientes')
  await nav(page, 'Serviços')
  await expect(row(page, 'Corte de cabelo')).toBeVisible()
  await shot(page, '04-servicos')
})

test('03 validação do formulário de cliente', async ({ page }) => {
  await nav(page, 'Clientes')
  await page.getByRole('button', { name: '+ Novo cliente' }).click()
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  await expect(dialog(page).getByText('Informe o nome')).toBeVisible()
  await expect(dialog(page).getByText('E-mail inválido.')).toBeVisible()
  await expect(dialog(page).getByText('Telefone deve ter 10 ou 11 dígitos')).toBeVisible()
  await shot(page, '05-validacao-cliente')
})

test('04 cadastro de cliente', async ({ page }) => {
  await nav(page, 'Clientes')
  await page.getByRole('button', { name: '+ Novo cliente' }).click()
  await dialog(page).getByLabel('Nome').fill(CLIENT)
  await dialog(page).getByLabel('E-mail').fill('e2e@exemplo.test')
  await dialog(page).getByLabel('Telefone').fill('(11) 98888-7777')
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  await expect(dialog(page)).toBeHidden()
  await expect(row(page, CLIENT)).toContainText('(11) 98888-7777')
})

test('05 e-mail duplicado é rejeitado', async ({ page }) => {
  await nav(page, 'Clientes')
  await page.getByRole('button', { name: '+ Novo cliente' }).click()
  await dialog(page).getByLabel('Nome').fill('Outro Nome')
  await dialog(page).getByLabel('E-mail').fill('e2e@exemplo.test')
  await dialog(page).getByLabel('Telefone').fill('11988887777')
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  await expect(dialog(page).getByText('Já existe um cliente com este e-mail.')).toBeVisible()
})

test('06 edição de cliente', async ({ page }) => {
  await nav(page, 'Clientes')
  await row(page, CLIENT).getByRole('button', { name: 'Editar' }).click()
  await dialog(page).getByLabel('Nome').fill(CLIENT_EDITED)
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  await expect(dialog(page)).toBeHidden()
  await expect(row(page, CLIENT_EDITED)).toBeVisible()
})

test('07 cadastro de serviço com preço "90,50"', async ({ page }) => {
  await nav(page, 'Serviços')
  await page.getByRole('button', { name: '+ Novo serviço' }).click()
  await dialog(page).getByLabel('Nome').fill(SERVICE)
  await dialog(page).getByLabel('Descrição (opcional)').fill('Serviço de teste')
  await dialog(page).getByLabel('Duração (min)').fill('45')
  await dialog(page).getByLabel('Preço (R$)').fill('90,50')
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  await expect(dialog(page)).toBeHidden()
  await expect(row(page, SERVICE)).toContainText('45 min')
  await expect(row(page, SERVICE)).toContainText(/R\$\s*90,50/) // o formato pt-BR usa espaço não separável
})

test('08 validação de serviço e de campo monetário', async ({ page }) => {
  await nav(page, 'Serviços')
  await page.getByRole('button', { name: '+ Novo serviço' }).click()
  const d = dialog(page)
  await d.getByLabel('Nome').fill('Teste Inválido')
  await d.getByLabel('Duração (min)').fill('50')
  await d.getByLabel('Preço (R$)').fill('abc')
  await d.getByRole('button', { name: 'Salvar' }).click()
  await expect(d.getByText('Duração: 15 a 480 min')).toBeVisible()
  await expect(d.getByText('Informe um preço válido')).toBeVisible()
  await d.getByLabel('Preço (R$)').fill('-5')
  await d.getByLabel('Duração (min)').fill('30')
  await d.getByRole('button', { name: 'Salvar' }).click()
  await expect(d.getByText('Informe um preço válido')).toBeVisible()
  await shot(page, '06-validacao-servico')
})

test('09 edição de serviço (preço com milhar "1.234,56")', async ({ page }) => {
  await nav(page, 'Serviços')
  await row(page, SERVICE).getByRole('button', { name: 'Editar' }).click()
  await expect(dialog(page).getByLabel('Preço (R$)')).toHaveValue('90,50')
  await dialog(page).getByLabel('Preço (R$)').fill('1.234,56')
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  await expect(dialog(page)).toBeHidden()
  await expect(row(page, SERVICE)).toContainText(/R\$\s*1\.234,56/)
  // volta para 90,50 para manter o cálculo simples nos próximos testes
  await row(page, SERVICE).getByRole('button', { name: 'Editar' }).click()
  await dialog(page).getByLabel('Preço (R$)').fill('90,50')
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  await expect(row(page, SERVICE)).toContainText(/R\$\s*90,50/)
})

test('10 criação de agendamento (fim calculado pela duração)', async ({ page }) => {
  await nav(page, 'Agendamentos')
  await newAppointment(page, at(DAY, '10:00'))
  await expect(dialog(page)).toBeHidden()
  const r = row(page, CLIENT_EDITED)
  await expect(r).toHaveCount(1)
  await expect(r).toContainText('10:00')
  await expect(r).toContainText('até 10:45')
  await expect(r).toContainText('Agendado')
  await shot(page, '07-agendamento-criado')
})

test('11 conflito de horário é rejeitado e nada é criado', async ({ page }) => {
  await nav(page, 'Agendamentos')
  await newAppointment(page, at(DAY, '10:30')) // sobrepõe 10:00–10:45
  await expect(dialog(page).getByRole('alert')).toContainText('Horário indisponível')
  await shot(page, '08-conflito-rejeitado')
  await dialog(page).getByRole('button', { name: 'Cancelar' }).click()
  await expect(row(page, CLIENT_EDITED)).toHaveCount(1)
  // horário encostado (10:45) é permitido
  await newAppointment(page, at(DAY, '10:45'))
  await expect(dialog(page)).toBeHidden()
  await expect(row(page, CLIENT_EDITED)).toHaveCount(2)
})

test('12 remarcação: conflito mantém original; horário livre atualiza', async ({ page }) => {
  await nav(page, 'Agendamentos')
  const first = row(page, CLIENT_EDITED).filter({ hasText: '10:00' })
  await first.getByRole('button', { name: 'Remarcar' }).click()
  await dialog(page).getByLabel('Novo horário').fill(at(DAY, '10:30')) // conflita com o de 10:45
  await dialog(page).getByRole('button', { name: 'Remarcar' }).click()
  await expect(dialog(page).getByRole('alert')).toContainText('Horário indisponível')
  await dialog(page).getByLabel('Novo horário').fill(at(DAY, '14:00'))
  await dialog(page).getByRole('button', { name: 'Remarcar' }).click()
  await expect(dialog(page)).toBeHidden()
  await expect(row(page, CLIENT_EDITED).filter({ hasText: '14:00' })).toContainText('até 14:45')
  await expect(row(page, CLIENT_EDITED).filter({ hasText: '10:00' })).toHaveCount(0)
})

test('13 cancelamento com confirmação real (recusar e aceitar)', async ({ page }) => {
  await nav(page, 'Agendamentos')
  const r = row(page, CLIENT_EDITED).filter({ hasText: '14:00' })
  page.once('dialog', (d) => d.dismiss()) // recusar: nada muda
  await r.getByRole('button', { name: 'Cancelar' }).click()
  await expect(r).toContainText('Agendado')
  page.once('dialog', (d) => d.accept())
  await r.getByRole('button', { name: 'Cancelar' }).click()
  await expect(r).toContainText('Cancelado')
  await shot(page, '09-cancelamento')
  // o horário cancelado volta a ficar livre
  await newAppointment(page, at(DAY, '14:00'))
  await expect(dialog(page)).toBeHidden()
})

test('14 exclusões com confirmação real e bloqueios', async ({ page }) => {
  await nav(page, 'Clientes')
  page.once('dialog', (d) => d.accept())
  await row(page, CLIENT_EDITED).getByRole('button', { name: 'Excluir' }).click()
  await expect(page.getByRole('status')).toContainText('possui agendamentos')
  await expect(row(page, CLIENT_EDITED)).toBeVisible()

  await nav(page, 'Serviços')
  page.once('dialog', (d) => d.accept())
  await row(page, SERVICE).getByRole('button', { name: 'Excluir' }).click()
  await expect(page.getByRole('status')).toContainText('possui agendamentos')

  // serviço sem agendamentos: recusar mantém; aceitar remove
  await page.getByRole('button', { name: '+ Novo serviço' }).click()
  await dialog(page).getByLabel('Nome').fill('Descartável E2E')
  await dialog(page).getByLabel('Duração (min)').fill('15')
  await dialog(page).getByLabel('Preço (R$)').fill('0')
  await dialog(page).getByRole('button', { name: 'Salvar' }).click()
  const tmp = row(page, 'Descartável E2E')
  await expect(tmp).toBeVisible()
  page.once('dialog', (d) => d.dismiss())
  await tmp.getByRole('button', { name: 'Excluir' }).click()
  await expect(tmp).toBeVisible()
  page.once('dialog', (d) => d.accept())
  await tmp.getByRole('button', { name: 'Excluir' }).click()
  await expect(tmp).toHaveCount(0)
})

test('15 dados persistem após recarregar a página e refletem no dashboard', async ({ page }) => {
  await nav(page, 'Agendamentos')
  await expect(row(page, CLIENT_EDITED)).toHaveCount(3)
  await page.reload()
  await nav(page, 'Agendamentos')
  await expect(row(page, CLIENT_EDITED)).toHaveCount(3)
  await nav(page, 'Dashboard')
  await expect(page.getByTestId('kpi-Clientes').locator('strong')).toHaveText('7')
  await expect(page.getByTestId('kpi-Serviços').locator('strong')).toHaveText('5')
  await expect(page.getByTestId('kpi-Cancelados').locator('strong')).toHaveText('3')
})

test('16 layout móvel sem rolagem horizontal', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 })
  for (const tab of ['Dashboard', 'Agendamentos', 'Clientes', 'Serviços']) {
    await nav(page, tab)
    await expect(page.getByRole('heading', { name: tab })).toBeVisible()
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)
    expect(overflow, `${tab} com rolagem horizontal`).toBe(false)
  }
  await nav(page, 'Agendamentos')
  await shot(page, '10-mobile-agendamentos')
})
