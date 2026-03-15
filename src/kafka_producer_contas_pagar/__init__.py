"""Public API for kafka_producer_contas_pagar package."""

from .producer import (
    ContasPagar,
    KafkaProducerContasPagar,
    handler,
    DEFAULT_BOOTSTRAP_SERVERS,
    DEFAULT_TOPIC,
)

__all__ = [
    "ContasPagar",
    "KafkaProducerContasPagar",
    "handler",
    "DEFAULT_BOOTSTRAP_SERVERS",
    "DEFAULT_TOPIC",
]
