import time
from src.database import FinancialDB
from src.ingestion import FinancialFeed
from src.processing import DataProcessor

def run_pipeline():
    # 1. Inicializar los tres componentes del sistema
    db = FinancialDB()
    feed = FinancialFeed()
    processor = DataProcessor()

    print("\n[SISTEMA] Pipeline de DataOps iniciado. Presiona Ctrl+C para detenerlo.\n")

    # 2. Bucle de ejecución continua (Simulación en Tiempo Real)
    while True:
        try:
            # CAPA DE INGESTA: Intentamos traer un tick del exterior
            raw_tick = feed.generate_tick()
            
            # CAPA DE PROCESAMIENTO: Validamos y rellenamos nulos si aplica
            processed_tick = processor.process_raw_tick(raw_tick)
            
            # Si el procesador no descartó el registro, lo guardamos
            if processed_tick:
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO market_feeds (timestamp, ticker, price, volume, is_imputed)
                        VALUES (?, ?, ?, ?, ?);
                        """,
                        (
                            processed_tick["timestamp"],
                            processed_tick["ticker"],
                            processed_tick["price"],
                            processed_tick["volume"],
                            processed_tick["is_imputed"]
                        )
                    )
                    conn.commit()
                print(f"[BASE DE DATOS] ✅ Registro guardado exitosamente.")
        
        except ConnectionError as e:
            # AQUÍ SE LOGRA LA RESILIENCIA: El corte de red se atrapa.
            # El programa NO se muere, simplemente duerme un momento y vuelve a intentar.
            print(f"[SISTEMA] 🚨 Mitigación de Red Activada: {e} Reintentando en 3 segundos...")
            time.sleep(3)
        
        except Exception as e:
            # Atrapamos cualquier otro error inesperado para evitar caídas catastróficas
            print(f"[SISTEMA] 💥 Error inesperado en el loop: {e}")
        
        # Una pequeña pausa de 1 segundo entre ticks para poder leer la pantalla
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        print("\n[SISTEMA] Pipeline detenido manualmente por el usuario. Limpieza completada.")