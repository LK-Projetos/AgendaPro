// Sobe a API para os testes E2E com um banco SQLite ISOLADO e descartável (e2e/.tmp/e2e.db),
// populado com o seed fictício. Nunca toca em backend/agendapro.db.
import { spawn, spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, rmSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const backend = resolve(here, '../../backend')
const tmp = join(here, '.tmp')
const dbFile = join(tmp, 'e2e.db')
const py = process.env.PYTHON ?? (existsSync(join(backend, '.venv/Scripts/python.exe'))
  ? join(backend, '.venv/Scripts/python.exe')
  : join(backend, '.venv/bin/python'))

mkdirSync(tmp, { recursive: true })
for (const f of [dbFile, `${dbFile}-wal`, `${dbFile}-shm`]) rmSync(f, { force: true })

const env = { ...process.env, AGENDAPRO_DB_URL: `sqlite:///${dbFile.replaceAll('\\', '/')}` }
const seed = spawnSync(py, ['-m', 'app.seed'], { cwd: backend, env, stdio: 'inherit' })
if (seed.status !== 0) process.exit(seed.status ?? 1)

const api = spawn(py, ['-m', 'uvicorn', 'app.main:app', '--port', process.env.E2E_API_PORT ?? '8001'], {
  cwd: backend,
  env,
  stdio: 'inherit',
})
const stop = () => api.kill()
process.on('SIGINT', stop)
process.on('SIGTERM', stop)
api.on('exit', (code) => process.exit(code ?? 0))
