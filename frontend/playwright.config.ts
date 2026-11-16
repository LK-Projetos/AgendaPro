import { defineConfig } from '@playwright/test'

const API_PORT = 8001
const WEB_PORT = 5174

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1, // os cenários compartilham um banco isolado e rodam em sequência
  retries: 0,
  timeout: 30_000,
  reporter: [['list'], ['html', { outputFolder: 'e2e/.report', open: 'never' }]],
  use: {
    baseURL: `http://127.0.0.1:${WEB_PORT}`,
    channel: 'chrome', // usa o Google Chrome instalado (sem baixar navegadores)
    viewport: { width: 1280, height: 800 },
    locale: 'pt-BR',
    timezoneId: 'America/Sao_Paulo',
  },
  webServer: [
    {
      command: 'node e2e/start-api.mjs',
      url: `http://127.0.0.1:${API_PORT}/api/health`,
      reuseExistingServer: false,
      timeout: 60_000,
      env: { E2E_API_PORT: String(API_PORT) },
    },
    {
      command: 'npm run dev -- --host 127.0.0.1',
      url: `http://127.0.0.1:${WEB_PORT}`,
      reuseExistingServer: false,
      timeout: 60_000,
      env: { VITE_PORT: String(WEB_PORT), VITE_API_TARGET: `http://127.0.0.1:${API_PORT}` },
    },
  ],
})
