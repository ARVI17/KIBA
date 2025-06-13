import pathlib

ROOT = pathlib.Path(__file__).resolve().parent / "backend" / "app"

files = [
    ROOT / "routes" / "auth.py",
    ROOT / "routes" / "paciente.py",
    ROOT / "routes" / "sms.py",
    ROOT / "routes" / "cita.py",
    ROOT / "main.py",
]

for path in files:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    new_text = text.replace("from models.", "from backend.app.models.")
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")

print("\u2705 Reemplazo completado correctamente en los archivos")
