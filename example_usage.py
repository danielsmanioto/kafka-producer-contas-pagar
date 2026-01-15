"""
Example usage script for Kafka Producer - Contas Pagar

This script demonstrates different ways to use the Kafka producer
"""
from datetime import datetime, timedelta
from kafka_producer_contas import ContasPagar, KafkaProducerContasPagar, handler


def example_1_simple_publish():
    """Example 1: Simple single message publish"""
    print("\n=== Example 1: Simple Single Message ===")
    
    conta = ContasPagar(
        id=1000,
        centro_custo_id=100,
        valor_previsto=1500.00,
        valor_pago=1500.00,
        data=datetime.now().strftime('%Y-%m-%d'),
        status='pago',
        usuario='admin'
    )
    
    producer = KafkaProducerContasPagar()
    producer.publish(conta)
    producer.close()


def example_2_batch_publish():
    """Example 2: Batch publish multiple messages"""
    print("\n=== Example 2: Batch Publish ===")
    
    contas = [
        ContasPagar(
            id=2000,
            centro_custo_id=200,
            valor_previsto=5000.00,
            valor_pago=None,
            data=datetime.now().strftime('%Y-%m-%d'),
            status='pendente',
            usuario='financeiro'
        ),
        ContasPagar(
            id=2001,
            centro_custo_id=201,
            valor_previsto=3500.00,
            valor_pago=3500.00,
            data=(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            status='pago',
            usuario='admin'
        ),
        ContasPagar(
            id=2002,
            centro_custo_id=202,
            valor_previsto=2000.00,
            valor_pago=None,
            data=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            status='vencido',
            usuario='gerente'
        ),
    ]
    
    producer = KafkaProducerContasPagar()
    success, failed = producer.publish_batch(contas)
    print(f"\nBatch result: {success} successful, {failed} failed")
    producer.close()


def example_3_lambda_handler():
    """Example 3: Using lambda-style handler"""
    print("\n=== Example 3: Lambda Handler ===")
    
    event = {
        'id': 3000,
        'centro_custo_id': 300,
        'valor_previsto': 7500.00,
        'valor_pago': 5000.00,
        'data': datetime.now().strftime('%Y-%m-%d'),
        'status': 'pendente',
        'usuario': 'supervisor'
    }
    
    response = handler(event)
    print(f"Response: {response}")


def example_4_custom_configuration():
    """Example 4: Custom Kafka configuration"""
    print("\n=== Example 4: Custom Configuration ===")
    
    # You can customize the Kafka connection
    producer = KafkaProducerContasPagar(
        bootstrap_servers='localhost:9092',  # Custom server
        topic='contas-pagar'                  # Custom topic
    )
    
    conta = ContasPagar(
        id=4000,
        centro_custo_id=400,
        valor_previsto=10000.00,
        valor_pago=10000.00,
        data=datetime.now().strftime('%Y-%m-%d'),
        status='pago',
        usuario='diretor'
    )
    
    producer.publish(conta)
    producer.close()


if __name__ == "__main__":
    print("╔═════════════════════════════════════════════════════════╗")
    print("║  Kafka Producer - Contas Pagar - Usage Examples        ║")
    print("╚═════════════════════════════════════════════════════════╝")
    
    try:
        example_1_simple_publish()
        example_2_batch_publish()
        example_3_lambda_handler()
        example_4_custom_configuration()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
