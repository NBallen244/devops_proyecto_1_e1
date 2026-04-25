# Guía de Pruebas con Docker - Blacklist Microservice

## Estructura de Pruebas

```
tests/
├── __init__.py
├── conftest.py           # Configuración y fixtures de pytest
├── test_blacklist.py     # Pruebas para endpoints de blacklist
├── test_auth.py          # Pruebas de autenticación
└── test_health.py        # Pruebas del health check
```

## Ejecutar Pruebas en Docker

### Opción 1: Usando docker-compose (RECOMENDADO)

```bash
# Levantar los servicios
docker-compose up -d

# Ejecutar las pruebas
docker-compose exec blacklist-microservice pytest

# Ejecutar con cobertura
docker-compose exec blacklist-microservice pytest --cov=app --cov-report=term-missing

# O ejecutar en un contenedor temporal
docker-compose run --rm blacklist-microservice pytest --cov=app
```

### Opción 2: Ejecutar en contenedor individual

```bash
# Construir la imagen
docker build -t blacklist-microservice .

# Ejecutar las pruebas en un contenedor temporal
docker run --rm blacklist-microservice pytest

# Con cobertura
docker run --rm blacklist-microservice pytest --cov=app --cov-report=term-missing
```

### Opción 3: En contenedor existente

Si ya tienes el contenedor corriendo:
```bash
# Buscar el ID del contenedor
docker ps | grep blacklist

# Ejecutar las pruebas
docker exec -it <container_id> pytest

# Con cobertura
docker exec -it <container_id> pytest --cov=app --cov-report=term-missing
```

## Comandos Útiles de Pruebas en Docker

### Ejecutar pruebas con diferentes opciones

```bash
# Ver resultados detallados
docker-compose exec blacklist-microservice pytest -v

# Ejecutar solo un archivo de pruebas
docker-compose exec blacklist-microservice pytest tests/test_blacklist.py

# Ejecutar una prueba específica
docker-compose exec blacklist-microservice pytest tests/test_blacklist.py::TestBlacklistPost::test_add_email_to_blacklist_success

# Ver cobertura con detalles
docker-compose exec blacklist-microservice pytest --cov=app --cov-report=term-missing

# Parar en el primer error
docker-compose exec blacklist-microservice pytest -x
```

## Cobertura Actual

La cobertura actual del código es del **82%**, cubriendo:

- ✅ Todos los endpoints principales (`POST /blacklists`, `GET /blacklists/<email>`, `DELETE /blacklists`)
- ✅ Autenticación JWT
- ✅ Health check
- ✅ Generación de tokens
- ✅ Validación de datos
- ✅ Manejo de errores comunes

## Casos de Prueba Implementados

### POST /blacklists
- ✅ Agregar email válido exitosamente
- ✅ Rechazar email duplicado (409)
- ✅ Validar formato de email inválido (400)
- ✅ Validar UUID inválido (400)
- ✅ Rechazar sin token JWT (401)
- ✅ Validar campos requeridos
- ✅ Permitir agregar sin razón de bloqueo

### GET /blacklists/{email}
- ✅ Email existe en blacklist
- ✅ Email no existe en blacklist
- ✅ Rechazar sin token JWT (401)
- ✅ Verificar múltiples emails secuencialmente

### DELETE /blacklists
- ✅ Limpiar base de datos exitosamente
- ✅ Limpiar base de datos vacía
- ✅ Rechazar sin token JWT (401)
- ✅ Verificar que todos los emails fueron eliminados

### Autenticación
- ✅ Generar token exitosamente
- ✅ Token generado funciona en endpoints protegidos
- ✅ Rechazar token inválido
- ✅ Rechazar sin token
- ✅ Rechazar header de autorización malformado

### Health Check
- ✅ Retornar estado healthy
- ✅ No requiere autenticación
- ✅ Solo acepta método GET

## Requisitos

Para ejecutar las pruebas necesitas:

1. **Docker y Docker Compose instalados**
2. **Imagen construida con las dependencias de pruebas**

Las pruebas ya están incluidas en la imagen Docker y usan SQLite en memoria para no depender de PostgreSQL durante las pruebas.

## Troubleshooting

### Error: "pytest: command not found"
Asegúrate de que la imagen Docker incluya las dependencias de pruebas. Reconstruye la imagen:
```bash
docker-compose build blacklist-microservice
```

### Error al ejecutar pruebas
Si las pruebas fallan, verifica que:
1. El contenedor esté corriendo: `docker-compose ps`
2. Las dependencias estén instaladas: pytest está incluido en requirements.txt
3. El directorio tests/ esté presente en el contenedor