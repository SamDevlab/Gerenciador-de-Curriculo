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
- 🖥️ **Interface Gráfica**: GUI intuitiva que abre automaticamente
- 🛡️ **Validações Robustas**: Impede o backup de arquivos não permitidos e valida entradas
- 🔒 **Segurança**: Confirmações para operações destrutivas

## 🛠️ Tecnologias Utilizadas

Este projeto utiliza **apenas bibliotecas nativas** do Python, garantindo máxima compatibilidade e zero configuração.

- **Linguagem**: Python 3.10+
- **Bibliotecas Nativas**:
  - `tkinter`: Interface Gráfica (GUI)
  - `pathlib`: Manipulação moderna de caminhos de arquivos
  - `argparse`: Interface de linha de comando robusta
  - `json`: Persistência de dados leve
  - `shutil`: Operações de arquivo seguras
  - `datetime` & `typing`: Type hints e manipulação de datas

## 📦 Instalação

### Pré-requisitos
Você só precisa ter o **Python 3.10+** instalado.

### Dependências
**Zero dependências externas!** Não é necessário rodar `pip install`. Basta baixar o script e rodar.

*Nota para usuários Linux: Caso o tkinter não esteja instalado por padrão na sua distro, use `sudo apt-get install python3-tk`.*

## 📖 Como Usar

### 🖥️ Interface Gráfica (Padrão)

A maneira mais fácil de usar. Basta rodar o script sem argumentos:

```bash
python main.py