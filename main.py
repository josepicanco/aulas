import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# localizando nossa base (esse arquivo deve estar na mesma pasta do codigo)
arquivo_csv = 'titanic_dataset.csv'

# lendo o arquivo para verificar algum erro
if os.path.exists(arquivo_csv):
    # lendo a tabela do titanic
    tabela = pd.read_csv(arquivo_csv)

    # verificação para limpeza
    print("--- RELATÓRIO DE DADOS ---")
    total_antes = len(tabela)
    nulos_por_coluna = tabela.isnull().sum()
    
    print(f"Total de passageiros no começo: {total_antes}")
    print("Dados faltando por coluna:")
    print(nulos_por_coluna)
    print("-" * 30)

    # Gráfico simples para mostrar o que estava "sujo" (nulos)
    plt.figure(figsize=(8, 4))
    nulos_por_coluna[nulos_por_coluna > 0].plot(kind='bar', color='orange')
    plt.title('O que eu encontrei de dados nulos:')
    plt.ylabel('Quantidade de buracos nos dados')
    plt.show()

    # preenchendo as idades vazias com a mediana (assim evita dados nulos)
    valor_do_meio = tabela['Age'].median()
    tabela['Age'] = tabela['Age'].fillna(valor_do_meio)

    # tirando a coluna da cabine que tem muitoS NULOS
    tabela = tabela.drop(columns=['Cabin'])

    # tirando linhas que não tem o porto de embarque (são poucas não influenciam o resultado)
    tabela.dropna(subset=['Embarked'], inplace=True)

    # TRABALHANDO COM A FAMÍLIA (SibSp e Parch)
    # somar os parentes pra ver quem tava sozinho
    tabela['Soma_Parentes'] = tabela['SibSp'] + tabela['Parch']
    
    # critério para saber quem estava sozinho ou não
    tabela.loc[tabela['Soma_Parentes'] == 0, 'Como_Viajava'] = 'Sozinho'
    tabela.loc[tabela['Soma_Parentes'] > 0, 'Como_Viajava'] = 'Com Familia'

    # GRÁFICOS
    # Gráfico 1 - Sobrevivência por Classe e Sexo
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    
    # vermelho mulher e azul homem
    cores_lista = {"female": "red", "male": "blue"}
    
    sns.barplot(data=tabela, x='Pclass', y='Survived', hue='Sex', palette=cores_lista, errorbar=None)
    
    plt.title('Sobrevivencia por Classe e Sexo')
    plt.xlabel('Classe')
    plt.ylabel('Taxa de Sobreviventes')
    plt.legend(title='Legenda', labels=['Homem (Azul)', 'Mulher (Vermelho)'])

    # Gráfico 2 - Porto de Embarque
    plt.subplot(1, 2, 2)
    
    # traduzindo os portos pra ficar mais fácil de ler
    tabela['Porto'] = tabela['Embarked'].replace({'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'})
    
    sns.countplot(data=tabela, x='Porto', hue='Survived', palette='magma')
    plt.title('Sobreviventes por Porto')
    plt.legend(title='Sobreviveu', labels=['Nao', 'Sim'])

    plt.tight_layout()
    plt.show()

    # Gráfico 3 - Família
    plt.figure(figsize=(7, 4))
    sns.barplot(data=tabela, x='Como_Viajava', y='Survived', errorbar=None)
    plt.title('Quem sobreviveu mais: Sozinho ou com Familia?')
    plt.show()

    print("Terminei de rodar tudo!")
else:
    print("O arquivo nao foi encontrado, coloque ele na mesma pasta do script")