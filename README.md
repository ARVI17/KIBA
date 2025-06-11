# KIBA

## Requisitos

### Backend (Python)
- Python 3.10 o superior
- pip
- MySQL en `localhost` (por ejemplo mediante XAMPP)
- Dependencias listadas en `requirements.txt`

### Frontend (Node/React)
- Node.js 18 o superior
- npm o yarn

## Instalaci\u00f3n

### Backend
1. (Opcional) Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usar `venv\Scripts\activate`
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar variables de entorno creando un archivo `.env` en la ra\u00edz y definiendo, por ejemplo:
   ```
   SECRET_KEY=clave-super-secreta-kiba
   ```
   Ajusta la cadena de conexi\u00f3n a la base de datos en `backend/app/config.py` o mediante la variable `SQLALCHEMY_DATABASE_URI` si fuera necesario.

### Frontend
1. Posicionarse en la carpeta `frontend` y ejecutar:
   ```bash
   npm install  # o yarn
   ```

## Ejecuci\u00f3n

### Iniciar el backend
En la ra\u00edz del proyecto:
```bash
python manage.py       # o `python manage.py runserver` si est\u00e1 definido
```

### Iniciar el frontend
Desde la carpeta `frontend`:
```bash
npm start  # o yarn dev seg\u00fan la configuraci\u00f3n del proyecto
```
