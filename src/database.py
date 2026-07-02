import sqlite3
import os

class FinancialDB:
    def __init__(self, db_path="data/fintech_core.db"):
        """
        Paso 1: El constructor (__init__). 
        Define dónde se guardará físicamente el archivo de la base de datos.
        """
        self.db_path = db_path
        # Esta línea asegura que la carpeta 'data/' se cree automáticamente si no existe.
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # Ejecutamos la creación de las tablas de inmediato al inicializar el objeto.
        self.init_db()

    def get_connection(self):
        """
        Paso 2: Método para conectar.
        Cada vez que queramos escribir o leer, abriremos un puente temporal con este método.
        """
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """
        Paso 3: Estructuración física de las columnas (Esquema SQL).
        Aquí combatimos la corrupción de datos definiendo tipos estrictos (TEXT, REAL).
        """
        query = """
        CREATE TABLE IF NOT EXISTS market_feeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ticker TEXT NOT NULL,
            price REAL NOT NULL,
            volume REAL NOT NULL,
            is_imputed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        # El bloque 'with' abre el puente y lo cierra automáticamente para evitar que el archivo se bloquee.
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            
            # PASO CLAVE INDUSTRIAL: El Índice.
            # En finanzas, buscar registros fila por fila es lento. Un índice en el Ticker y Tiempo 
            # hace que las consultas pasen de tardar segundos a milisegundos.
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticker_timestamp ON market_feeds (ticker, timestamp);")
            conn.commit()
            print("[INFO] Base de datos relacional indexada y lista de forma local.")