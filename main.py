import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import gdown

message = """
<div style="text-align: justify;">
Os valores apresentados nas planilhas referem-se ao total (geral e por tipo de resíduo), por mês e ano, em toneladas, de resíduos sólidos coletados pelas empresas e concessionárias do serviço público participantes do Sistema de Limpeza Urbana da cidade de São Paulo. 
Os dados analisados abrangem os anos de <strong>2013 a 2020</strong>, permitindo uma visão temporal das variações e tendências na coleta de resíduos sólidos na cidade.

Nestes dados estão incluídos somente resíduos sólidos urbanos coletados pelo sistema público, não contemplando os volumes de resíduos do setor privado, dos grandes geradores (geradores que produzem acima de 200 litros de lixo comum ou domiciliar, como padarias, lanchonetes, comércios e indústrias) e do sistema de logística reversa. 

Além disso, o estudo destaca a coleta de diferentes tipos de resíduos, como lixo domiciliar, entulho e restos de poda, evidenciando a predominância do lixo domiciliar como principal tipo coletado. Este levantamento fornece subsídios importantes para a elaboração de políticas públicas de gerenciamento de resíduos, bem como para iniciativas de redução, reciclagem e reaproveitamento, visando a sustentabilidade ambiental e a eficiência do sistema de limpeza urbana de São Paulo.
</div>
"""


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



url_imagem = 'https://images.even3.com/s0wEPJKo7O8zF6dk3lUq79KWry8=/fit-in/250x250/smart/even3.blob.core.windows.net/logos/marca_UJ_2019_VERTICAL_Colorida_Prancheta1.0c8ff47c70f94f41aae7.png'


st.markdown(f"""
<div style="text-align: center;">
    <img src="{url_imagem}" width="250" />
</div>
""", unsafe_allow_html=True)



st.title("AV3 - Programação de Sistemas Especialistas\nProjeto: Análise de Dados de Resíduos Sólidos (São Paulo - SP)")



st.subheader("""
            
            Equipe: Danilo Ribeiro, Esdras Wendel e Renoir Auguste
            
            """)
st.subheader("Orientador: Igor González Pimenta")


st.header("Introdução")


st.markdown(message, unsafe_allow_html=True)


def plot_residuos_por_ano(ano):
    st.subheader(f"Coleta de Resíduos Sólidos: {ano}")
    
    df = baixar_arquivo(ano)
    
    if df is not None:
        df.index += 1  
        df = df[df['TIPO DE RESIDUO'] != 'TOTAL']  
        
        meses = df.columns[1:13]  
        
        residuos_array = df[meses].to_numpy()
        
        
        residuos_media = np.mean(residuos_array, axis=0)
        
        
        st.subheader("Extração e Tratamento dos Dados - Pandas")
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

        st.header("Conclusão")
        st.subheader("Considerações finais do Projeto")
        st.subheader("Conclusão")

        st.markdown("""
<div style="text-align: justify;">
A análise dos resíduos sólidos coletados na cidade de São Paulo revela padrões importantes sobre a gestão de resíduos urbanos. 
Um dos principais destaques é a predominância do <strong>lixo domiciliar</strong>, que representa a maior parcela entre os tipos de resíduos coletados. 
Esse padrão reflete o comportamento e o volume gerado diretamente pela população, indicando que o gerenciamento do lixo residencial é o maior desafio para o sistema público.

A concentração do lixo domiciliar como principal contribuinte é consistente em todos os anos analisados, o que reforça a necessidade de políticas públicas voltadas para <strong>educação ambiental</strong> e <strong>incentivo à reciclagem</strong>. 
A criação de programas de separação na fonte e iniciativas de compostagem também poderiam reduzir o volume total e aumentar a eficiência do sistema.

Por outro lado, os dados também indicam uma menor representatividade de outros resíduos sólidos, como entulho e restos de poda, o que pode ser atribuído a volumes gerados principalmente por grandes geradores, que não estão incluídos na coleta pública. 
Isso destaca a importância de iniciativas específicas para lidar com esses resíduos, como sistemas de logística reversa e programas de coleta especializados.

Em resumo, a gestão do lixo domiciliar deve ser priorizada, tanto pela sua relevância em volume quanto pelo impacto direto na eficiência da limpeza urbana. 
A implementação de ações coordenadas, envolvendo educação, infraestrutura e parcerias público-privadas, será essencial para tornar o sistema de resíduos da cidade mais sustentável.
</div>
""", unsafe_allow_html=True)
        

        st.subheader("Referências")
        st.write(" Base de Dados + Repositório (Github)")                
        st.write("http://dados.prefeitura.sp.gov.br/it/dataset/coleta-de-residuos-solidos-urbanos")
        st.write("https://github.com/rv-dnl/datascience-project/blob/main/main.py")
    
        





ano_selecionado = st.sidebar.selectbox("Selecione o Ano", options=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])



plot_residuos_por_ano(ano_selecionado)
