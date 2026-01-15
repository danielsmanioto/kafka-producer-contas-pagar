"""
Test class for Kafka Producer - Contas Pagar
Classe de teste para inserir várias mensagens no Kafka
"""
import random
from datetime import datetime, timedelta
from kafka_producer_contas import ContasPagar, KafkaProducerContasPagar


class TestKafkaProducerContasPagar:
    """Test class for sending multiple messages to Kafka"""
    
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        """
        Initialize test class
        
        Args:
            bootstrap_servers: Kafka broker address
        """
        self.producer = KafkaProducerContasPagar(bootstrap_servers=bootstrap_servers)
        self.usuarios = ['admin', 'financeiro', 'gerente', 'supervisor', 'operador']
        self.status_list = ['pendente', 'pago', 'vencido', 'cancelado']
    
    def generate_random_conta(self, id: int) -> ContasPagar:
        """
        Generate a random ContasPagar object for testing
        
        Args:
            id: Unique ID for the conta
            
        Returns:
            ContasPagar: Random conta object
        """
        # Random date in the last 90 days
        days_ago = random.randint(0, 90)
        data = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Random values
        valor_previsto = round(random.uniform(100.0, 10000.0), 2)
        status = random.choice(self.status_list)
        
        # If status is 'pago', set valor_pago, otherwise it may be None or partial
        if status == 'pago':
            valor_pago = valor_previsto
        elif status == 'pendente':
            valor_pago = None
        else:
            # Partial payment or full payment
            valor_pago = round(random.uniform(0, valor_previsto), 2) if random.random() > 0.5 else None
        
        return ContasPagar(
            id=id,
            centro_custo_id=random.randint(100, 500),
            valor_previsto=valor_previsto,
            valor_pago=valor_pago,
            data=data,
            status=status,
            usuario=random.choice(self.usuarios)
        )
    
    def test_send_single_message(self):
        """Test sending a single message"""
        print("\n=== Testing Single Message ===")
        conta = ContasPagar(
            id=1,
            centro_custo_id=100,
            valor_previsto=1500.00,
            valor_pago=1500.00,
            data=datetime.now().strftime('%Y-%m-%d'),
            status='pago',
            usuario='admin'
        )
        
        success = self.producer.publish(conta)
        print(f"Result: {'Success' if success else 'Failed'}")
        return success
    
    def test_send_multiple_messages(self, count: int = 10):
        """
        Test sending multiple random messages
        
        Args:
            count: Number of messages to send
        """
        print(f"\n=== Testing {count} Random Messages ===")
        
        contas = [self.generate_random_conta(i + 1) for i in range(count)]
        
        success_count, failure_count = self.producer.publish_batch(contas)
        
        print(f"\n--- Results ---")
        print(f"Total messages: {count}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failure_count}")
        print(f"Success rate: {(success_count/count)*100:.1f}%")
        
        return success_count, failure_count
    
    def test_send_specific_scenarios(self):
        """Test specific business scenarios"""
        print("\n=== Testing Specific Scenarios ===")
        
        scenarios = [
            ContasPagar(
                id=101,
                centro_custo_id=200,
                valor_previsto=5000.00,
                valor_pago=None,
                data=datetime.now().strftime('%Y-%m-%d'),
                status='pendente',
                usuario='financeiro'
            ),
            ContasPagar(
                id=102,
                centro_custo_id=200,
                valor_previsto=3000.00,
                valor_pago=3000.00,
                data=(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                status='pago',
                usuario='admin'
            ),
            ContasPagar(
                id=103,
                centro_custo_id=300,
                valor_previsto=2500.00,
                valor_pago=None,
                data=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                status='vencido',
                usuario='gerente'
            ),
            ContasPagar(
                id=104,
                centro_custo_id=150,
                valor_previsto=7500.00,
                valor_pago=5000.00,
                data=datetime.now().strftime('%Y-%m-%d'),
                status='pendente',
                usuario='supervisor'
            ),
        ]
        
        success_count, failure_count = self.producer.publish_batch(scenarios)
        
        print(f"\n--- Results ---")
        print(f"Scenarios tested: {len(scenarios)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failure_count}")
        
        return success_count, failure_count
    
    def close(self):
        """Close the producer"""
        self.producer.close()


def run_all_tests():
    """Run all test scenarios"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║  Kafka Producer - Contas Pagar - Test Suite          ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    test = TestKafkaProducerContasPagar()
    
    try:
        # Test 1: Single message
        test.test_send_single_message()
        
        # Test 2: Multiple random messages
        test.test_send_multiple_messages(count=10)
        
        # Test 3: Specific scenarios
        test.test_send_specific_scenarios()
        
        print("\n" + "="*60)
        print("All tests completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error during tests: {str(e)}")
    finally:
        test.close()


if __name__ == "__main__":
    # Run all tests
    run_all_tests()
    
    # Or run individual tests:
    # test = TestKafkaProducerContasPagar()
    # test.test_send_multiple_messages(count=50)
    # test.close()
