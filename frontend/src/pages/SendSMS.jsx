import React, { useState } from 'react';
import api from '../api';

export default function SendSMS() {
  const [numero, setNumero] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [respuesta, setRespuesta] = useState(null);
  const [error, setError] = useState('');

  const enviarSMS = async (e) => {
    e.preventDefault();
    setError('');
    setRespuesta(null);

    try {
      const res = await api.post('/enviar-sms', {
        numero,
        mensaje
      });

      if (res.data.success) {
        setRespuesta('SMS enviado exitosamente.');
        setNumero('');
        setMensaje('');
      } else {
        setError('Error en el envío.');
      }
    } catch (err) {
      setError('Error al conectar con el servidor.');
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-blue-600">📤 Enviar SMS</h2>
      <form onSubmit={enviarSMS} className="space-y-4 bg-white shadow-lg p-6 rounded-lg">
        {respuesta && <p className="text-green-600">{respuesta}</p>}
        {error && <p className="text-red-600">{error}</p>}

        <div>
          <label className="block font-semibold mb-1">Número de teléfono</label>
          <input
            type="text"
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            required
            placeholder="573001112233"
            className="w-full border px-3 py-2 rounded-lg"
          />
        </div>

        <div>
          <label className="block font-semibold mb-1">Mensaje</label>
          <textarea
            value={mensaje}
            onChange={(e) => setMensaje(e.target.value)}
            required
            rows={4}
            className="w-full border px-3 py-2 rounded-lg"
            placeholder="Texto del SMS"
          ></textarea>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white font-bold py-2 rounded-lg hover:bg-blue-700"
        >
          Enviar SMS
        </button>
      </form>
    </div>
  );
}
