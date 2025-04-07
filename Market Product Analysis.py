import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tabulate import tabulate

# Função para identificar e retornar outliers para volume e valor por subproduto
def identificar_outliers(dataframe):
    outliers_volume = {}
    outliers_valor = {}
    
    for subproduto in dataframe['SubProduto'].unique():
        sub_df = dataframe[dataframe['SubProduto'] == subproduto]

        # Calculando os limites dos outliers para o volume
        Q1_volume = sub_df['Volumen'].quantile(0.25)
        Q3_volume = sub_df['Volumen'].quantile(0.75)
        IQR_volume = Q3_volume - Q1_volume
        lower_bound_volume = Q1_volume - 1.5 * IQR_volume
        upper_bound_volume = Q3_volume + 1.5 * IQR_volume
        outliers_volume[subproduto] = sub_df[(sub_df['Volumen'] < lower_bound_volume) | (sub_df['Volumen'] > upper_bound_volume)]

        # Calculando os limites dos outliers para o valor
        Q1_valor = sub_df['Valor'].quantile(0.25)
        Q3_valor = sub_df['Valor'].quantile(0.75)
        IQR_valor = Q3_valor - Q1_valor
        lower_bound_valor = Q1_valor - 1.5 * IQR_valor
        upper_bound_valor = Q3_valor + 1.5 * IQR_valor
        outliers_valor[subproduto] = sub_df[(sub_df['Valor'] < lower_bound_valor) | (sub_df['Valor'] > upper_bound_valor)]
    
    return outliers_volume, outliers_valor

# Carregando o arquivo Excel
arquivo_excel = 'C:\Users\Caique-PC\Desktop\Analises de Dados Feitas\data_analysis'
dados = pd.read_excel('DB')

# Gerando gráficos de outliers e identificando outliers para cada subproduto
variaveis_numericas = []
for i in dados.columns[3:5].tolist():
    if dados.dtypes[i] == 'float64':
        print(i, ':', dados.dtypes[i])
        variaveis_numericas.append(i)

plt.figure(figsize=(20, 15))
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 24

num_variaveis = len(variaveis_numericas)
f, axes = plt.subplots(1, num_variaveis)

for coluna, variavel in enumerate(variaveis_numericas):
    sns.scatterplot(data=dados, x=dados.index, y=variavel, ax=axes[coluna])
   
    Q1 = dados[variavel].quantile(0.25)
    Q3 = dados[variavel].quantile(0.75)
    print(f"{variavel} - Q1: {Q1}, Q3: {Q3}")

   
    axes[coluna].axhline(y=Q1, color='r', linestyle='--', label='Q1')
    axes[coluna].axhline(y=Q3, color='g', linestyle='--', label='Q3')


handles, labels = axes[0].get_legend_handles_labels()
if labels:
    f.legend(handles, labels, loc='upper right')
plt.show()

outliers_volume, outliers_valor = identificar_outliers(dados)

# Imprimindo outliers para cada subproduto
for subproduto in dados['SubProduto'].unique():
    print(f"\nOutliers para '{subproduto}':")
    print("Volume:")
    print(tabulate(outliers_volume[subproduto], headers='keys', tablefmt='pretty'))
    print("\nValor:")
    print(tabulate(outliers_valor[subproduto], headers='keys', tablefmt='pretty'))

