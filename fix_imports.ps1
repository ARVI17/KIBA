# Cambia al directorio raíz del proyecto (ajusta si estás en otro lugar)
Set-Location -Path "$PSScriptRoot\backend\app"

# Archivos a modificar
$archivos = @(
    "routes\auth.py",
    "routes\paciente.py",
    "routes\sms.py",
    "routes\cita.py",
    "main.py"
)

# Reemplazar imports antiguos por imports con namespace correcto
foreach ($archivo in $archivos) {
    (Get-Content $archivo) -replace 'from models\.', 'from backend.app.models.' |
    Set-Content $archivo
}

Write-Host "✅ Reemplazo completado correctamente en los archivos"
