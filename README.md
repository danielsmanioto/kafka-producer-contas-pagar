# Kafka Producer - Contas Pagar

> Produtor Kafka em Python para publicação de eventos financeiros no tópico `contas-pagar-topic`.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Kafka](https://img.shields.io/badge/Apache-Kafka-231F20?logo=apachekafka&logoColor=white)](https://kafka.apache.org/)
[![Status](https://img.shields.io/badge/Producer-Ativo-success)](#)

---

## 📑 Sumário

- [Visão geral](#-visão-geral)
- [Infraestrutura oficial](#-infraestrutura-oficial)
- [Como executar](#-como-executar)
- [Configuração](#-configuração)
- [Modelo de dados](#-modelo-de-dados)
- [Testes](#-testes)
- [Troubleshooting](#-troubleshooting)

---

## 🌐 Visão geral

Este projeto publica mensagens de contas a pagar para processamento assíncrono pelo consumer Java da solução.

## 🔗 Infraestrutura oficial

Este repositório **não possui mais infraestrutura própria**. Utilize:

- [danielsmanioto/infra-gerenciador-pessoal](https://github.com/danielsmanioto/infra-gerenciador-pessoal)

## 🚀 Como executar

### 1) Pré-requisitos

- Python 3.9+
- Docker e Docker Compose

### 2) Subir infraestrutura centralizada

```bash
git clone https://github.com/danielsmanioto/infra-gerenciador-pessoal.git
cd infra-gerenciador-pessoal
docker compose up -d
```

### 3) Instalar dependências

```bash
cd ../kafka-producer-contas-pagar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4) Executar producer

```bash
python kafka_producer_contas.py
```

## ⚙️ Configuração

Variáveis suportadas:

```bash
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export KAFKA_TOPIC_CONTAS_PAGAR=contas-pagar-topic
```

Também pode ser configurado no código:

```python
producer = KafkaProducerContasPagar(
    bootstrap_servers='localhost:9092',
    topic='contas-pagar-topic'
)
```

## 📊 Modelo de dados

```python
@dataclass
class ContasPagar:
    id: int
    centro_custo_id: int
    valor_previsto: float
    valor_pago: Optional[float]
    data: str
    status: str
    usuario: str
```

## 🧪 Testes

```bash
python test_kafka_producer.py
```

Cobertura principal:

- envio unitário
- envio em lote
- cenários de negócio

## 🐛 Troubleshooting

Se houver erro de conexão com Kafka:

```bash
cd ../infra-gerenciador-pessoal
docker compose ps
docker compose logs -f kafka
```

## 📝 Licença

Projeto pessoal para estudo e evolução arquitetural.
