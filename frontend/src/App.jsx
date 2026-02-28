import React, { useState } from 'react';
import DicomUploader from './components/DicomUploader';
import MedicalDashboard from './components/MedicalDashboard';
import { Stethoscope, Loader2 } from 'lucide-react';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <nav className="bg-white border-b border-gray-200 py-4 px-8 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Stethoscope className="text-white h-6 w-6" />
          </div>
          <span className="text-xl font-bold tracking-tight">Radimal <span className="text-blue-600">Insights</span></span>
        </div>
        <div className="text-sm text-gray-500 font-medium">Demo MVP v1.0</div>
      </nav>

      <main className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {!analysisResult ? (
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-10">
              <h1 className="text-4xl font-extrabold text-gray-900 mb-4">Análisis Radiológico con IA</h1>
              <p className="text-lg text-gray-600">Sube archivos DICOM para obtener reportes estructurados instantáneos validados por nuestro sistema de Guardrails.</p>
            </div>

            {loading ? (
              <div className="flex flex-col items-center justify-center py-20">
                <Loader2 className="h-12 w-12 text-blue-600 animate-spin mb-4" />
                <p className="text-gray-500 font-medium">Procesando imagen médica y generando reporte...</p>
              </div>
            ) : (
              <DicomUploader
                onUploadStart={() => { setLoading(true); setError(null); }}
                onUploadSuccess={(data) => { setAnalysisResult(data); setLoading(false); }}
                onUploadError={(err) => { setError(err); setLoading(false); }}
              />
            )}

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
                Error: {error}
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <button
                onClick={() => setAnalysisResult(null)}
                className="text-blue-600 hover:text-blue-800 font-medium flex items-center"
              >
                ← Cargar otro estudio
              </button>
            </div>
            <MedicalDashboard data={analysisResult} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
