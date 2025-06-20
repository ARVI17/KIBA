import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Dashboard from './pages/Dashboard'
import SendSMS from './pages/SendSMS'
import ImportSMS from './pages/ImportSMS'
import Reports from './pages/Reports'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/send-sms" element={<SendSMS />} />
            <Route path="/import-sms" element={<ImportSMS />} />
            <Route path="/reports" element={<Reports />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  )
}
