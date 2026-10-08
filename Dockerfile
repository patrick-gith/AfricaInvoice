# ---------- Image de base ----------
FROM python:3.14-slim
# ---------- Variables d'environnement ----------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ---------- Dépendances système ----------
# WeasyPrint a besoin de Pango, Cairo, GDK-Pixbuf + polices
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Pour WeasyPrint (PDF)
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    # Polices pour l'affichage correct des PDF
    fonts-dejavu \
    fonts-liberation \
    # Dépendances psycopg2
    gcc \
    libpq-dev \
    # Utilitaires
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# ---------- Dossier de travail ----------
WORKDIR /app

# ---------- Dépendances Python ----------
# Copie d'abord requirements.txt seul pour profiter du cache Docker
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ---------- Code source ----------
COPY . .

# ---------- Collecte des fichiers statiques ----------
RUN python manage.py collectstatic --noinput

# ---------- Port exposé ----------
EXPOSE 8000

# ---------- Commande de démarrage ----------
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn ProjectInvoice.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]
