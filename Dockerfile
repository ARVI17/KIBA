FROM python:3.11.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "5000"]
