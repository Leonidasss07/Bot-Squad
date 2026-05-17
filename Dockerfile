# Base con Python para ejecutar la app
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias 
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto dentro del contenedor
COPY . .

# Exponer el puerto donde se ejecuta Streamlit
EXPOSE 8501

# Ejecutar la aplicación Streamlit
CMD ["streamlit", "run", "web/app.py", "--server.address=0.0.0.0", "--server.port=8501"]