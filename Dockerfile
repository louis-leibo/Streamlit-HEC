FROM python:3.11-slim

# Variables d'environnement utiles
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Dossier de travail dans le conteneur
WORKDIR /app

# Dépendances système utiles pour lxml (et futures libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ouvrir le port par défaut de Streamlit
EXPOSE 8501

# Lancer l'application ----
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]