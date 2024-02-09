# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo
COPY . .

# Ejecuta la aplicación cuando se inicie el contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
