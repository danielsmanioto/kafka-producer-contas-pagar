"""Test class for Kafka Producer - Contas Pagar."""

import os
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from kafka_producer_contas_pagar import ContasPagar, KafkaProducerContasPagar


class TestKafkaProducerContasPagar:
    """Test class for sending multiple messages to Kafka."""

    def __init__(self, bootstrap_servers: str = None):
        bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = KafkaProducerContasPagar(bootstrap_servers=bootstrap_servers)
        self.usuarios = ["admin", "financeiro", "gerente", "supervisor", "operador"]
        self.status_list = ["pendente", "pago", "vencido", "cancelado"]

    def generate_random_conta(self, id: int = None) -> ContasPagar:
        if id is None:
            id = int(time.time() * 1000000)

        days_ago = random.randint(0, 90)
        data = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        valor_previsto = round(random.uniform(100.0, 10000.0), 2)
        status = random.choice(self.status_list)

        if status == "pago":
            valor_pago = valor_previsto
        elif status == "pendente":
            valor_pago = None
        else:
            valor_pago = round(random.uniform(0, valor_previsto), 2) if random.random() > 0.5 else None

        return ContasPagar(
            id=id,
            centro_custo_id=random.randint(100, 500),
            valor_previsto=valor_previsto,
            valor_pago=valor_pago,
            data=data,
            status=status,
            usuario=random.choice(self.usuarios),
        )

    def test_send_single_message(self):
        print("\n=== Testing Single Message ===")
        conta = ContasPagar(
            id=1,
            centro_custo_id=100,
            valor_previsto=1500.00,
            valor_pago=1500.00,
            data=datetime.now().strftime("%Y-%m-%d"),
            status="pago",
            usuario="admin",
        )

        success = self.producer.publish(conta)
        print(f"Result: {'Success' if success else 'Failed'}")
        return success

    def test_send_multiple_messages(self, count: int = 10):
        print(f"\n=== Testing {count} Random Messages ===")

        base_id = int(time.time() * 1000)
        contas = [self.generate_random_conta(base_id + i) for i in range(count)]

        success_count, failure_count = self.producer.publish_batch(contas)

        print("\n--- Results ---")
        print(f"Total messages: {count}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failure_count}")
        print(f"Success rate: {(success_count / count) * 100:.1f}%")

        return success_count, failure_count

    def test_send_specific_scenarios(self):
        print("\n=== Testing Specific Scenarios ===")

        base_id = int(time.time() * 1000) + 1000000

        scenarios = [
            ContasPagar(
                id=base_id + 1,
                centro_custo_id=200,
                valor_previsto=5000.00,
                valor_pago=None,
                data=datetime.now().strftime("%Y-%m-%d"),
                status="pendente",
                usuario="financeiro",
            ),
            ContasPagar(
                id=base_id + 2,
                centro_custo_id=200,
                valor_previsto=3000.00,
                valor_pago=3000.00,
                data=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                status="pago",
                usuario="admin",
            ),
            ContasPagar(
                id=base_id + 3,
                centro_custo_id=300,
                valor_previsto=2500.00,
                valor_pago=None,
                data=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                status="vencido",
                usuario="gerente",
            ),
            ContasPagar(
                id=base_id + 4,
                centro_custo_id=150,
                valor_previsto=7500.00,
                valor_pago=5000.00,
                data=datetime.now().strftime("%Y-%m-%d"),
                status="pendente",
                usuario="supervisor",
            ),
        ]

        success_count, failure_count = self.producer.publish_batch(scenarios)

        print("\n--- Results ---")
        print(f"Scenarios tested: {len(scenarios)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failure_count}")

        return success_count, failure_count

    def close(self):
        self.producer.close()


def run_all_tests():
    print("╔════════════════════════════════════════════════════════╗")
    print("║  Kafka Producer - Contas Pagar - Test Suite          ║")
    print("╚════════════════════════════════════════════════════════╝")

    test = TestKafkaProducerContasPagar()

    try:
        test.test_send_single_message()
        test.test_send_multiple_messages(count=10)
        test.test_send_specific_scenarios()

        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during tests: {str(e)}")
    finally:
        test.close()


if __name__ == "__main__":
    run_all_tests()
