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


### Satélites Utilizados

- **NASA/NASADEM_HGT/001** - https://developers.google.com/earth-engine/datasets/catalog/NASA_NASADEM_HGT_001?hl=pt-br
- **CIESIN/GPWv411/GPW_Population_Count** - https://developers.google.com/earth-engine/datasets/catalog/CIESIN_GPWv411_GPW_Population_Count?hl=pt-br
- **MODIS/061/MCD12Q1** - https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1?hl=pt-br
- **NASA/GPM_L3/IMERG_MONTHLY_V06** - https://developers.google.com/earth-engine/datasets/catalog/NASA_GPM_L3_IMERG_MONTHLY_V06?hl=pt-br
- **NASA/FLDAS/NOAH01/C/GL/M/V001** - https://developers.google.com/earth-engine/datasets/catalog/NASA_FLDAS_NOAH01_C_GL_M_V001?hl=pt-br
- **NASA/SMAP/SPL4SMGP/008** - https://developers.google.com/earth-engine/datasets/catalog/NASA_SMAP_SPL4SMGP_008?hl=pt-br
- **LANDSAT/LT05/C02/T1_L2** - https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2?hl=pt-br
- **LANDSAT/LE07/C02/T1_L2** - https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2?hl=pt-br
- **LANDSAT/LC08/C02/T1_L2** - https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2?hl=pt-br
- **LANDSAT/LC09/C02/T1_L2** - https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2?hl=pt-br
