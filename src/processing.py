import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional

# ==========================================
# CAPA 1: Esquema de Validación (Pydantic)
# ==========================================
class MarketTickSchema(BaseModel):
    """
    Define exactamente cómo DEBE verse un tick financiero.
    Si algo no cumple con esto, Pydantic lanzará un error estructurado.
    """
    timestamp: str
    ticker: str
    # Permitimos que price sea un float o un None (opcional) para procesarlo después
    price: Optional[float] = None 
    volume: float

# ==========================================
# CAPA 2: Motor de Procesamiento (Pandas)
# ==========================================
class DataProcessor:
    def __init__(self):
        # Mantenemos un histórico en memoria de los últimos precios válidos por ticker
        # Esto nos permite hacer el Forward Fill controlado entre diferentes ráfagas de datos
        self.last_known_prices = {}

    def process_raw_tick(self, raw_data: dict) -> dict:
        """
        Toma un diccionario crudo de la calle, lo valida y arregla si es necesario.
        """
        # 1. Validar la estructura inicial con Pydantic
        tick = MarketTickSchema(**raw_data)
        
        processed_tick = tick.model_dump()
        processed_tick["is_imputed"] = 0  # Bandera por defecto: No alterado

        # 2. Control de Datos Corruptos (Manejo de Nulos Financieros)
        if processed_tick["price"] is None:
            ticker = processed_tick["ticker"]
            
            # Si tenemos un registro guardado del precio anterior de este activo, lo usamos
            if ticker in self.last_known_prices:
                processed_tick["price"] = self.last_known_prices[ticker]
                processed_tick["is_imputed"] = 1  # Encendemos la bandera de advertencia
                print(f"[PROCESADOR] 🛠️ Dato imputado para {ticker} usando Forward Fill: ${processed_tick['price']}")
            else:
                # Si es el primer tick del programa y vino nulo, no hay historial; lo descartamos por seguridad
                print(f"[PROCESADOR] ❌ Descartando tick de {ticker}: Precio nulo sin historial previo.")
                return None
        else:
            # Si el precio vino limpio de la calle, actualizamos nuestra memoria histórica
            self.last_known_prices[processed_tick["ticker"]] = processed_tick["price"]

        return processed_tick