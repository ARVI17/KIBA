// frontend/src/pages/Login.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import hablame from '../api/hablame';
import { useAuth } from '../AuthContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [genericError, setGenericError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setEmailError('');
    setPasswordError('');
    setGenericError('');
    try {
      const { data } = await hablame.post('/login', {
        correo: email,
        contrasena: password,
      });
      if (data.success) {
        login(data.token, { email });
        navigate('/dashboard');
      } else if (data.error === 'Email no registrado') {
        setEmailError(data.error);
      } else if (data.error === 'Contraseña incorrecta') {
        setPasswordError(data.error);
      } else {
        setGenericError(data.error || 'Error al iniciar sesión');
      }
    } catch (err) {
      setGenericError('Error al iniciar sesión');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handleLogin} className="bg-white shadow-xl rounded-lg p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold text-blue-600 mb-6 text-center">Iniciar Sesión - CitaMatic</h2>

        {genericError && (
          <div className="alert alert-danger mb-4">{genericError}</div>
        )}

        <div className="mb-4">
          {emailError && <div className="alert alert-danger mb-2">{emailError}</div>}
          <label className="block mb-1 font-semibold">Email</label>
          <input
            type="email"
            className="w-full border px-4 py-2 rounded-lg"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          {passwordError && (
            <div className="alert alert-danger mb-2">{passwordError}</div>
          )}
          <label className="block mb-1 font-semibold">Contraseña</label>
          <input
            type="password"
            className="w-full border px-4 py-2 rounded-lg"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white font-bold py-2 rounded-lg hover:bg-blue-700"
        >
          Iniciar Sesión
        </button>
      </form>
    </div>
  );
}
