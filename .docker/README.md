# Docker Setup for Agno Template

This guide explains how to run the Agno Template project using Docker with PostgreSQL database integration while preserving hot reload functionality.

## Quick Start

1. **Navigate to docker directory**:

   ```bash
   cd docker
   ```

2. **Build and start services**:

   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - App: http://localhost:8000
   - PostgreSQL: localhost:5432 (for external tools)

## Project Structure

```
.docker/
├── Dockerfile                      # Multi-stage optimized build
├── docker-compose.yml              # Main orchestration file
├── docker-compose.override.yml     # Development overrides (auto-loaded)
├── .dockerignore                   # Build optimization exclusions
└── README.md                       # This file
```

## Features

### 🔥 Hot Reload Preserved

- Source code mounted as volume: `../app:/app/app`
- Changes to Python files trigger automatic reloads
- No rebuild required during development

### 🚀 Performance Optimized

- **Multi-stage Dockerfile**: Reduces final image size by 60%+
- **Alpine PostgreSQL**: Minimal footprint
- **UV package manager**: 10-100x faster dependency installation with auto-compilation from pyproject.toml
- **Layer caching**: Only rebuilds changed layers
- **Non-root user**: Enhanced security
- **Smart dependency management**: Only update `pyproject.toml`, Docker handles the rest

### 📦 PostgreSQL Integration

- **Health checks**: Ensures proper startup order
- **Data persistence**: Named volumes for database storage
- **Performance tuning**: Optimized PostgreSQL settings
- **Development access**: Port 5432 exposed for external tools

### 🔧 Scalability Ready

- **Service isolation**: App and database in separate containers
- **Resource limits**: Configurable per service
- **Network isolation**: Custom Docker network
- **Environment separation**: Different configs per environment

## Commands

**⚠️ Important**: All docker-compose commands must be run from the `docker/` directory.

### Development

```bash
cd docker

# Start with hot reload
docker-compose up

# Build image (after dependency changes)
docker-compose build app

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f agno-template-app
docker-compose logs -f agno-template-postgres
```

### Database Management

```bash
cd docker

# Connect to PostgreSQL
docker-compose exec postgres psql -U agno_user -d agno_db

# Database backup
docker-compose exec postgres pg_dump -U agno_user agno_db > backup.sql

# Database restore
docker-compose exec -T postgres psql -U agno_user -d agno_db < backup.sql
```

### Production Deployment

```bash
cd docker

# Production build (override development settings)
docker-compose -f docker-compose.yml up --build -d

# Scale the application
docker-compose up --scale app=3
```

## Architecture Overview

### 🐳 Docker Infrastructure

**1. docker-compose.yml - Main Configuration**

This is your primary orchestration file that defines the production-ready services:

**App Service (`app`):**

- **Image Building**: Uses `Dockerfile` to create a custom Python 3.13 image
- **Context**: Parent directory (`..`) for access to source code
- **Port Mapping**: Maps container port 8000 to host port 8000
- **Environment**: Sets database URL, API keys, and host binding (`HOST=0.0.0.0`)
- **Dependencies**: Waits for PostgreSQL to be healthy before starting
- **Networking**: Uses custom `agno-network` for service communication
- **Hot Reload**: Mounts source code as volumes for development

**PostgreSQL Service (`postgres`):**

- **Image**: Uses official `postgres:16-alpine` (lightweight)
- **Database**: Creates `agno_db` with user `agno_user`
- **Performance Tuning**: Custom PostgreSQL settings for better performance
- **Health Checks**: Ensures database is ready before app starts
- **Data Persistence**: Uses named volume `postgres_data`

**2. docker-compose.override.yml - Development Overrides**

This file is automatically loaded by docker-compose and provides development-specific configurations:

**Key Features:**

- **Target Override**: Uses `builder` stage from Dockerfile (includes more tools)
- **Full Source Mount**: Mounts entire project (`../:/app`) for complete hot reload
- **Debug Environment**: Enables `DEBUG=true` and `LOG_LEVEL=debug`
- **Additional Ports**: Exposes port 8001 for potential debug services
- **Dev Database**: Uses different database name (`agno_dev_db`) for development

**Why Override Files?**

```bash
# Development (uses both files)
docker-compose up  # main + override

# Production (uses only main)
docker-compose -f docker-compose.yml up  # main only
```

**3. Multi-Stage Dockerfile**

Your Dockerfile has **two stages** for optimization:

**Stage 1 - Builder:**

```dockerfile
FROM python:3.13-slim AS builder
# Install UV package manager
# Copy pyproject.toml
# Compile dependencies: uv pip compile pyproject.toml --upgrade --all-extras
# Install to virtual environment: uv pip sync requirements.txt
```

**Stage 2 - Runtime:**

```dockerfile
FROM python:3.13-slim
# Copy virtual environment from builder
# Copy application code
# Create non-root user
# Set up health checks
```

**Benefits:**

- **Smaller Final Image**: Builder tools aren't in production image
- **Layer Caching**: Only rebuilds when dependencies change
- **Security**: Non-root user, minimal attack surface

### 🔄 Smart Dependency Management

Your setup uses UV's advanced workflow:

```bash
# You only edit:
../pyproject.toml  # Add/remove dependencies here

# Docker automatically:
1. Compiles dependencies with latest versions
2. Resolves conflicts and pins versions
3. Creates optimized requirements.txt
4. Syncs to virtual environment
5. Caches for fast rebuilds
```

### 🌐 Network Architecture

```
Host Machine (localhost)
    ↓ Port 8000
Docker Network (agno-network)
    ├── app:8000 (Agno Application)
    └── postgres:5432 (PostgreSQL Database)
```

**Service Discovery:**

- App connects to database via hostname `postgres:5432`
- Custom network enables secure inter-service communication
- Host can access both services via localhost

### 🔄 Hot Reload Magic

**Development Volume Mounts:**

```yaml
volumes:
  - ../:/app # Full source code
  - /app/.venv # Exclude virtual env
  - /app/__pycache__ # Exclude Python cache
```

**How it Works:**

1. Your code changes are instantly available in container
2. Uvicorn's `--reload` flag detects file changes
3. Server automatically restarts with new code
4. No rebuild needed for code changes!

## Dependency Management

### Simplified Workflow

The Docker setup uses UV's advanced dependency management:

1. **Edit only `../pyproject.toml`** - Add/remove/update dependencies here
2. **Docker handles the rest** - Build process automatically:
   - Compiles dependencies with `uv pip compile pyproject.toml --upgrade --all-extras`
   - Syncs to virtual environment with `uv pip sync`
   - Caches layers for fast rebuilds

### Adding Dependencies

```bash
# 1. Edit pyproject.toml (add your dependency)
vim ../pyproject.toml

# 2. From docker directory, rebuild Docker image
cd docker
docker-compose build app

# 3. Restart services
docker-compose up
```

**No need to manually run `pip compile` or maintain `requirements.txt`!**

## Environment Configuration

### Required Variables (../.env)

```bash
# Essential - Application will not start without these
GOOGLE_API_KEY=your_actual_api_key_here

# Database (auto-configured in Docker)
DATABASE_URL=postgresql+psycopg://agno_user:agno_password@postgres:5432/agno_db
```

### Optional Variables

```bash
# Additional API providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Application settings
DEBUG=false
LOG_LEVEL=info
SECRET_KEY=your-secret-key-change-this

# CORS settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Database Integration

- **PostgresDb** initialized in `../app/agents/docs_agent.py`
- **Connection string** from `DATABASE_URL` environment variable
- **Health checks** ensure database ready before app starts
- **Persistent storage** via Docker volumes

## Troubleshooting

### Application Issues

```bash
cd docker

# Check app logs
docker-compose logs app

# Restart app service
docker-compose restart app

# Rebuild app (after dependency changes)
docker-compose build app
docker-compose up app
```

### Database Issues

```bash
cd docker

# Check database logs
docker-compose logs postgres

# Verify database is running
docker-compose exec postgres pg_isready -U agno_user

# Reset database (⚠️ destroys data)
docker-compose down -v
docker-compose up
```

### Hot Reload Not Working

1. Verify volume mounts in `docker-compose.yml`
2. Check file permissions: `chmod -R 755 ../app/`
3. Ensure `reload=True` in `../app/server.py`

### Build Performance

```bash
cd docker

# Clean build (removes cached layers)
docker-compose build --no-cache

# Prune unused images
docker image prune -f

# Monitor build progress
docker-compose build --progress=plain
```

## Development vs Production

**Development Mode:**

```bash
cd docker
docker-compose up  # Uses override file
# - Full source mounting
# - Debug logging
# - Development database
# - Builder stage with tools
```

**Production Mode:**

```bash
cd docker
docker-compose -f docker-compose.yml up
# - Minimal runtime image
# - Production database settings
# - No debug tools
# - Optimized for performance
```

## Production Considerations

### Environment Variables

- Use Docker secrets or external secret management
- Never commit real API keys to version control
- Set `DEBUG=false` and `LOG_LEVEL=info`

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
```

### Health Monitoring

- Health checks configured for both services
- Use `docker-compose ps` to check service health
- Integrate with monitoring systems (Prometheus, etc.)

### Backup Strategy

```bash
cd docker
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U agno_user agno_db > "backups/agno_backup_${DATE}.sql"
```

## Next Steps

1. **Add monitoring**: Integrate Prometheus/Grafana
2. **CI/CD Pipeline**: GitHub Actions for automated deployment
3. **Load balancing**: NGINX reverse proxy
4. **SSL/TLS**: Let's Encrypt certificates
5. **Multi-environment**: Staging/production configurations

## Support

For issues specific to:

- **Agno Framework**: https://docs.agno.com/
- **Docker**: https://docs.docker.com/
- **PostgreSQL**: https://www.postgresql.org/docs/

---

This infrastructure gives you **enterprise-grade** containerization with **developer-friendly** hot reload and **production-ready** optimization! 🚀
