# CICD5 - Flask Messages App with Docker

**Aplicație web containerizată cu Docker, Flask și PostgreSQL**

## Descriere

Acest proiect demonstrează utilizarea **Docker** pentru containerizarea unei aplicații web Flask cu bază de date PostgreSQL, folosind practici moderne de securitate și orchestrare.

**Autor:** Samciucov Valentin  
**Tehnologii:** Flask, PostgreSQL, Docker, Docker Compose

## 🛠️ Tehnologii Folosite

### Backend
- **Flask 2.3.3** - Framework web Python
- **psycopg2-binary** - Driver PostgreSQL
- **Gunicorn** - WSGI server

### Database
- **PostgreSQL 15** - Bază de date relațională
- **Persistență date** cu volume Docker

### Containerization & Orchestration
- **Docker** - Container engine (industry standard)
- **Docker Compose** - Orchestration multi-container
- **Dockerfile** - Definiție imagine (standard Docker)

## Structura Proiectului

```
cicd-laborator5/
├── application.py           # Aplicația Flask principală
├── Dockerfile              # Definiție imagine Docker pentru Flask
├── Dockerfile.db           # Definiție imagine Docker pentru PostgreSQL
├── requirements.txt        # Dependințe Python
├── docker-compose.yml      # Configurare orchestrare
├── init.sql               # Script inițializare bază de date
├── .env                   # Variabile de mediu pentru testare locală
├── .env.compose           # Variabile de mediu pentru docker-compose
├── Images configuration.md         # Ghid complet pas cu pas
├── templates/
│   └── index.html         # Template HTML
└── README.md              # Documentație
```

## Quick Start

### Prerechizite

1. **Instalare Docker Desktop:**
   - **Windows:** Descarcă de la [docker.com](https://www.docker.com/products/docker-desktop)
   - **macOS:** Descarcă de la [docker.com](https://www.docker.com/products/docker-desktop)
   - **Linux:** `sudo apt install docker.io docker-compose`

2. **Verificare instalare:**
   ```bash
   docker --version
   docker-compose version
   ```

### Opțiunea 1: Docker Compose

1. **Clonare repository:**
   ```bash
   git clone https://github.com/SamValentin7/CICD-Laborator5.git
   cd CICD-Laborator5
   ```

2. **Construire și pornire servicii:**
   ```bash
   docker-compose up --build
   ```

3. **Accesare aplicație:**
   - **URL:** http://localhost:5000

4. **Oprire servicii:**
   ```bash
   docker-compose down
   ```

### Opțiunea 2: Imagini Docker Individuale

1. **Build imagini:**
   ```bash
   docker build -t samvalentin/cicd5-flask-app -f Dockerfile .
   docker build -t samvalentin/cicd5-postgres-db -f Dockerfile.db .
   ```

2. **Creare rețea:**
   ```bash
   docker network create cicd5-network
   ```

3. **Pornire database:**
   ```bash
   docker run -d --name cicd5-db --network cicd5-network -p 5432:5432 -v postgres_data:/var/lib/postgresql/data samvalentin/cicd5-postgres-db
   ```

4. **Așteptare 30 secunde** pentru inițializarea bazei de date

5. **Pornire Flask app:**
   ```bash
   docker run -d --name cicd5-app --network cicd5-network -p 5000:5000 samvalentin/cicd5-flask-app
   ```

6. **Accesare aplicație:** http://localhost:5000

## Imagini Docker Hub

Proiectul include două imagini publice pe Docker Hub:

- **Flask App:** [samvalentin/cicd5-flask-app](https://hub.docker.com/repository/docker/samvalentin/cicd5-flask-app)
- **PostgreSQL DB:** [samvalentin/cicd5-postgres-db](https://hub.docker.com/repository/docker/samvalentin/cicd5-postgres-db)

### Utilizare imagini din Docker Hub:

```bash
# Database
docker run -d --name hub-db --network cicd5-network -p 5432:5432 -v postgres_data:/var/lib/postgresql/data samvalentin/cicd5-postgres-db:latest

# Flask app
docker run -d --name hub-app --network cicd5-network -p 5000:5000 -e DB_HOST=hub-db -e DB_PORT=5432 -e DB_NAME=messages_db -e DB_USER=postgres -e DB_PASSWORD=postgres samvalentin/cicd5-flask-app:latest
```

## Comenzi Docker Utile

### Construire Imagini
```bash
docker build -t samvalentin/cicd5-flask-app -f Dockerfile .
docker build -t samvalentin/cicd5-postgres-db -f Dockerfile.db .
```

### Rulare Containere
```bash
docker run -d --name cicd5-db --network cicd5-network -p 5432:5432 -v postgres_data:/var/lib/postgresql/data samvalentin/cicd5-postgres-db
docker run -d --name cicd5-app --network cicd5-network -p 5000:5000 samvalentin/cicd5-flask-app
```

### Management Containere
```bash
docker ps                    # Listează containere active
docker ps -a                 # Listează toate containerele
docker logs cicd5-db         # Vizualizează log-uri database
docker logs cicd5-app        # Vizualizează log-uri aplicație
docker stop cicd5-app cicd5-db    # Oprește containere
docker rm cicd5-app cicd5-db      # Șterge containere
```

### Management Volume
```bash
docker volume ls             # Listează volume
docker volume inspect postgres_data  # Inspectează volum
docker volume rm postgres_data       # Șterge volum
```

## Configurare Mediului

### Variabile de Mediu
- `DB_HOST` - Host bază de date (default: cicd5-db)
- `DB_PORT` - Port bază de date (default: 5432)
- `DB_NAME` - Nume bază de date (default: messages_db)
- `DB_USER` - Utilizator PostgreSQL (default: postgres)
- `DB_PASSWORD` - Parolă PostgreSQL (default: postgres)

### Volume Persistente
- `postgres_data` - Date PostgreSQL
- Asigură persistența datelor între repornirile containerelor

## Securitate Docker

### Bune Practici
- Utilizare non-root user în containere
- Volume pentru persistența datelor
- Health checks pentru monitorizare
- Network isolation între servicii
- Variabile de mediu pentru configurare

### Probleme Comune

1. **Port deja folosit:**
   ```bash
   docker-compose down
   docker ps -a
   docker rm $(docker ps -aq)
   ```

2. **Probleme conectare bază de date:**
   ```bash
   docker logs cicd5-db
   docker-compose restart db
   ```

3. **Resetare completă baze de date:**
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

4. **Docker Desktop nu pornește:**
   - Verifică dacă virtualizarea este activată în BIOS
   - Restart Docker Desktop
   - Reinstalează Docker Desktop dacă este necesar

**Laborator 5 - Containerizare cu Docker**  
*Creat de Samciucov Valentin © 2026*