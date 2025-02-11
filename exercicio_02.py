# Importando Bibliotecas
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image
import timeit
import io

# Configuração inicial da página
st.set_page_config(
    page_title='Telemarketing Analysis',
    page_icon='./telmarketing_icon.png',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Configuração do tema do seaborn
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# Função para carregar os dados
@st.cache_data(show_spinner=True)
def load_data(filepath):
    """Carrega dados de um arquivo CSV."""
    try:
        return pd.read_csv(filepath, sep=';')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para converter o DataFrame para Excel
def to_excel(df):
    """Converte um DataFrame para bytes de um arquivo Excel."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    processed_data = output.getvalue()
    return processed_data

# Função para aplicar filtros em colunas selecionadas
@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    """Filtra um DataFrame baseado nos valores selecionados de uma coluna específica."""
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

def main():
    # SIDEBAR
    st.sidebar.image('./Bank-Branding.jpg')
  

    st.write('# Telemarketing Analysis')
    st.markdown("---")

    # Inicia o cronômetro
    start = timeit.default_timer()


    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type = ['csv','xlsx'])

    
    if data_file_1 is None:
        st.stop()  # Interrompe a execução silenciosamente


    # Carrega os dados
    bank_raw = load_data(data_file_1)

    if bank_raw is None:
        return  # Interrompe se o arquivo não for carregado corretamente

    # Criar uma cópia para aplicar os filtros
    bank = bank_raw.copy()

# Exibir DataFrame antes dos filtros
    st.write("### Antes dos Filtros")
    st.write(bank_raw.head())


    with st.sidebar.form(key='my_form'):

        # SELECIONA O TIPO DE GRÁFICO
        graph_type = st.radio('Tipo de gráfico:', ('Barras', 'Pizza'))
        
        # IDADES
        max_age = int(bank_raw.age.max())  # Agora `bank_raw` já está definido
        min_age = int(bank_raw.age.min())
        idades = st.slider('Idade', min_age, max_age, (min_age, max_age), step=1)

        # Filtros Multiselect
        filtros = {
            "Profissão": "job",
            "Estado civil": "marital",
            "Default": "default",
            "Financiamento Imobiliário?": "housing",
            "Tem empréstimo?": "loan",
            "Meio de contato": "contact",
            "Mês do contato": "month",
            "Dia da semana": "day_of_week"
        }

        selecionados = {}
        for label, coluna in filtros.items():
            opcoes = bank_raw[coluna].unique().tolist() + ['all']
            selecionados[coluna] = st.multiselect(label, opcoes, ['all'])

        # Botão para aplicar filtros
        submit_button = st.form_submit_button("Aplicar Filtros")

    # Aplicando os filtros SOMENTE se o botão for pressionado
    if submit_button:
        bank = bank.query("age >= @idades[0] and age <= @idades[1]")
        for coluna, valores in selecionados.items():
            if 'all' not in valores:
                bank = bank[bank[coluna].isin(valores)].reset_index(drop=True)

    st.write('## Após os filtros')
    st.write(bank.head())

    df_xlsx = to_excel(bank)
    st.download_button(label='⬇️  Download tabela filtrada em EXCEL',
                            data=df_xlsx ,
                            file_name= 'bank_filtered.xlsx')
    st.markdown("---")


    # CRIAÇÃO DOS DATAFRAMES PARA O GRÁFICO
    bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True).mul(100).reset_index()
    bank_raw_target_perc.columns = ['Categoria', 'Percentual']

    try:
        bank_target_perc = bank['y'].value_counts(normalize=True).mul(100).reset_index()
        bank_target_perc.columns = ['Categoria', 'Percentual']
    except:
            st.error('Erro no filtro')

    # Botões de download dos dados dos gráficos
    col1, col2 = st.columns(2)

    df_xlsx = to_excel(bank_raw_target_perc)
    col1.write('### Proporção original')
    col1.write(bank_raw_target_perc)
    col1.download_button(label='⬇️  Download',
                            data=df_xlsx ,
                            file_name= 'bank_raw_y.xlsx')
        
    df_xlsx = to_excel(bank_target_perc)
    col2.write('### Proporção da tabela com filtros')
    col2.write(bank_target_perc)
    col2.download_button(label='⬇️  Download',
                            data=df_xlsx ,
                            file_name= 'bank_y.xlsx')
    st.markdown("---")


    # Dicionário de cores 
    cores = {"yes": "#39C841", "no": "#DB132B"}



    # Criando a figura com subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Dados Brutos", "Dados Filtrados"])

    # Gráfico dos dados brutos
    fig.add_trace(go.Bar(
        x=bank_raw_target_perc['Categoria'],  
        y=bank_raw_target_perc['Percentual'],
        text=[f"{v:.1f}%" for v in bank_raw_target_perc['Percentual']],
        textposition='outside',
        name="Dados Brutos",
        marker=dict(color=[cores.get(c, "gray") for c in bank_raw_target_perc['Categoria']])
    ), row=1, col=1)  

    # PLOTS
    if graph_type == 'Barras':
        fig.add_trace(go.Bar(
            x=bank_target_perc['Categoria'],  
            y=bank_target_perc['Percentual'],
            text=[f"{v:.1f}%" for v in bank_target_perc['Percentual']],
            textposition='outside',
            name="Dados Filtrados",
            marker=dict(color=[cores.get(c, "gray") for c in bank_target_perc['Categoria']])
        ), row=1, col=2)  

        # Layout do gráfico
        fig.update_layout(
            title_text="Proporção de Aceite",
            showlegend=False,  
            paper_bgcolor="#F8F9FA",  
            plot_bgcolor="white"
        )
    else:

                # Criando subplots para os gráficos de pizza
        fig = make_subplots(rows=1, cols=2, subplot_titles=["Dados Brutos", "Dados Filtrados"], 
                            specs=[[{"type": "pie"}, {"type": "pie"}]])

        # Gráfico de pizza para os dados brutos
        fig.add_trace(go.Pie(
            labels=bank_raw_target_perc['Categoria'],  # Ajuste correto para a coluna renomeada
            values=bank_raw_target_perc['Percentual'],  
            textinfo='percent+label',  
            marker=dict(colors=["#39C841", "#DB132B"])
        ), row=1, col=1)

        # Gráfico de pizza para os dados filtrados
        fig.add_trace(go.Pie(
            labels=bank_target_perc['Categoria'],  
            values=bank_target_perc['Percentual'],  
            textinfo='percent+label',  
            marker=dict(colors=["#39C841", "#DB132B"])
        ), row=1, col=2)

        # Layout
        fig.update_layout(
            title_text="Distribuição da Resposta da Campanha",
            showlegend=False,
            paper_bgcolor="#F8F9FA"
        )


    # Exibir no Streamlit
    st.plotly_chart(fig)

if __name__ == '__main__':
	main()
