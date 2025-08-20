// Minimal in-memory database and a pool shim to satisfy usage in API routes
export type User = { id: number; name: string; email: string; password: string }
export const users: User[] = []

// Simple pool shim matching pool.query(sql, [param]) -> { rows }
export const pool = {
  async query(sql: string, params: any[] = []) {
    if (/SELECT\s+id,\s*name,\s*email\s+FROM\s+users\s+WHERE\s+id\s*=\s*\$1/i.test(sql)) {
      const id = Number(params[0])
      const user = users.find(u => u.id === id)
      return { rows: user ? [{ id: user.id, name: user.name, email: user.email }] : [] }
    }
    return { rows: [] }
  },
  async connect() {
    const client = {
      query: this.query,
      release() { /* no-op for in-memory */ }
    }
    return client
  },
  async end() {
      // no-op for in-memory pool
    }
}
