import { Link, Outlet } from 'react-router-dom'

export default function Layout() {
  return (
    <div>
      <header className="bg-blue-600 text-white">
        <nav className="container mx-auto p-4 flex gap-4">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/send-sms">Enviar SMS</Link>
          <Link to="/import-sms">Importar SMS</Link>
          <Link to="/reports">Reportes</Link>
          <Link to="/login" className="ml-auto">Salir</Link>
        </nav>
      </header>
      <main className="p-4">
        <Outlet />
      </main>
    </div>
  )
}
