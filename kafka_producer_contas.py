"""Kafka Producer for Contas Pagar (Accounts Payable)."""
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from kafka import KafkaProducer


DEFAULT_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
DEFAULT_TOPIC = os.getenv('KAFKA_TOPIC_CONTAS_PAGAR', 'contas-pagar-topic')


@dataclass
class ContasPagar:
    """Data model for Contas Pagar (Accounts Payable)"""
    id: int
    centro_custo_id: int
    valor_previsto: float
    valor_pago: Optional[float]
    data: str  # ISO format: YYYY-MM-DD
    status: str  # e.g., 'pendente', 'pago', 'vencido'
    usuario: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


class KafkaProducerContasPagar:
    """Kafka Producer for Contas Pagar messages"""
    
    def __init__(
        self,
        bootstrap_servers: Optional[str] = None,
        topic: Optional[str] = None
    ):
        """
        Initialize Kafka Producer
        
        Args:
            bootstrap_servers: Kafka broker address
            topic: Topic name for publishing messages
        """
        bootstrap_servers = bootstrap_servers or DEFAULT_BOOTSTRAP_SERVERS
        self.topic = topic or DEFAULT_TOPIC
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,
            compression_type='gzip'
        )
    
    def publish(self, conta: ContasPagar) -> bool:
        """
        Publish a single Conta Pagar message to Kafka
        
        Args:
            conta: ContasPagar object to publish
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use conta.id as the message key for partitioning
            future = self.producer.send(
                self.topic,
                key=conta.id,
                value=conta.to_dict()
            )
            
            # Block until message is sent
            record_metadata = future.get(timeout=10)
            
            print(f"✓ Message sent successfully to {record_metadata.topic} "
                  f"[partition: {record_metadata.partition}, "
                  f"offset: {record_metadata.offset}]")
            
            return True
            
        except Exception as e:
            print(f"✗ Error publishing message: {str(e)}")
            return False
    
    def publish_batch(self, contas: List[ContasPagar]) -> tuple:
        """
        Publish multiple Contas Pagar messages to Kafka
        
        Args:
            contas: List of ContasPagar objects to publish
            
        Returns:
            tuple: (success_count, failure_count)
        """
        success_count = 0
        failure_count = 0
        
        for conta in contas:
            if self.publish(conta):
                success_count += 1
            else:
                failure_count += 1
        
        return success_count, failure_count
    
    def close(self):
        """Close the producer and flush pending messages"""
        try:
            self.producer.flush()
            self.producer.close()
            print("✓ Producer closed successfully")
        except Exception as e:
            print(f"✗ Error closing producer: {str(e)}")


# Lambda-style handler function
def handler(event: dict) -> dict:
    """
    Lambda-style handler for processing Contas Pagar events
    
    Args:
        event: Dictionary containing conta data
        
    Returns:
        dict: Response with status and message
    """
    try:
        # Create ContasPagar object from event
        conta = ContasPagar(**event)
        
        # Initialize producer
        producer = KafkaProducerContasPagar()
        
        # Publish message
        success = producer.publish(conta)
        
        # Close producer
        producer.close()
        
        if success:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Conta published successfully',
                    'conta_id': conta.id
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Failed to publish conta'
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error: {str(e)}'
            })
        }


if __name__ == "__main__":
    # Example usage
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
