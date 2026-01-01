# 📄 Resume Version Manager (CLI)

*"Chega de curriculo_final_v2_agora_vai.pdf espalhado pela área de trabalho."*

Uma ferramenta de linha de comando (CLI) simples e poderosa escrita em Python para gerenciar, versionar e organizar o histórico do seu currículo. Funciona como uma "Time Machine" local para seus documentos.

## 🎯 O Problema

Durante a busca por emprego, adaptamos nosso currículo para diferentes vagas e empresas. Isso gera uma confusão de arquivos com nomes estranhos, e muitas vezes perdemos aquela versão perfeita que fizemos semana passada.

## 💡 A Solução

Este script automatiza o backup e o versionamento. Ele copia seu arquivo atual para um repositório seguro, renomeia com data/hora e etiquetas (tags), e mantém um registro JSON organizado.

## 🚀 Funcionalidades

- 📸 **Snapshots Automáticos**: Salva uma cópia do arquivo com Timestamp + Tag.
- 🗂️ **Histórico Organizado**: Lista todas as versões em uma tabela limpa no terminal.
- 🏷️ **Tags e Notas**: Permite adicionar metadados (ex: "Vaga Google", "Foco Backend") para fácil identificação.
- ♻️ **Restauração Segura**: Recupere qualquer versão antiga com um único comando, sem sobrescrever acidentalmente o arquivo atual.
- 🛡️ **Validações**: Impede o backup de arquivos não permitidos (apenas .pdf, .docx, etc.) e evita duplicidade de IDs.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Bibliotecas Nativas**:
  - `pathlib`: Manipulação moderna de caminhos de arquivos.
  - `argparse`: Criação de interface de linha de comando robusta.
  - `json`: Persistência de dados leve.
  - `shutil`: Operações de arquivo de alto nível.
  - `datetime` & `typing`.

## 📦 Como Usar

### 1. Pré-requisitos

Você só precisa ter o Python 3.10+ instalado na sua máquina.

### 2. Comandos Disponíveis

#### ➤ Adicionar uma nova versão (add)

Salva o estado atual do seu currículo.

```bash
python index.py add "meu_curriculo.pdf" -t "Senior_Dev" -n "Adicionei certificação AWS"
```

#### ➤ Listar histórico (list)

Vê todas as versões salvas, IDs e notas.

```bash
python index.py list
```

**Saída Exemplo:**

```
ID   | DATA               | TAG            | NOTA
----------------------------------------------------------------------
3    | 01/01/2026 14:30  | Senior_Dev     | Adicionei certificação AWS..
2    | 28/12/2025 09:15  | Estagio        | Versão inicial
```

#### ➤ Restaurar uma versão (restore)

Traz uma versão antiga de volta para a pasta atual.

```bash
# Restaura a versão com ID 2
python index.py restore 2

# Ou defina um nome específico para o arquivo de saída
python index.py restore 2 -o "curriculo_recuperado.pdf"
```

#### ➤ Deletar uma versão (delete)

Remove o registro do banco de dados e o arquivo de backup físico.

```bash
python index.py delete 3
```

## 📂 Estrutura do Projeto

Ao rodar o script pela primeira vez, ele cria automaticamente a estrutura necessária:

```
.
├── index.py                 # O Script principal
├── resume_history.json      # "Banco de dados" dos registros
└── resume_backups/          # Pasta onde os arquivos ficam guardados (seguro)
    ├── 20260101_143000_Senior_Dev.pdf
    └── 20251228_091500_Estagio.pdf
```

## 🧠 Aprendizados

Este projeto foi desenvolvido para demonstrar competências em:

- **Automação de Tarefas**: Resolver um problema real do dia a dia.
- **Manipulação de Sistema de Arquivos**: Uso seguro de `pathlib` e tratamento de exceções.
- **Design de Software**: Separação de responsabilidades, Type Hinting e código limpo.

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar e modificar.
