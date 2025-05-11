# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala herramientas necesarias del sistema como nmap y whois
RUN apt-get update && apt-get install -y nmap whois dnsutils && apt-get clean

# Copia el resto del proyecto
COPY . .

# Variables de entorno para comportamiento de Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWARNINGS=1

# Comando de inicio de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
