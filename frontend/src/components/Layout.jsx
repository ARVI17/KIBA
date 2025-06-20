import { Link, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext'

export default function Layout() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  }

  return (
    <div>
      <header className="bg-blue-600 text-white">
        <nav className="container mx-auto p-4 flex gap-4">
          <Link to="/">Inicio</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/send-sms">Enviar SMS</Link>
          <Link to="/import-sms">Importar SMS</Link>
          <Link to="/reports">Reportes</Link>
          <button onClick={handleLogout} className="ml-auto">Salir</button>
        </nav>
      </header>
      <main className="p-4">
        <Outlet />
      </main>
    </div>
  )
}
