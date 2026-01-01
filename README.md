# 📄 Gerenciador de Versões de Currículo

*"Chega de curriculo_final_v2_agora_vai.pdf espalhado pela área de trabalho."*

Uma ferramenta de linha de comando (CLI) e com interface simples e poderosa escrita em Python para gerenciar, versionar e organizar o histórico do seu currículo. Funciona como uma "Time Machine" local para seus documentos.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 🎯 O Problema

Durante a busca por emprego, adaptamos nosso currículo para diferentes vagas e empresas. Isso gera uma confusão de arquivos com nomes estranhos, e muitas vezes perdemos aquela versão perfeita que fizemos semana passada.

## 💡 A Solução

Este script automatiza o backup e o versionamento. Ele copia seu arquivo atual para um repositório seguro, renomeia com data/hora e etiquetas (tags), e mantém um registro JSON organizado.

## 🚀 Funcionalidades

- 📸 **Snapshots Automáticos**: Salva uma cópia do arquivo com Timestamp + Tag
- 🗂️ **Histórico Organizado**: Lista todas as versões em uma tabela limpa no terminal
- 🏷️ **Tags e Notas**: Permite adicionar metadados (ex: "Vaga Google", "Foco Backend") para fácil identificação
- ♻️ **Restauração Segura**: Recupere qualquer versão antiga com um único comando, sem sobrescrever acidentalmente o arquivo atual
- 🗑️ **Gerenciamento Completo**: Delete versões antigas quando não precisar mais delas
- 🖥️ **Interface Gráfica**: GUI intuitiva com suporte a arrastar e soltar
- 🛡️ **Validações Robustas**: Impede o backup de arquivos não permitidos e valida entradas
- 🔒 **Segurança**: Confirmações para operações destrutivas

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Bibliotecas Nativas**:
  - `pathlib`: Manipulação moderna de caminhos de arquivos
  - `argparse`: Interface de linha de comando robusta
  - `json`: Persistência de dados leve
  - `shutil`: Operações de arquivo seguras
  - `datetime` & `typing`: Type hints e manipulação de datas
- **Bibliotecas Opcionais**:
  - `tkinter`: Interface gráfica nativa
  - `tkdnd`: Suporte avançado a arrastar e soltar

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior instalado
- Sistema operacional: Windows, macOS ou Linux

### Instalação Básica

1. **Clone ou baixe** os arquivos do projeto
2. **Navegue** até a pasta do projeto:
   ```bash
   cd "caminho/para/versionador-de-curriculo"
   ```

### Instalação com Suporte a Arrastar e Soltar (Opcional)

Para suporte completo a arrastar e soltar na interface gráfica:

```bash
pip install tkdnd
```

*Nota: Sem essa biblioteca, a GUI ainda funciona, mas você precisará clicar para selecionar arquivos.*

## 📖 Como Usar

### Interface de Linha de Comando (CLI)

#### ➤ Adicionar uma nova versão

```bash
python index.py add "meu_curriculo.pdf" -t "Senior_Dev" -n "Adicionei certificação AWS"
```

**Parâmetros:**
- `file`: Caminho para o arquivo do currículo (.pdf, .docx, .doc, .txt)
- `-t/--tag`: Tag obrigatória (ex: "Google", "Senior", "Estagio")
- `-n/--note`: Nota opcional descritiva

#### ➤ Listar histórico

```bash
python index.py list
```

**Saída Exemplo:**
```
ID   | DATA               | TAG            | NOTA
----------------------------------------------------------------------
3    | 01/01/2026 14:30  | Senior_Dev     | Adicionei certificação AWS..
2    | 28/12/2025 09:15  | Estagio        | Versão inicial
1    | 25/12/2025 10:45  | Junior         | Primeira versão
```

#### ➤ Restaurar uma versão

```bash
# Restaura a versão com ID 2
python index.py restore 2

# Ou defina um nome específico para o arquivo de saída
python index.py restore 2 -o "curriculo_recuperado.pdf"
```

#### ➤ Deletar uma versão

```bash
python index.py delete 3
```

*⚠️ Esta operação remove permanentemente o arquivo de backup e o registro do histórico.*

### Interface Gráfica (GUI)

Para uma experiência mais visual e intuitiva:

```bash
python index.py gui
```

#### Funcionalidades da GUI:

- **🖱️ Área de Arrastar e Soltar**: Arraste seu currículo diretamente da área de trabalho
- **📝 Campos de Entrada**: Digite tag e nota de forma visual
- **✅ Validação**: Verificação automática de campos obrigatórios
- **📋 Histórico Visual**: Visualize todas as versões em uma janela separada
- **🧹 Interface Limpa**: Campos são limpos automaticamente após adicionar

#### Como Usar a GUI:

1. Execute `python index.py gui`
2. Arraste seu arquivo para a área indicada (ou clique para selecionar)
3. Digite uma tag descritiva (ex: "Google_Tech", "Senior_Python")
4. Adicione uma nota opcional
5. Clique em "➕ Adicionar Versão"
6. Use "📋 Listar Histórico" para ver todas as versões salvas

## 📂 Estrutura do Projeto

O script cria automaticamente a estrutura necessária na primeira execução:

```
versionador-de-curriculo/
├── index.py                    # Script principal (CLI + GUI)
├── readme.md                   # Esta documentação
├── resume_history.json         # Banco de dados JSON dos registros
└── resume_backups/             # Pasta segura para backups
    ├── 20260101_143000_Senior_Dev.pdf
    ├── 20251228_091500_Estagio.pdf
    └── ...
```

### Arquivos Gerados:

- **`resume_history.json`**: Contém metadados de todas as versões
- **`resume_backups/`**: Pasta com todas as cópias de backup físicas
- **Nomes de arquivo**: Formato `AAAAMMDD_HHMMSS_TAG.extensão`

## 🔧 Configuração Avançada

### Extensões Suportadas

Por padrão, o sistema aceita:
- `.pdf` - Documentos PDF
- `.docx` - Documentos Word modernos
- `.doc` - Documentos Word legados
- `.txt` - Arquivos de texto

### Personalização

Para modificar as extensões permitidas, edite a constante `ALLOWED_EXTENSIONS` no código:

```python
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt', '.rtf'}
```

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique se o caminho do arquivo está correto
- Use aspas se o caminho contiver espaços

### Erro: "Extensão não permitida"
- Verifique se o arquivo tem uma extensão suportada (.pdf, .docx, .doc, .txt)
- Para adicionar suporte a outras extensões, modifique `ALLOWED_EXTENSIONS`

### GUI não abre
- Certifique-se de que tkinter está instalado (vem com Python por padrão)
- Para Windows: `python -m tkinter` para testar
- Para Linux: `sudo apt-get install python3-tk`

### Arrastar e soltar não funciona
- Instale tkdnd: `pip install tkdnd`
- Reinicie o script

## 🧠 Aprendizados e Competências Demonstradas

Este projeto foi desenvolvido para demonstrar:

- **🏗️ Arquitetura de Software**: Separação clara entre CLI e GUI
- **🔧 Manipulação de Sistema de Arquivos**: Uso seguro de pathlib e validações
- **📊 Persistência de Dados**: JSON para armazenamento estruturado
- **🖥️ Desenvolvimento de Interfaces**: Tkinter para aplicações desktop
- **⚡ Automação**: Resolução prática de problemas do dia a dia
- **🛡️ Tratamento de Erros**: Validações robustas e mensagens claras
- **📝 Documentação**: README completo e código comentado

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**💡 Dica**: Mantenha suas tags consistentes (ex: "Empresa_Cargo", "Data_Foco") para facilitar a busca posterior!

**📧 Suporte**: Para dúvidas ou sugestões, abra uma issue no repositório.
