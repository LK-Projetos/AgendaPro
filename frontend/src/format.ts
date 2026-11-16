export const brl = (v: number) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

export const dateTime = (iso: string) =>
  new Date(iso).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })

export const timeOnly = (iso: string) => new Date(iso).toLocaleTimeString('pt-BR', { timeStyle: 'short' })

/** ISO local ("2030-01-08T10:00:00") -> valor de <input type="datetime-local"> */
export const toInputValue = (iso: string) => iso.slice(0, 16)

export const phoneMask = (digits: string) =>
  digits.length === 11
    ? `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`
    : digits.length === 10
      ? `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`
      : digits
