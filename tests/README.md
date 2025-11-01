# Tests de la Blacklist API

Este directorio contiene los tests automatizados para la API de lista negra de emails.

## 📋 Tests Incluidos

### `test_endpoints.py`
Tests para todos los endpoints de la API:

- **TestHealthEndpoint**: Test del health check
- **TestLoginEndpoint**: Tests de autenticación y login
- **TestBlacklistEndpoint**: Tests para agregar emails a la blacklist
- **TestBlacklistEmailEndpoint**: Tests para consultar emails en la blacklist

## 🚀 Cómo Ejecutar los Tests

### Instalar pytest (si no lo tienes)
```bash
pip install pytest pytest-cov
```

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests con más detalle
```bash
pytest -v
```

### Ejecutar tests con reporte de cobertura
```bash
pytest --cov=. --cov-report=html
```

### Ejecutar un archivo específico
```bash
pytest tests/test_endpoints.py
```

### Ejecutar una clase específica
```bash
pytest tests/test_endpoints.py::TestLoginEndpoint
```

### Ejecutar un test específico
```bash
pytest tests/test_endpoints.py::TestLoginEndpoint::test_login_exitoso
```

## 📊 Cobertura de Tests

Los tests cubren:
- ✅ Health check endpoint
- ✅ Login exitoso y fallido
- ✅ Validaciones de autenticación JWT
- ✅ Agregar emails a blacklist (casos exitosos y de error)
- ✅ Consultar emails en blacklist
- ✅ Validaciones de formato de email
- ✅ Validaciones de UUID
- ✅ Manejo de duplicados
- ✅ Límites de caracteres

## 🧪 Estructura de los Tests

Cada test sigue el patrón AAA:
- **Arrange**: Preparar datos y estado
- **Act**: Ejecutar la acción a probar
- **Assert**: Verificar el resultado

## 📝 Fixtures

- `client`: Cliente de prueba de Flask con base de datos en memoria
- `auth_token`: Token JWT válido para tests que requieren autenticación

## 🔧 Base de Datos de Test

Los tests utilizan SQLite en memoria (`:memory:`) para no afectar la base de datos de desarrollo/producción.

