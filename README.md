# Kafka Producer - Contas Pagar

Produtor Kafka em Python para publicação de eventos de contas a pagar no tópico `contas-pagar-topic`.

## 📋 Descrição

Este projeto publica mensagens no ecossistema do Gerenciador Pessoal e foi ajustado para usar a infraestrutura centralizada do repositório `infra-gerenciador-pessoal`.

## 🔗 Infraestrutura oficial

Este projeto **não mantém mais infraestrutura própria**.

Toda a infraestrutura local foi centralizada em:

- [danielsmanioto/infra-gerenciador-pessoal](https://github.com/danielsmanioto/infra-gerenciador-pessoal)

## 🚀 Como usar

### 1. Pré-requisitos

- Python 3.9+
- Docker e Docker Compose

### 2. Suba a infraestrutura centralizada

```bash
git clone https://github.com/danielsmanioto/infra-gerenciador-pessoal.git
cd infra-gerenciador-pessoal
docker compose up -d
```

### 3. Instale as dependências

```bash
cd ../kafka-producer-contas-pagar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Execute o produtor

```bash
python kafka_producer_contas.py
```

## ⚙️ Configuração

O produtor usa variáveis de ambiente com fallback local:

```bash
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export KAFKA_TOPIC_CONTAS_PAGAR=contas-pagar-topic
```

Ou via código:

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

Os testes cobrem:

- ✅ Envio de mensagem única
- ✅ Envio de múltiplas mensagens
- ✅ Cenários de negócio

## 📦 Características

- ✨ Código simples e reutilizável
- 🔄 Publicação em lote
- 🔑 Chave por ID da conta
- 🗜️ Compressão gzip
- ✅ `acks='all'` e retry habilitado

## 🐛 Troubleshooting

Se o Kafka não conectar:

```bash
cd ../infra-gerenciador-pessoal
docker compose ps
docker compose logs -f kafka
```

## 📝 Licença

Este é um projeto pessoal de gerenciamento financeiro.

## 👨‍💻 Autor

Daniel Smanioto
