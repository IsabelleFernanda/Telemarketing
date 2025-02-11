# Telemarketing Analysis

## Visão Geral
Este projeto realiza uma análise exploratória de dados de uma campanha de telemarketing de um banco. Utilizando a biblioteca Streamlit, a aplicação permite a importação de um arquivo de dados, aplicação de filtros e geração de gráficos interativos para visualização das informações.

## Funcionalidades
- Upload de arquivos CSV ou Excel com dados da campanha
- Filtros interativos por idade, profissão, estado civil, tipo de contato, entre outros
- Geração de tabelas dinâmicas para visualizar a distribuição dos clientes
- Exportação dos dados filtrados em formato Excel
- Gráficos dinâmicos (barras e pizza) com Plotly para análise de aceitação da campanha

## Tecnologias Utilizadas
- Python
- Streamlit
- Pandas
- Seaborn
- Plotly
- XlsxWriter

## Como Executar o Projeto
1. Clone este repositório:
   ```bash
   git clone https://github.com/IsabelleFernanda/Telemarketing.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd Telemarketing
   ```
3. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   streamlit run exercicio_02.py
   ```

## Demonstração
A aplicação está hospedada no Render e pode ser acessada pelo seguinte link:
[Telemarketing Analysis - Render](https://telemarketing-pnxh.onrender.com/)

## Estrutura do Projeto
```
Telemarketing/
│-- exercicio_02.py       # Código principal da aplicação Streamlit
│-- requirements.txt      # Dependências necessárias
│-- README.md             # Documentação do projeto
│-- telmarketing_icon.png # Ícone da página
│-- Bank-Branding.jpg     # Imagem usada na sidebar
```

## Contato
Caso tenha dúvidas ou sugestões, entre em contato via GitHub!

---
Desenvolvido por Isabelle Fernanda 

