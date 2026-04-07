# Blacklist Microservice

Microservicio para la gestión de lista negra global de emails de una organización.

## Características

- **POST /blacklists**: Agregar un email a la lista negra global
- **GET /blacklists/<email>**: Consultar si un email está en la lista negra
- Autenticación mediante JWT Bearer Token
- Persistencia en PostgreSQL
- Registro de IP y timestamp de solicitudes

## Stack Tecnológico

- Python 3.8+
- Flask 1.1.x
- Flask-SQLAlchemy
- Flask-RESTful
- Flask-Marshmallow
- Flask-JWT-Extended
- Werkzeug
- PostgreSQL

## Instalación y Configuración

### Opción 1: Ejecutar con Docker (Recomendado)

```bash
# Clonar o descargar el proyecto
cd blacklist-microservice

# Ejecutar con Docker Compose (incluye PostgreSQL)
docker-compose up --build

# En segunda terminal, verificar que esté funcionando
curl http://localhost:5000/health
```

El servidor estará disponible en `http://localhost:5000` y PostgreSQL en puerto `5432`

### Opción 2: Instalación Manual

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
cp .env.example .env
# Editar .env con credenciales de PostgreSQL

# Ejecutar la aplicación
python app.py
```

### Comandos Docker Útiles

```bash
# Ejecutar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Parar y eliminar volúmenes (resetea la base de datos)
docker-compose down -v

# Reconstruir imágenes
docker-compose up --build

# Ejecutar comandos en el contenedor
docker-compose exec web bash
docker-compose exec db psql -U blacklist_user -d blacklist_db
```

## Endpoints

### Health Check
- **GET /health**: Verifica el estado del servicio

### Autenticación
- **POST /token**: Obtiene un token de acceso

### Lista Negra
- **POST /blacklists**: Agregar email a lista negra
- **GET /blacklists/<email>**: Consultar estado de email

## Uso con Postman

1. **Ejecutar el microservicio**: `docker-compose up --build`
2. **Importar la colección** `Blacklist_Microservice.postman_collection.json`
3. **Configurar variables**:
   - `baseUrl`: `http://localhost:5000`
   - `accessToken`: (se obtendrá en paso siguiente)
4. **Obtener token**: Ejecutar "Get Authentication Token"
5. **Copiar token**: Del response a la variable `accessToken`
6. **Probar endpoints**: Ejecutar "Add Email to Blacklist" y "Check if Email is Blacklisted"

### Flujo de Pruebas Recomendado
1. Health Check → Verificar servicio
2. Get Token → Obtener autenticación
3. Add Email to Blacklist → Agregar email de prueba
4. Check if Email is Blacklisted → Verificar que esté en lista negra
5. Check Non-Blacklisted Email → Verificar email limpio

## Estructura del Proyecto

```
blacklist-microservice/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── blacklist.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── blacklist_schema.py
│   ├── resources/
│   │   ├── __init__.py
│   │   └── blacklist_resource.py
│   ├── __init__.py
│   └── auth.py
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── init.sql
└── Blacklist_Microservice.postman_collection.json
```

## Ejemplos de Uso

### Agregar email a lista negra
```bash
POST /blacklists
Authorization: Bearer <token>
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "app_uuid": "12345678-1234-1234-1234-123456789012",
    "blocked_reason": "Comportamiento sospechoso"
}
```

### Consultar email
```bash
GET /blacklists/usuario@ejemplo.com
Authorization: Bearer <token>
```

## Consideraciones de Producción

- **Cambiar `JWT_SECRET_KEY`** por una clave segura
- **Usar AWS RDS** para PostgreSQL en producción
- **Configurar variables de entorno** apropiadas
- **Implementar logging** y monitoreo
- **Considerar límites de tasa** (rate limiting)
- **Usar Docker** para despliegue consistente
- **Configurar health checks** en load balancers
- **Implementar backup** de base de datos

## Docker en Producción

Para producción, considerar:

```dockerfile
# Dockerfile.prod con optimizaciones adicionales
FROM python:3.8-slim
# ... configuración optimizada para producción
```

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    build: 
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    # ... configuración de producción
```