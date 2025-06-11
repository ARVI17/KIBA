import React, { useState } from 'react';
import * as XLSX from 'xlsx';
import api from '../api';

export default function ImportSMS() {
  const [archivo, setArchivo] = useState(null);
  const [datos, setDatos] = useState([]);
  const [enviado, setEnviado] = useState(false);

  const leerArchivo = (e) => {
    const file = e.target.files[0];
    setArchivo(file);

    const reader = new FileReader();
    reader.onload = (e) => {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const hoja = workbook.Sheets[workbook.SheetNames[0]];
      const datos = XLSX.utils.sheet_to_json(hoja);
      setDatos(datos);
    };
    reader.readAsArrayBuffer(file);
  };

  const enviarSMSMasivos = async () => {
    try {
      const response = await api.post('/importar-sms', {
        mensajes: datos,
      });

      if (response.data.success) {
        setEnviado(true);
      }
    } catch (error) {
      console.error('Error al enviar:', error);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-bold text-blue-600 mb-4">📥 Importar SMS desde Excel</h2>

      <input type="file" accept=".xlsx" onChange={leerArchivo} className="mb-4" />

      {datos.length > 0 && (
        <div className="mb-4">
          <p className="font-semibold">Vista previa:</p>
          <ul className="text-sm bg-gray-100 p-2 rounded-lg max-h-60 overflow-auto">
            {datos.map((item, idx) => (
              <li key={idx}>
                📱 {item.numero} – ✉️ {item.mensaje}
              </li>
            ))}
          </ul>
        </div>
      )}

      <button
        onClick={enviarSMSMasivos}
        disabled={datos.length === 0}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
      >
        Enviar SMS Masivos
      </button>

      {enviado && (
        <p className="text-green-600 mt-4 font-semibold">✅ Envío realizado correctamente</p>
      )}
    </div>
  );
}
