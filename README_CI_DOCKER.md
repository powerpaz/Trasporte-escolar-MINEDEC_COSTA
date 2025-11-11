# CI + Docker

## GitHub Actions → Render
Este workflow usa un **Deploy Hook** de Render para disparar el despliegue al hacer push a `main`.

### Pasos
1. En Render, ve a tu servicio → **Settings → Deploy Hooks** y copia el **Deploy Hook** URL.
2. En GitHub, ve a **Settings → Secrets and variables → Actions → New repository secret**:
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: pega la URL del deploy hook copiada de Render.
3. El workflow `.github/workflows/render-deploy.yml` se ejecutará en cada push a `main` o manualmente (Workflow Dispatch).

## Docker (local / VPS)
### Build
```bash
docker build -t transporte-escolar-api .
```
### Run
```bash
docker run --rm -p 8080:8080 -e PORT=8080 transporte-escolar-api
# http://localhost:8080/api/health
```
### Docker Compose
```bash
docker compose up --build
# http://localhost:8080/api/health
```

> El frontend (GitHub Pages) debe apuntar a la URL del backend mediante:
```html
<script>window.API_BASE = 'https://TU-BACKEND';</script>
```