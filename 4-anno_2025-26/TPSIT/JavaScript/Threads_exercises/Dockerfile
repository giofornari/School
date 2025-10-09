# Usa un'immagine Python leggera
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file requirements
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutti i file dell'applicazione
COPY . .

# Esponi la porta 5000 per Flask
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["python", "web_app.py"]
