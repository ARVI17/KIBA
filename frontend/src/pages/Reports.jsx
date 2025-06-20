import React, { useEffect, useState } from 'react';
import hablame from '../api/hablame';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export default function Reports() {
  const [historial, setHistorial] = useState([]);

  useEffect(() => {
    hablame.get('/historial')
      .then(res => setHistorial(res.data))
      .catch(err => console.error('Error al cargar historial:', err));
  }, []);

  const exportarExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(historial);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Historial');
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    saveAs(new Blob([excelBuffer]), 'Historial_SMS.xlsx');
  };

  const exportarPDF = () => {
    const doc = new jsPDF();
    const tabla = historial.map(item => [item.fecha_envio, item.numero, item.mensaje, item.estado]);
    doc.autoTable({
      head: [['Fecha', 'Número', 'Mensaje', 'Estado']],
      body: tabla,
    });
    doc.save('Historial_SMS.pdf');
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h2 className="text-2xl font-bold text-blue-600 mb-4">📄 Historial de Envíos</h2>

      <div className="flex gap-4 mb-4">
        <button onClick={exportarExcel} className="bg-green-600 text-white px-4 py-2 rounded-lg">Exportar Excel</button>
        <button onClick={exportarPDF} className="bg-red-600 text-white px-4 py-2 rounded-lg">Exportar PDF</button>
      </div>

      <table className="w-full text-sm border shadow-lg bg-white rounded-lg overflow-hidden">
        <thead className="bg-blue-100 text-left">
          <tr>
            <th className="p-2 border">Fecha</th>
            <th className="p-2 border">Número</th>
            <th className="p-2 border">Mensaje</th>
            <th className="p-2 border">Estado</th>
          </tr>
        </thead>
        <tbody>
          {historial.map((item, index) => (
            <tr key={index} className="border-t">
              <td className="p-2 border">{item.fecha_envio}</td>
              <td className="p-2 border">{item.numero}</td>
              <td className="p-2 border">{item.mensaje}</td>
              <td className={`p-2 border font-semibold ${item.estado === 'Entregado' ? 'text-green-600' : 'text-red-600'}`}>{item.estado}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
