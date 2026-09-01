# 📦 Divisor de Carga — Sistema Distribuído de Arquivos

Um **sistema de armazenamento distribuído** simples que simula o funcionamento do **HDFS (Hadoop Distributed File System)**.

Em vez de guardar um arquivo inteiro em um único lugar, o projeto **divide o arquivo em pedaços de 1MB** e os **distribui entre vários nós**, para depois baixá-los e remontar o arquivo original.

---

## 🧠 Como funciona

O fluxo segue a arquitetura clássica do Hadoop:

```
┌──────────────────────┐
│   ORCHESTRADOR       │
│  (NameNode + Cliente)│
│  ─ guarda o "mapa"   │
│    de onde cada      │
│    pedaço está       │
└──────────┬───────────┘
           │ divide em 1MB
           ▼
┌──────────────┐  ┌──────────────┐
│   NÓ 5001    │  │   NÓ 5002    │
│  (DataNode)  │  │  (DataNode)  │
│ parte_0,2,4  │  │ parte_1,3,5  │
└──────────────┘  └──────────────┘
```

- 🧩 **Orquestrador** (`orchestrador.py`) — divide o arquivo, distribui os pedaços e guarda o mapa de localização (simula o *NameNode*).
- 💾 **DataNodes** (`datanode.py`) — recebem, guardam e servem os pedaços (simulam os *DataNodes*).

Cada arquivo é cortado em blocos de **1MB** que vão sendo alternados entre os nós:

| Arquivo | Pedaço | Onde fica |
|---------|--------|-----------|
| `arquivo_gigante.txt` | `part_0`, `part_2`… | Nó 5001 |
| `arquivo_gigante.txt` | `part_1`, `part_3`… | Nó 5002 |

---

## 🛠️ Pré-requisitos

- **Python 3** instalado

### 1. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  venv\Scripts\activate
  ```

> Você verá `(venv)` no início do prompt — sinal de que o ambiente está ativo.

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Isso instala `flask` (para os nós) e `requests` (para o orquestrador) com as versões corretas.

---

## 🚀 Como usar

### 1. Suba os nós (DataNodes)

Abra **dois terminais** e rode um nó em cada porta:

**Terminal 1**
```bash
python datanode.py 5001
```

**Terminal 2**
```bash
python datanode.py 5002
```

Repare que cada nó cria a própria pasta de armazenamento (`storage_5001`, `storage_5002`).

### 2. Distribua o arquivo (upload)

No `orchestrador.py`, deixe o **upload** ativo e comente o download:

```python
fazer_upload_distribuido("arquivo_gigante.txt")
# fazer_download_e_remontar("arquivo_gigante.txt")
```

Rode o orquestrador:

```bash
python orchestrador.py
```

Isso vai:
1. Ler o arquivo em blocos de 1MB
2. Enviar cada bloco para um nó (alternando)
3. Salvar o mapa de localização em **`metadados.json`**

```
✅ Upload de 'arquivo_gigante.txt' concluído em 50 partes.
```

### 3. Baixe e remonte o arquivo (download)

Agora **comente o upload** e deixe só o download:

```python
# fazer_upload_distribuido("arquivo_gigante.txt")
fazer_download_e_remontar("arquivo_gigante.txt")
```

Rode de novo — o orquestrador **lê o `metadados.json` automaticamente**:

```bash
python orchestrador.py
```

Resultado:

```
🔄 Remontando arquivo 'arquivo_gigante.txt' a partir dos nós...
Baixando parte de: http://localhost:5001/download/arquivo_gigante_txt_part_0
...
🏁 Arquivo 'recuperado_arquivo_gigante.txt' remontado com sucesso!
```

O arquivo original é reconstruído como **`recuperado_arquivo_gigante.txt`** 🎉

> 💡 **Dica:** como o mapa fica salvo em `metadados.json`, você pode repetir o **download** quantas vezes quiser, sem precisar refazer o upload — desde que as partes ainda existam nos nós.

---

## ⚠️ Solução de problemas

| Problema | Causa provável | Solução |
|----------|---------------|---------|
| `Arquivo não encontrado nos metadados!` | O `metadados.json` ainda não existe ou o arquivo nunca foi enviado | Faça o **upload** primeiro |
| Erro de conexão no upload (`requests.exceptions.ConnectionError`) | Os nós 5001/5002 não estão rodando | Suba os DataNodes |
| `❌ Erro crítico: Falha ao baixar parte` | A parte foi apagada do nó | Refaça o upload |
| Arquivo remontado truncado | Alguma parte faltou no download | Verifique se todos os nós estão no ar |

---

## 📁 Estrutura do projeto

```
divisor_de_carga/
├── orchestrador.py       # Orquestrador (divide, distribui e remonta)
├── datanode.py           # Nó de armazenamento (HTTP Flask)
├── gerar_dados.py        # Gera o arquivo de teste grande
├── requirements.txt      # Dependências do projeto
├── .gitignore
├── metadados.json        # Mapa de onde cada pedaço está (gerado)
├── storage_5001/         # Partes guardadas no nó 5001
├── storage_5002/         # Partes guardadas no nó 5002
└── arquivo_gigante.txt   # Arquivo de exemplo
```

---

## 🎓 Conceitos de Computação Distribuída

Este projeto ilustra na prática:

- **Divisão de carga** — o trabalho de armazenar é distribuído entre várias máquinas
- **Tolerância a falhas** — se um nó cair, o arquivo não se perde inteiro (os pedaços ainda estão no outro)
- **Transparência de localização** — o usuário não precisa saber *onde* cada pedaço está; o orquestrador cuida disso
- **Escalabilidade horizontal** — basta adicionar mais nós (portas) para distribuir mais carga

---

## 📜 Licença

Projeto educacional para fins de estudo. Sinta-se à vontade para usar e modificar! ✌️
