import React from 'react';
import { useAuth } from '../AuthContext';

export default function Home() {
  const { getUser } = useAuth();
  const user = getUser();
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4 text-blue-600">Bienvenido a CitaMatic</h1>
      {user && <p className="text-gray-700">Sesión iniciada como {user.email}</p>}
    </div>
  );
}
