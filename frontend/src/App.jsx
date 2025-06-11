import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import SendSMS from './pages/SendSMS'
import ImportSMS from './pages/ImportSMS'
import Reports from './pages/Reports'
import Login from './pages/Login'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/send-sms" element={<SendSMS />} />
          <Route path="/import-sms" element={<ImportSMS />} />
          <Route path="/reports" element={<Reports />} />
        </Route>
        <Route path="*" element={<Login />} />
      </Routes>
    </Router>
  )
}
