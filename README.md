# CICD-Laborator5

## Descriere Proiect

Acest proiect este o aplicație web simplă de tip "Message Board" creată în cadrul Laboratorului 5 pentru automatizarea procesului de livrare a aplicațiilor în producție prin metoda CI/CD. Aplicația permite utilizatorilor să adauge și să vizualizeze mesaje stocate într-o bază de date.

### Stack Tehnologic

- **Backend**: Python Flask
- **Bază de date**: PostgreSQL 15
- **Containerizare**: Docker & Docker Compose
- **CI/CD**: GitHub Actions (pentru automatizarea build și deploy)

## Structura Proiectului

```
CICD-Laborator5/
├── application.py          # Aplicația Flask principală
├── Dockerfile             # Fișier pentru containerizarea aplicației
├── docker-compose.yml     # Fișier pentru orchestrarea serviciilor
├── init.sql               # Script de inițializare a bazei de date
├── requirements.txt       # Dependințe Python
├── README.md              # Documentația proiectului
└── logs/                  # Director pentru loguri
```

## Funcționalități

Aplicația oferă următoarele funcționalități:
- Adăugarea de mesaje noi în baza de date
- Vizualizarea tuturor mesajelor stocate
- Interfață web simplă și intuitivă

## Sarcini Realizate

### 1. Crearea aplicației web legată cu o bază de date

Aplicația Flask (`application.py`) se conectează la o bază de date PostgreSQL și permite:
- Adăugarea mesajelor prin formularul web
- Afișarea tuturor mesajelor din baza de date

### 2. Crearea fișierului Dockerfile

Fișierul [`Dockerfile`](Dockerfile:1) definește imaginea Docker pentru aplicație:
- Folosește imaginea de bază `python:3.11-slim`
- Instalează dependențele din `requirements.txt`
- Copiază fișierele aplicației
- Rulează aplicația pe portul 5000

### 3. Crearea fișierului docker-compose.yml

Fișierul [`docker-compose.yml`](docker-compose.yml:1) definește două servicii:
- **web**: Aplicația Flask (port 5000)
- **db**: Baza de date PostgreSQL 15

### 4. Construirea și rularea containerului local

```bash
# Construirea și pornirea serviciilor
docker-compose up --build

# Rularea în background
docker-compose up -d --build

# Oprirea serviciilor
docker-compose down

# Vizualizarea logurilor
docker-compose logs -f
```

### 5. Construirea imaginii Docker

```bash
# Construirea imaginii
docker build -t cicd-laborator5:latest .

# Listarea imaginilor
docker images
```

### 6. Încărcarea imaginii pe Docker Hub

```bash
# Login în Docker Hub
docker login

# Tag-uirea imaginii pentru Docker Hub
docker tag samvalentin/cicd-laborator5:latest samvalentin/cicd-laborator5:latest

# Încărcarea imaginii
docker push username/myapp:latest
```

### 7. Verificarea imaginii pe Docker Hub

Accesați [Docker Hub](https://hub.docker.com/) și verificați că imaginea a fost încărcată corect.

## Accesarea Aplicației

După pornirea serviciilor cu Docker Compose, aplicația este accesibilă la:
```
http://localhost:5000
```
