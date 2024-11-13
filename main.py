import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import gdown

message = "Os valores apresentados nas planilhas referem-se ao total (geral e por tipo de resíduo), por mês e ano, em toneladas, de resíduos sólidos coletados pelas empresas e concessionárias do serviço público participantes do Sistema de Limpeza Urbana da cidade de São Paulo. Nestes dados estão incluídos somente resíduos sólidos urbanos coletados pelo sistema público, não contemplando os volumes de resíduos do setor privado,dos grandes geradores (gerador que produz de lixo comum ou domiciliar, acima de 200 litros, como padarias, lanchonetes comércios e indústrias) e do sistema de logística reversa."

def baixar_arquivo(ano):

    file_ids = {
        2013: '1eigAZA7CesbolJ0fqjPMO1dy8spOMqRo',  
        2014: '15xaTTnpkul4htrcNGAlulUsU_UOXeg0O',
        2015: '1HAJMjVOVsSrEcg7cZNkyV-q6PKW3cM0I',
        2016: '12RqoruJDE8_7aK144PiKqjrn5JSsjBId',
        2017: '1E3EAguBPiauUFHVGvQnLj3NvZYVreFoN',
        2018: '1_NhxCitvFLT1viTYzCMGU9bG11ye4lum',
        2019: '1IsD9ipH8FNZLzhq2BSPcRcsoTH9aXlta',
        2020: '1AM7i0bs9RImHJslJ9x-1Ox6DsntJydKC'
    }
    
    file_id = file_ids.get(ano)
    
    if file_id is None:
        st.write(f"Arquivo para o ano {ano} não encontrado.")
        return None
    
    
    url = f"https://drive.google.com/uc?id={file_id}"
    
    output = f"sp_coletaresiduos{ano}.xlsx"
    
    
    gdown.download(url, output, quiet=False)
    
    df = pd.read_excel(output)
    return df


st.title("AV3 - Programação de Sistemas Especialistas\nProjeto: Análise de Dados de Resíduos Sólidos (São Paulo - SP)")


st.subheader("Integrantes da Equipe")
st.write("Danilo Ribeiro, Esdras Wendel, Renoir Auguste")

st.write("________________________________________")


st.subheader("""Alguns esclarecimentos referente ao Projeto
             http://dados.prefeitura.sp.gov.br/it/dataset/coleta-de-residuos-solidos-urbanos""")

st.write(message)


def plot_residuos_por_ano(ano):
    st.header(f"Ano: {ano}")
    
  
    df = baixar_arquivo(ano)
    
    if df is not None:
        df.index += 1  
        df = df[df['TIPO DE RESIDUO'] != 'TOTAL']  
        
        meses = df.columns[1:13]  
        
        residuos_array = df[meses].to_numpy()
        
        
        residuos_media = np.mean(residuos_array, axis=0)
        
        
        st.subheader("Tabela de Dados")
        df_rounded = df.round(2)
        st.dataframe(df_rounded, use_container_width=True)

        # Gráfico 1: Gráfico de Barras Empilhadas
        
        st.subheader("Gráfico Geral - Resíduos Coletados por Tipo de Resíduo (Barras Empilhadas)")
        
        
        residuos_tipo = df.set_index('TIPO DE RESIDUO')[meses].transpose()
        
        plt.figure(figsize=(10, 6))
        residuos_tipo.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.ylim(0, 500000)
        plt.title(f'Resíduos Coletados por Tipo - {ano}', fontsize=16)
        plt.xlabel('Meses', fontsize=12)
        plt.ylabel('Quantidade de Resíduos (em toneladas)', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title='Tipo de Resíduo', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(plt)

        # Gráfico 2: Média Mensal de Resíduos
        
        st.subheader("Gráfico Geral - Média Mensal de Resíduos")
        plt.figure(figsize=(10, 6))
        plt.plot(meses, residuos_media, label="Média Mensal", color='black', linestyle='--', linewidth=2)
        plt.ylim(0, 50000)
        plt.title(f'Variação Mensal dos Resíduos - Média ({ano})', fontsize=16)
        plt.xlabel('Meses', fontsize=12)
        plt.ylabel('Quantidade de Resíduos (em toneladas)', fontsize=12)
        plt.legend(title='Tipo de Resíduo', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(ticks=range(12), labels=meses, rotation=45)
        plt.gcf().patch.set_facecolor('#FFFFFF')
        st.pyplot(plt)

        # Gráfico 3: Resíduos Acumulados
        
        st.subheader("Gráfico de Resíduos Acumulados")
        
        residuos_acumulados = np.cumsum(residuos_media)
        
        plt.figure(figsize=(10, 6))
        plt.plot(meses, residuos_acumulados, label="Resíduos Acumulados", color='green', linestyle='-', linewidth=2)
        plt.ylim(0, 500000)
        plt.title(f'Resíduos Acumulados ao Longo do Ano - {ano}', fontsize=16)
        plt.xlabel('Meses', fontsize=12)
        plt.ylabel('Resíduos Acumulados (em toneladas)', fontsize=12)
        plt.legend(title='Acumulados', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(ticks=range(12), labels=meses, rotation=45)
        plt.gcf().patch.set_facecolor('#FFFFFF')
        st.pyplot(plt)

        # Gráfico 4: Comparação de Resíduos Mensais por Tipo de Resíduo
        
        st.subheader("Gráfico de Barras - Comparação de Resíduos Mensais por Tipo de Resíduo")
        
        plt.figure(figsize=(10, 6))
        df.set_index('TIPO DE RESIDUO')[meses].transpose().plot(kind='bar', figsize=(10, 6))
        plt.ylim(0, 500000)
        plt.title(f'Comparação de Resíduos Mensais por Tipo - {ano}', fontsize=16)
        plt.xlabel('Meses', fontsize=12)
        plt.ylabel('Quantidade de Resíduos (em toneladas)', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title='Tipo de Resíduo', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(plt)

        # Gráfico 5: Evolução de Cada Tipo de Resíduo
        
        st.subheader("Gráfico de Linha - Evolução de Cada Tipo de Resíduo")
        
        plt.figure(figsize=(10, 6))
        for tipo in df['TIPO DE RESIDUO']:
            plt.plot(meses, df[df['TIPO DE RESIDUO'] == tipo][meses].values.flatten(), label=tipo)
        
        plt.ylim(0, 500000)
        plt.title(f'Evolução Mensal de Cada Tipo de Resíduo - {ano}', fontsize=16)
        plt.xlabel('Meses', fontsize=12)
        plt.ylabel('Quantidade de Resíduos (em toneladas)', fontsize=12)
        plt.legend(title='Tipo de Resíduo', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Gráfico 6: Quantidade Total de Resíduos por Tipo de Resíduo
        
        st.subheader("Gráfico de Barras - Quantidade Total de Resíduos por Tipo")
        
        residuos_totais_por_tipo = df.set_index('TIPO DE RESIDUO')[meses].sum(axis=1)
        
        plt.figure(figsize=(10, 6))
        residuos_totais_por_tipo.plot(kind='bar', color='lightblue', figsize=(10, 6))
        plt.ylim(0, 5000000)
        plt.title(f'Quantidade Total de Resíduos por Tipo - {ano}', fontsize=16)
        plt.xlabel('Tipo de Resíduo', fontsize=12)
        plt.ylabel('Quantidade Total de Resíduos (em Mega Tonelada)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt)


ano_selecionado = st.sidebar.selectbox("Selecione o Ano", options=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])

plot_residuos_por_ano(ano_selecionado)
