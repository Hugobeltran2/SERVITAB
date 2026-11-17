# SERVITAB - Sistema de Gestión y Suministro Privado de Agua

**SERVITAB S.A. de C.V.** es una plataforma integral para la gestión técnica, operativa, comercial y de distribución de agua potable y tratada, diseñada específicamente para la región de **Villahermosa, Tabasco**.

El sistema permite administrar el ciclo hídrico completo de operaciones privadas:
1. **Captación:** Registro de fuentes superficiales (Río Carrizal, Río Grijalva, Río La Sierra) y pozos profundos concesionados.
2. **Potabilización y Calidad:** Control de dosificación química (Sulfato de aluminio, PAC, Polímeros, Gas cloro) y monitoreo de calidad según la norma **NOM-127-SSA1-2021** (turbiedad en NTU, cloro residual y pH).
3. **Almacenamiento y Bombeo:** Gestión de tanques elevados, cisternas de almacenamiento y estaciones de rebombeo (Ciudad Deportiva, Tabasco 2000, Loma de Caballo).
4. **Distribución y Redes:** Sectorización de zonas (Tabasco 2000, Tamulté, Atasta, Centro, Ciudad Industrial, Corredor Parrilla) y acueductos (Acueducto Usumacinta, matrices de alta presión).
5. **Comercial / CRM:** Padrón de clientes empresariales, residenciales privados, hoteleros e industriales; asignación y lectura de medidores.
6. **Facturación y Cobranza:** Facturación en Pesos Mexicanos (MXN), tarifas por m³, emisión de recibos con código de barras/imprimibles y registro de cobranza (Efectivo, TPV, SPEI, OXXO).
7. **Reportes:** Paneles dinámicos, exportación a Excel/CSV de recaudación, morosidad y consumos.

---

## 🚀 Requisitos Previos

- Python 3.10 o superior (compatible con Python 3.12 y 3.13)
- Git
- SQLite (incluido por defecto para desarrollo) o MySQL 8.0+ / PostgreSQL (para producción)

---

## 🛠️ Instalación y Puesta en Marcha Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/servitab-water-management.git
cd servitab-water-management
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
En Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar y precargar datos de Villahermosa
```bash
flask --app app.py init-db
flask --app app.py seed-villahermosa
```

### 5. Iniciar el servidor de desarrollo
```bash
python app.py
```
Abre en tu navegador: `http://127.0.0.1:5000`

---

## 🔐 Credenciales Precargadas para Evaluación

| Rol | Usuario | Contraseña | Perfil |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin_servitab` | `AdminServitab2026!` | Acceso total al panel, reportes y configuración |
| **Operador Planta** | `operador_planta` | `Operador2026!` | Registro de dosificación química y lecturas |
| **Logística Pipas** | `logistica_pipas` | `Pipas2026!` | Control de distribución y lecturas de medidores |
| **Cajero / Cobranza** | `cajero_servitab` | `CajaServitab2026!` | Emisión de comprobantes y cobro de recibos |

---

## ⚙️ Variables de Entorno (Producción)

Crea un archivo `.env` en la raíz del proyecto para producción:

```env
SECRET_KEY=clave_secreta_de_produccion_muy_segura
USE_MYSQL=true
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=usuario_servitab
MYSQL_PASSWORD=password_seguro
MYSQL_DB=servitab_water
WATER_RATE_PER_M3=18.50
DEFAULT_CURRENCY=MXN
```

O para PostgreSQL:
```env
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/servitab_water
```

---

## 🐳 Despliegue con Docker y Gunicorn

El sistema está listo para ejecutarse en entornos contenerizados con servidores WSGI de grado de producción:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

---

## 📄 Licencia

Propiedad de **SERVITAB S.A. de C.V.** - Villahermosa, Tabasco. Todos los derechos reservados.
