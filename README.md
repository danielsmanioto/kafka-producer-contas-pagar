# Kafka Producer - Contas Pagar

Kafka Producer para gerenciamento de Contas a Pagar (Accounts Payable) - Projeto de gerenciamento pessoal financeiro.

## 📋 Descrição

Este projeto implementa um produtor Kafka em Python para publicar mensagens de contas a pagar em uma fila Kafka. O código foi desenvolvido com arquitetura limpa, estilo lambda, e inclui classes de teste para inserir múltiplas mensagens.

## 🏗️ Estrutura do Projeto

```
kafka-producer-contas-pagar/
├── docker-compose.yml          # Infraestrutura Kafka + Zookeeper
├── kafka_producer_contas.py    # Produtor Kafka principal (estilo lambda)
├── test_kafka_producer.py      # Classe de testes para múltiplas mensagens
├── requirements.txt            # Dependências Python
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

## 📊 Modelo de Dados - ContasPagar

```python
@dataclass
class ContasPagar:
    id: int                      # ID único da conta
    centro_custo_id: int         # ID do centro de custo
    valor_previsto: float        # Valor previsto/orçado
    valor_pago: Optional[float]  # Valor efetivamente pago (None se pendente)
    data: str                    # Data no formato YYYY-MM-DD
    status: str                  # Status: 'pendente', 'pago', 'vencido', 'cancelado'
    usuario: str                 # Usuário responsável
```

## 🚀 Como Usar

### 1️⃣ Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.7+ instalado

### 2️⃣ Subir a Infraestrutura Kafka

```bash
# Iniciar Kafka e Zookeeper
docker-compose up -d

# Verificar se os containers estão rodando
docker-compose ps

# Ver logs (opcional)
docker-compose logs -f kafka
```

### 3️⃣ Instalar Dependências Python

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 4️⃣ Executar o Produtor

**Exemplo básico:**
```bash
python kafka_producer_contas.py
```

**Usar como módulo Python:**
```python
from kafka_producer_contas import ContasPagar, KafkaProducerContasPagar
from datetime import datetime

# Criar uma conta
conta = ContasPagar(
    id=1,
    centro_custo_id=100,
    valor_previsto=1500.00,
    valor_pago=1500.00,
    data=datetime.now().strftime('%Y-%m-%d'),
    status='pago',
    usuario='admin'
)

# Publicar no Kafka
producer = KafkaProducerContasPagar()
producer.publish(conta)
producer.close()
```

**Usar como Lambda Handler:**
```python
from kafka_producer_contas import handler

# Simular evento
event = {
    'id': 1,
    'centro_custo_id': 100,
    'valor_previsto': 1500.00,
    'valor_pago': 1500.00,
    'data': '2026-01-15',
    'status': 'pago',
    'usuario': 'admin'
}

# Processar
response = handler(event)
print(response)
```

### 5️⃣ Executar Testes

```bash
# Executar todos os testes
python test_kafka_producer.py
```

Os testes incluem:
- ✅ Envio de mensagem única
- ✅ Envio de múltiplas mensagens aleatórias (10 por padrão)
- ✅ Cenários específicos de negócio (pendente, pago, vencido)

**Personalizar quantidade de mensagens:**
```python
from test_kafka_producer import TestKafkaProducerContasPagar

test = TestKafkaProducerContasPagar()
test.test_send_multiple_messages(count=100)  # Enviar 100 mensagens
test.close()
```

## 🛠️ Configuração

### Kafka Settings

Por padrão, o produtor conecta em `localhost:9092` e publica no tópico `contas-pagar`.

Para alterar:
```python
producer = KafkaProducerContasPagar(
    bootstrap_servers='seu-servidor:9092',
    topic='seu-topico'
)
```

### Docker Compose

O arquivo `docker-compose.yml` configura:
- **Zookeeper** na porta `2181`
- **Kafka** nas portas `9092` (externa) e `9093` (interna)

## 📦 Características

- ✨ **Código Limpo**: Arquitetura estilo lambda, fácil de entender e manter
- 🔄 **Batch Processing**: Suporte para envio em lote de múltiplas mensagens
- 🔑 **Particionamento**: Usa o ID da conta como chave para particionamento
- 🗜️ **Compressão**: Mensagens comprimidas com gzip
- ✅ **Confiabilidade**: Configurado com `acks='all'` e retries
- 🧪 **Testes**: Classe completa de testes com cenários aleatórios e específicos

## 🐛 Troubleshooting

**Kafka não conecta:**
```bash
# Verificar se o Kafka está rodando
docker-compose ps

# Reiniciar containers
docker-compose restart

# Ver logs de erro
docker-compose logs kafka
```

**Erro de conexão recusada:**
- Aguarde alguns segundos após iniciar o Kafka (ele leva um tempo para ficar pronto)
- Verifique se as portas 2181 e 9092 não estão sendo usadas por outros processos

## 🛑 Parar a Infraestrutura

```bash
# Parar containers
docker-compose down

# Parar e remover volumes (apaga dados)
docker-compose down -v
```

## 📝 Licença

Este é um projeto pessoal de gerenciamento financeiro.

## 👨‍💻 Autor

Daniel Smanioto
