"""Compatibility wrapper for legacy imports.

Core code now lives under src/kafka_producer_contas_pagar.
"""

import sys
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from kafka_producer_contas_pagar import ContasPagar, KafkaProducerContasPagar, handler


if __name__ == "__main__":
    # Example usage (kept for backward compatibility)
    example_conta = ContasPagar(
        id=1,
        centro_custo_id=100,
        valor_previsto=1500.00,
        valor_pago=1500.00,
        data=datetime.now().strftime('%Y-%m-%d'),
        status='pago',
        usuario='admin'
    )
    
    producer = KafkaProducerContasPagar()
    producer.publish(example_conta)
    producer.close()
