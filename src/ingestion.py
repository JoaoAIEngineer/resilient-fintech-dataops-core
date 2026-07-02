import random
import time
from datetime import datetime

class FinancialFeed:
    def __init__(self):
        # Definimos algunos tickers (identificadores de activos financieros) para simular
        self.tickers = ["BTC/USD", "ETH/USD", "SOL/USD", "AAPL", "TSLA"]

    def generate_tick(self):
        """
        Genera un solo registro de mercado (tick).
        A propósito, introducirá fallos aleatorios en el precio o simulará cortes de red.
        """
        # 1. Probabilidad del 10% de simular una caída total de red (Excepción)
        if random.random() < 0.10:
            raise ConnectionError("Fallo crítico de red: El servidor remoto no responde.")

        ticker = random.choice(self.tickers)
        timestamp = datetime.utcnow().isoformat()
        volume = round(random.uniform(10, 500), 2)
        
        # 2. Probabilidad del 15% de enviar un precio corrupto (None)
        if random.random() < 0.15:
            price = None
            print(f"[INGESTA] ⚠️ Alerta: Generando tick corrupto para {ticker} (Precio Nulo).")
        else:
            # Precio normal simulado basado en el activo
            price = round(random.uniform(50, 60000) if "BTC" in ticker else random.uniform(10, 3000), 2)
            print(f"[INGESTA] Generando tick limpio: {ticker} a ${price}")

        return {
            "timestamp": timestamp,
            "ticker": ticker,
            "price": price,
            "volume": volume
        }