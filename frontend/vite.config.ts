import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// VITE_API_TARGET / VITE_PORT permitem apontar o front para uma API/porta alternativa (usado nos testes E2E)
const api = process.env.VITE_API_TARGET ?? 'http://127.0.0.1:8000'
const port = Number(process.env.VITE_PORT ?? 5173)

export default defineConfig({
  plugins: [react()],
  server: { port, strictPort: true, proxy: { '/api': api } },
})
