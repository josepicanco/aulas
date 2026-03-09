import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# pegando o arquivo que tá na pasta
arquivo_csv = 'titanic_dataset.csv'

# conferir se o arquivo existe antes de dar erro
if os.path.exists(arquivo_csv):
    # lendo a tabela do titanic
    tabela = pd.read_csv(arquivo_csv)

    # LIMPEZA DOS DADOS
    # preenchendo as idades vazias com a mediana
    valor_do_meio = tabela['Age'].median()
    tabela['Age'] = tabela['Age'].fillna(valor_do_meio)

    # tirando a coluna da cabine que tem muito erro
    tabela = tabela.drop(columns=['Cabin'])

    # tirando linhas que não tem o porto de embarque
    tabela.dropna(subset=['Embarked'], inplace=True)

    # TRABALHANDO COM A FAMÍLIA (SibSp e Parch)
    # vou somar os parentes pra ver quem tava sozinho
    tabela['Soma_Parentes'] = tabela['SibSp'] + tabela['Parch']
    
    # lógica simples pra ver se está sozinho ou não
    tabela.loc[tabela['Soma_Parentes'] == 0, 'Como_Viajava'] = 'Sozinho'
    tabela.loc[tabela['Soma_Parentes'] > 0, 'Como_Viajava'] = 'Com Familia'

    # PARTE DOS GRÁFICOS
    # Gráfico 1 - Sobrevivência por Classe e Sexo
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    
    # cores que o professor pediu: vermelho mulher e azul homem
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