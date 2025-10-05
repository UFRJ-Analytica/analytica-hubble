# 📡 Radar de Inundações (Projeto Analytica Hubble)

Este é um protótipo de interface de usuário desenvolvido para o projeto **Analytica Hubble**, como parte do NASA Space Apps Challenge 2025. A ferramenta visa fornecer uma análise preditiva sobre riscos de inundações em centros urbanos no Brasil, utilizando dados geoespaciais e históricos.

---

## ✨ Funcionalidades do Protótipo

* **Seleção de Localidade:** Permite ao usuário escolher uma cidade para análise.
* **Seleção de Período:** Oferece opções de períodos para a avaliação de risco.
* **Visualização Geográfica:** Exibe um mapa com a localização da área selecionada.
* **Métricas de Risco:** Apresenta um placar claro com o nível de risco de inundação e uma estimativa da população que pode ser afetada.
* **Interface Interativa:** Interface limpa e intuitiva construída com Streamlit.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework de UI:** Streamlit
* **Manipulação de Dados:** Pandas

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### Pré-requisitos

Antes de começar, você precisa ter instalado:
* [Python 3.8+](https://www.python.org/downloads/)
* `pip` (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório ou baixe os arquivos**
    Crie uma pasta para o projeto e coloque os arquivos `radardeinundacoes.py` e `requirements.txt` dentro dela.

2.  **Crie e ative um ambiente virtual (Recomendado)**
    Ambientes virtuais isolam as dependências do seu projeto.

    ```bash
    # Crie o ambiente virtual
    python -m venv venv

    # Ative o ambiente (Windows)
    .\venv\Scripts\activate

    # Ative o ambiente (Linux/macOS)
    source venv/bin/activate
    ```

3.  **Instale as dependências**
    Com o ambiente virtual ativado, instale as bibliotecas necessárias que estão listadas no arquivo `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

### Rodando a Aplicação

Depois de instalar as dependências, execute o seguinte comando no seu terminal:

```bash
streamlit run radardeinundacoes.py
```

Seu navegador será aberto automaticamente com a aplicação rodando no endereço `http://localhost:8501`.
