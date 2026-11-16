import { createContext, useCallback, useContext, useState, type ReactNode } from 'react'

/* ---------- Toasts ---------- */
type Toast = { id: number; kind: 'ok' | 'err'; text: string }
const ToastCtx = createContext<(kind: Toast['kind'], text: string) => void>(() => {})
export const useToast = () => useContext(ToastCtx)

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<Toast[]>([])
  const push = useCallback((kind: Toast['kind'], text: string) => {
    const id = Date.now() + Math.random()
    setItems((l) => [...l, { id, kind, text }])
    setTimeout(() => setItems((l) => l.filter((t) => t.id !== id)), 5000)
  }, [])
  return (
    <ToastCtx.Provider value={push}>
      {children}
      <div className="toasts" role="status" aria-live="polite">
        {items.map((t) => (
          <div key={t.id} className={`toast ${t.kind}`}>
            {t.text}
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  )
}

/* ---------- Modal ---------- */
export function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  return (
    <div className="overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal" role="dialog" aria-modal="true" aria-label={title}>
        <header>
          <h2>{title}</h2>
          <button className="icon" onClick={onClose} aria-label="Fechar">
            ×
          </button>
        </header>
        {children}
      </div>
    </div>
  )
}

/* ---------- Campo de formulário ---------- */
export function Field({ label, error, children }: { label: string; error?: string; children: ReactNode }) {
  return (
    <label className={`field${error ? ' invalid' : ''}`}>
      <span>{label}</span>
      {children}
      {error && <small className="error">{error}</small>}
    </label>
  )
}

/* ---------- Estados de carregamento ---------- */
export const Loading = () => <p className="muted">Carregando…</p>
export const ErrorBox = ({ text, retry }: { text: string; retry?: () => void }) => (
  <div className="alert">
    <span>{text}</span>
    {retry && <button onClick={retry}>Tentar novamente</button>}
  </div>
)
export const Empty = ({ text }: { text: string }) => <p className="empty">{text}</p>
