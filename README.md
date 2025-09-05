# Calculadora de nota GS - Docker Compose Migration

## 📋 Análise do Projeto

### Arquitetura Atual (Antes)
```
┌─────────────────┐
│   Python App    │ ← Execução local
│   (main.py)     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   SQLite DB     │ ← Arquivo local
│ grade_calc.db   │
└─────────────────┘
```

### Arquitetura Futura (Depois)
```
┌─────────────────────────────────┐
│         Docker Host             │
│  ┌─────────────────┐            │
│  │  FastAPI App    │◄───────────┼─── http://localhost:8000
│  │  (Container)    │            │
│  └─────────────────┘            │
│           │                     │
│           ▼                     │
│  ┌─────────────────┐            │
│  │   SQLite DB     │            │
│  │   (Volume)      │            │
│  └─────────────────┘            │
│                                 │
│  ┌─────────────────┐            │
│  │  DB Initializer │            │
│  │  (Container)    │            │
│  └─────────────────┘            │
└─────────────────────────────────┘
```

## 🏗️ Componentes Identificados

### Serviços:
1. **app**: Aplicação FastAPI principal
2. **database**: Inicializador do banco de dados

### Dependências:
- `app` depende de `database` (banco deve ser inicializado primeiro)

### Estratégia de Containerização:
- **App**: Container Python com FastAPI + dependências
- **Database**: Container Python para inicializar SQLite
- **Ambos**: Usam imagem oficial `python:3.11-slim`

## 🚀 Implementação Docker Compose

### Recursos Implementados:

#### ✅ Definição dos Serviços (0,8 pontos)
- 2 serviços: `app`, `database`
- Cada serviço com configuração específica

#### ✅ Configuração de Redes (0,8 pontos)
- Rede customizada `fiap-network` tipo bridge
- Comunicação interna entre containers

#### ✅ Gerenciamento de Volumes (0,8 pontos)
- Volume `./data` para persistência do SQLite

#### ✅ Variáveis de Ambiente (0,8 pontos)
- `DATABASE_URL`: Caminho do banco de dados
- `APP_ENV`: Ambiente da aplicação

#### ✅ Políticas de Restart (0,8 pontos)
- `unless-stopped`: Para serviços principais
- `no`: Para inicializador (executa uma vez)

#### ✅ Exposição de Portas (0,8 pontos)
- Porta 8000: Aplicação FastAPI

#### ✅ Health Checks (0,9 pontos)
- Health check HTTP para aplicação
- Configuração de intervalos e timeouts

#### ✅ Usuário Sem Privilégios (0,8 pontos)
- Usuário `appuser` para aplicação
- Usuário `dbuser` para inicializador

## 📖 Instruções de Uso

### Pré-requisitos
- Docker Engine instalado
- Docker Compose instalado

### Comandos Essenciais

#### Iniciar todos os serviços:
```bash
docker-compose up -d
```

#### Ver logs em tempo real:
```bash
docker-compose logs -f
```

#### Parar todos os serviços:
```bash
docker-compose down
```

#### Rebuild e restart:
```bash
docker-compose up --build -d
```

#### Verificar status dos containers:
```bash
docker-compose ps
```

## 🔧 Processo de Deploy

### Passo a Passo:

1. **Preparação**
   ```bash
   git clone <repository>
   cd Calculadora-de-nota-necessaria-na-GS
   ```

2. **Build e Deploy**
   ```bash
   docker-compose up --build -d
   ```

3. **Verificação**
   ```bash
   # Verificar containers
   docker-compose ps
   
   # Testar aplicação
   curl http://localhost/
   
   # Testar cálculo
   curl -X POST http://localhost/calculate \
        -H "Content-Type: application/json" \
        -d '{"nota_1s": 8.0, "nota_cp_2s": 7.5, "meta_anual": 8.5}'
   ```

4. **Verificar Banco de Dados**
   ```bash
   # Entrar no container
   docker exec -it fiap-grade-calculator bash
   
   # Verificar banco
   sqlite3 /app/data/grade_calculator.db "SELECT * FROM grade_calculations;"
   ```

## 🔍 Troubleshooting

### Problema: Container não inicia
**Solução:**
```bash
docker-compose logs <service-name>
docker-compose down && docker-compose up --build
```

### Problema: Banco de dados não persiste
**Solução:**
```bash
# Verificar volume
docker volume ls
docker-compose down -v  # Remove volumes
docker-compose up -d    # Recria
```

### Problema: Aplicação não responde
**Solução:**
```bash
# Verificar health check
docker-compose ps
# Verificar logs
docker-compose logs app
```

### Problema: Aplicação não responde na porta 8000
**Solução:**
```bash
# Verificar se container está rodando
docker-compose ps
# Verificar logs da aplicação
docker-compose logs app
```

## 🧪 Testes Completos

### 1. Teste de Conectividade
```bash
curl http://localhost:8000/
# Esperado: {"message": "FIAP Grade Calculator API"}
```

### 2. Teste de Cálculo (CREATE)
```bash
curl -X POST http://localhost:8000/calculate \
     -H "Content-Type: application/json" \
     -d '{
       "nota_1s": 8.0,
       "nota_cp_2s": 7.5,
       "meta_anual": 8.5,
       "materia": "Docker Test"
     }'
```

### 3. Teste de Listagem (READ)
```bash
curl http://localhost:8000/calculations
```

### 4. Teste de Busca por ID (READ)
```bash
curl http://localhost:8000/calculations/1
```

### 5. Verificação do Banco
```bash
docker exec -it fiap-calculator-app sqlite3 /app/data/grade_calculator.db \
    "SELECT id, nota_1s, nota_cp_2s, meta_anual, nota_necessaria_gs, materia FROM grade_calculations;"
```

## 📊 Monitoramento

### Health Checks Disponíveis:
- **Aplicação**: `http://localhost:8000/`

### Logs:
```bash
# Todos os serviços
docker-compose logs

# Serviço específico
docker-compose logs app
```

## 🎯 Benefícios Alcançados

- ✅ **Orquestração automatizada**: Docker Compose gerencia todos os serviços
- ✅ **Escalabilidade**: Fácil replicação e scaling
- ✅ **Ambientes padronizados**: Mesmo ambiente em dev/test/prod
- ✅ **Deploy contínuo**: Comandos simples para deploy
- ✅ **Melhor utilização de recursos**: Containers otimizados

## 📹 Evidências para Vídeo

### Roteiro de Demonstração:
1. Mostrar arquivos do projeto
2. Executar `docker-compose up -d`
3. Verificar containers com `docker-compose ps`
4. Testar endpoint raiz
5. Fazer cálculo via POST
6. Listar todos os cálculos
7. Buscar cálculo específico
8. Entrar no container e verificar banco SQLite
9. Mostrar logs dos serviços
10. Demonstrar health checks
