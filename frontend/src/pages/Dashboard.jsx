import React, { useEffect, useState } from 'react';
import api from '../api';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Dashboard() {
  const [estadisticas, setEstadisticas] = useState({
    enviados: 0,
    entregados: 0,
    fallidos: 0,
    dias: [],
    cantidades: []
  });

  useEffect(() => {
    api.get('/dashboard')
      .then(res => setEstadisticas(res.data))
      .catch(err => console.error('Error cargando dashboard:', err));
  }, []);

  const data = {
    labels: estadisticas.dias,
    datasets: [
      {
        label: 'SMS enviados',
        data: estadisticas.cantidades,
        backgroundColor: '#3B82F6'
      }
    ]
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h2 className="text-2xl font-bold text-blue-600 mb-4">📊 Dashboard de Envíos</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white shadow-lg p-4 rounded-lg">
          <p className="text-gray-600 font-semibold">Enviados hoy</p>
          <p className="text-3xl text-blue-600 font-bold">{estadisticas.enviados}</p>
        </div>
        <div className="bg-white shadow-lg p-4 rounded-lg">
          <p className="text-gray-600 font-semibold">Entregados</p>
          <p className="text-3xl text-green-600 font-bold">{estadisticas.entregados}</p>
        </div>
        <div className="bg-white shadow-lg p-4 rounded-lg">
          <p className="text-gray-600 font-semibold">Fallidos</p>
          <p className="text-3xl text-red-600 font-bold">{estadisticas.fallidos}</p>
        </div>
      </div>

      <div className="bg-white shadow-lg p-4 rounded-lg">
        <Bar data={data} options={{ responsive: true, plugins: { legend: { display: false } } }} />
      </div>
    </div>
  );
}
