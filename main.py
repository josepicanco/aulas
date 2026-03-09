import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Caminho do arquivo
arquivo = 'titanic_dataset.csv'

if not os.path.exists(arquivo):
    print(f"ERRO: O arquivo '{arquivo}' não foi encontrado na pasta!")
else:
    # Carregando o dataset
    dados = pd.read_csv(arquivo)

    # 2. Limpeza e Tratamento
    dados['Age'] = dados['Age'].fillna(dados['Age'].median())
    dados.drop(columns=['Cabin'], inplace=True, errors='ignore')
    dados.dropna(subset=['Embarked'], inplace=True)

    # 3. Análise de Família (SibSp e Parch)
    # Criando lógica de quem viaja sozinho ou acompanhado
    dados['Parentes'] = dados['SibSp'] + dados['Parch']
    dados['Status_Viagem'] = dados['Parentes'].apply(lambda x: 'Sozinho' if x == 0 else 'Com Família')

    # 4. Gráfico 1: Sobrevivência por Classe e Sexo
    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)
    
    # Cores: Vermelho para mulheres, Azul para homens
    cores_br = {"female": "#d62728", "male": "#1f77b4"} 
    
    # ci=None remove as setas/linhas pretas de erro
    sns.barplot(data=dados, x='Pclass', y='Survived', hue='Sex', 
                palette=cores_br, errorbar=None)
    
    plt.title('Taxa de Sobrevivência por Classe e Sexo')
    plt.xlabel('Classe (1ª, 2ª e 3ª)')
    plt.ylabel('Percentual de Sobrevivência')
    plt.legend(title='Legenda de Cores', labels=['Masculino (Azul)', 'Feminino (Vermelho)'])

    # 5. Gráfico 2: Porto de Embarque (Nomes Reais)
    plt.subplot(1, 2, 2)
    mapeamento_portos = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}
    dados['Porto_Nome'] = dados['Embarked'].map(mapeamento_portos)

    sns.countplot(data=dados, x='Porto_Nome', hue='Survived', palette='viridis')
    plt.title('Sobrevivência por Porto de Embarque')
    plt.xlabel('Porto')
    plt.ylabel('Quantidade')
    plt.legend(title='Sobreviveu', labels=['Não', 'Sim'])

    plt.tight_layout()
    plt.show()

    # 6. Gráfico 3: Análise de Parentes (Sozinho vs Família)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=dados, x='Status_Viagem', y='Survived', palette='Set2', errorbar=None)
    plt.title('Influência de Parentes na Sobrevivência')
    plt.ylabel('Taxa de Sobrevivência')
    plt.show()

    print("\nExecução Finalizada com Sucesso.")