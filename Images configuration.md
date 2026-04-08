# CICD5 Docker Images Configuration

## Step 1: Create Environment Configuration

1. **Navigate to project folder:**
   ```bash
   cd cicd5-main
   ```

2. **Create .env file:**
   - The `.env` file should already exist in your folder
   - If missing, create it with these contents:
   ```env
   # Flask Application Configuration
   PORT=5000
   SECRET_KEY=dev-secret-key-change-in-production
   DEBUG=True

   # Database Configuration
   DB_HOST=cicd5-db
   DB_PORT=5432
   DB_NAME=messages_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_SSL_MODE=disable

   # PostgreSQL Configuration
   POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C
   ```

---

## Step 2: Build BOTH Docker Images

1. **Build the Flask app image:**
   ```bash
   docker build -t samvalentin/cicd5-flask-app -f Dockerfile .
   ```

2. **Build the database image:**
   ```bash
   docker build -t samvalentin/cicd5-postgres-db -f Dockerfile.db .
   ```

3. **Verify both images exist:**
   ```bash
   docker images
   ```
   You should see both images:
   - `samvalentin/cicd5-flask-app`
   - `samvalentin/cicd5-postgres-db`

---

## Step 3: Test BOTH Images Locally

1. **Create Docker network:**
   ```bash
   docker network create cicd5-network
   ```

2. **Run the database container:**
   ```bash
   docker run -d --name cicd5-db --network cicd5-network -p 5432:5432 -v postgres_data:/var/lib/postgresql/data samvalentin/cicd5-postgres-db
   ```

3. **Wait for database to be ready (30 seconds):**
   ```bash
   docker logs cicd5-db
   ```
   Wait until you see "database system is ready to accept connections"

4. **Run the Flask app container:**
   ```bash
   docker run -d --name cicd5-app --network cicd5-network -p 5000:5000 samvalentin/cicd5-flask-app
   ```

5. **Test the application:**
   - Open browser: http://localhost:5000
   - Add a test message
   - Verify it appears in the list
   - Check health endpoint: http://localhost:5000/health

6. **Stop both containers:**
   ```bash
   docker stop cicd5-app cicd5-db
   docker rm cicd5-app cicd5-db
   ```

---

## Step 4: Push BOTH Images to Docker Hub

1. **Login to Docker Hub:**
   ```bash
   docker login
   ```
   Enter your Docker Hub username and password

2. **Push the Flask app image:**
   ```bash
   docker push samvalentin/cicd5-flask-app:latest
   ```

3. **Push the database image:**
   ```bash
   docker push samvalentin/cicd5-postgres-db:latest
   ```

4. **Verify on Docker Hub:**
   - Go to https://hub.docker.com
   - Check your repositories
   - Verify both images appear

---

## Step 5: Test Docker Hub Images

1. **Remove local images:**
   ```bash
   docker rmi samvalentin/cicd5-flask-app samvalentin/cicd5-postgres-db
   ```

2. **Pull both images from Docker Hub:**
   ```bash
   docker pull samvalentin/cicd5-flask-app:latest
   docker pull samvalentin/cicd5-postgres-db:latest
   ```

3. **Run from Docker Hub:**
   ```bash
   # Database with persistent data volume
   docker run -d --name hub-db --network cicd5-network -p 5432:5432 -v postgres_data:/var/lib/postgresql/data samvalentin/cicd5-postgres-db:latest

   # Wait 30 seconds for database

   # Flask app
   docker run -d --name hub-app --network cicd5-network -p 5000:5000 -e DB_HOST=hub-db -e DB_PORT=5432 -e DB_NAME=messages_db -e DB_USER=postgres -e DB_PASSWORD=postgres samvalentin/cicd5-flask-app:latest
   ```

4. **Test the application:**
   - Open browser: http://localhost:5000
   - Verify it works

5. **Cleanup:**
   ```bash
   docker stop hub-app hub-db
   docker rm hub-app hub-db
   ```

---

## Step 6: Test with Docker Compose (Alternative)

1. **Test with docker-compose:**
   ```bash
   docker-compose up --build
   ```
   - Test at: http://localhost:5000
   - Stop: `docker-compose down`

---

## Commands Summary

```bash
# Build both images
docker build -t samvalentin/cicd5-flask-app -f Dockerfile .
docker build -t samvalentin/cicd5-postgres-db -f Dockerfile.db .

# Create network
docker network create cicd5-network

# Run both containers
docker run -d --name cicd5-db --network cicd5-network -p 5432:5432 samvalentin/cicd5-postgres-db
docker run -d --name cicd5-app --network cicd5-network -p 5000:5000 samvalentin/cicd5-flask-app

# Push to Docker Hub
docker push samvalentin/cicd5-flask-app:latest
docker push samvalentin/cicd5-postgres-db:latest

# Cleanup
docker stop cicd5-app cicd5-db
docker rm cicd5-app cicd5-db
docker network rm cicd5-network
```