import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import gdown

# Configuração do Streamlit
st.set_page_config(page_title="Análise de Resíduos SP", layout="wide")

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

st.title("Análise da Gestão de Resíduos Sólidos em São Paulo")
st.subheader("""
                **AV3** - Sistema de Gerenciamento de Resíduos (ODS 12)\n
                **Projeto** Integrado das disciplinas: Sistemas Especialistas, Análise Orientada a Objetos, Modelagem e Simulação Matemática\n
                **Equipe:** Danilo Ribeiro, Esdras Wendel e Renoir Auguste\n
                **Professores:** Caio Eduardo, Diego Passos e Igor González Pimenta\n
                **Faculdade:** Unijorge\n            """)

st.markdown(""" 
        ### Objetivo
        Este projeto visa desenvolver um software orientado a objeto para gerenciar e analisar dados relacionados à gestão de resíduos, oferecendo assim uma análise interativa dos dados de coleta de resíduos sólidos em São Paulo, permitindo:
        - **Monitoramento dos resíduos coletados.**
        - **Compreender os padrões de geração de resíduos ao longo do tempo.**
        - **Identificar os tipos de resíduos com maior volume coletado.**
        - **Gerar insights para aprimorar a gestão de resíduos urbanos.**
        
        ### Sobre os Dados
        Os dados utilizados foram extraídos de relatórios oficiais da cidade de São Paulo, abrangendo o período de **2013 a 2020**.
        
        ### Resultados e Benefícios
        A análise revela que o **lixo domiciliar** é o tipo de resíduo mais prevalente na coleta, destacando-se como o maior desafio para o sistema público de gestão de resíduos. Esse padrão se mantém consistente ao longo dos anos, evidenciando a necessidade de políticas públicas focadas em **educação ambiental** e **incentivo à reciclagem**.
        
        A implementação de programas de separação na fonte e de iniciativas de compostagem pode ajudar a reduzir o volume total de resíduos, aumentando a eficiência do sistema de coleta. Por outro lado, a menor representatividade de outros tipos de resíduos, como entulho e restos de poda, sugere que sua origem está em grandes geradores que não são atendidos pela coleta pública. Isso aponta para a importância de desenvolver iniciativas específicas, como sistemas de logística reversa e programas de coleta especializada, para tratar esses resíduos de forma eficaz.
        
        ### Benefícios da Análise
        - **Apoio na tomada de decisões** para políticas públicas.
        - Identificação de oportunidades para **reciclagem e reutilização**.
        - **Aumento da conscientização ambiental**.
    """)

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
        residuos_totais_por_tipo = df.groupby('TIPO DE RESIDUO')[meses].sum().transpose()
        residuos_totais_por_tipo.plot(kind='bar', figsize=(20, 10))
        plt.ylim(0, 500000)
        plt.title(f'Quantidade Total de Resíduos por Tipo de Resíduo - {ano}', fontsize=16)
        plt.xlabel('Meses', fontsize=12)
        plt.ylabel('Quantidade de Resíduos (em toneladas)', fontsize=12)
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Gráfico 7: Mediana dos Resíduos por Mês
        st.subheader("Gráfico da Mediana de Resíduos por Mês")
        residuos_mediana = np.median(residuos_array, axis=0)
        plt.figure(figsize=(10, 6))
        plt.plot(meses, residuos_mediana, label="Mediana", color='blue', linestyle='-', linewidth=2)
        plt.ylim(0, 50000)
        plt.title(f'Mediana Mensal dos Resíduos - {ano}', fontsize=16)
        plt.xlabel('Meses', fontsize=12)
        plt.ylabel('Quantidade de Resíduos (em toneladas)', fontsize=12)
        plt.legend(title='Mediana de Residuos', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(ticks=range(12), labels=meses, rotation=45)
        plt.gcf().patch.set_facecolor('#FFFFFF')
        st.pyplot(plt)

        st.header("Conclusão")
        st.subheader("Considerações finais do Projeto")

        st.markdown("""
<div style="text-align: justify;">
A análise dos resíduos sólidos coletados na cidade de São Paulo revela padrões cruciais para a gestão de resíduos urbanos. 
A predominância do lixo domiciliar destaca-se como o principal tipo de resíduo, refletindo o comportamento e o volume gerado pela população. Essa constatação indica que a gestão de resíduos residenciais é o maior desafio enfrentado pelo sistema público de coleta.
Essa concentração de lixo domiciliar é consistente ao longo dos anos analisados, evidenciando a necessidade de políticas públicas eficazes que promovam educação ambiental e incentivem a reciclagem. Programas de separação na fonte e iniciativas de compostagem podem desempenhar um papel fundamental na redução do volume de resíduos e no aumento da eficiência do sistema de coleta.
Por outro lado, os dados também destacam uma menor participação de outros tipos de resíduos, como entulho e restos de poda, o que sugere que esses volumes são oriundos de grandes geradores não atendidos pela coleta pública. Isso aponta para a necessidade de desenvolver soluções específicas para lidar com esses resíduos, como sistemas de logística reversa e programas de coleta especializada.
Portanto, é essencial que a gestão do lixo domiciliar seja uma prioridade, dada sua importância em termos de volume e impacto na eficiência da limpeza urbana. A implementação de ações coordenadas, que envolvam educação, infraestrutura e parcerias público-privadas, será fundamental para tornar o sistema de gestão de resíduos de São Paulo mais sustentável e eficiente.
Explore as páginas no menu lateral para interagir com os gráficos e obter insights detalhados sobre a gestão de resíduos na cidade.
</div>
""", unsafe_allow_html=True)
        

        st.subheader("Referências")
        st.write(" Base de Dados + Repositório (Github)")                
        st.write("http://dados.prefeitura.sp.gov.br/it/dataset/coleta-de-residuos-solidos-urbanos")
        st.write("https://github.com/rv-dnl/datascience-project/blob/main/main.py")




ano = st.selectbox("Escolha o ano", [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])


plot_residuos_por_ano(ano)