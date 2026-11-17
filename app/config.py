import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey_servitab_villahermosa_2026")

    # Identidad Corporativa (Giro Privado: SERVITAB - Villahermosa, Tabasco)
    REGION_NAME = os.environ.get("REGION_NAME", "Villahermosa, Tabasco")
    ORGANIZATION_NAME = os.environ.get("ORGANIZATION_NAME", "SERVITAB S.A. de C.V. - Servicios y Suministros de Agua")
    DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "MXN")
    DEFAULT_CURRENCY_SYMBOL = os.environ.get("DEFAULT_CURRENCY_SYMBOL", "$")
    # Tarifa base comercial/privada en Pesos Mexicanos (MXN / m3)
    WATER_RATE_PER_M3 = float(os.environ.get("WATER_RATE_PER_M3", 18.50))

    # Base de datos: Soporte híbrido SQLite (desarrollo/evaluación) y MySQL / PostgreSQL (producción)
    DATABASE_URL = os.environ.get("DATABASE_URL")
    USE_MYSQL = os.environ.get("USE_MYSQL", "false").lower() in ("true", "1", "yes")

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "servitab_water")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif USE_MYSQL:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        )
    else:
        # SQLite por defecto para desarrollo local
        instance_dir = os.path.join(BASE_DIR, "instance")
        os.makedirs(instance_dir, exist_ok=True)
        sqlite_path = os.path.join(instance_dir, "servitab_water.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optimización de conexión a base de datos (Pool de conexiones y auto-reconect)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,       # Recicla conexiones para evitar timeouts en MySQL / Cloud SQL
        "pool_pre_ping": True,     # Pre-ping para reconectar automáticamente ante caídas
    }
