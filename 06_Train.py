# ML
from sklearn.ensemble import RandomForestClassifier #modelo usado
from sklearn.pipeline import Pipeline #para fazer o pipeline
from sklearn.compose import ColumnTransformer # separar cat e num
from sklearn.impute import SimpleImputer #para inputar valores
from sklearn.preprocessing import StandardScaler, OneHotEncoder

#Core
import pandas as pd
import category_encoders as ce #lib para encodar as categoricas, tipo one hot encoder
import joblib # lib que serializa

target = 'Acidente Fatal',
cat_features = [
    'Turno','Município','Jurisdição','Administração','Conservação',
    'Condições Climáticas', 'Iluminação', 'Mão de direção', 
    'Relevo','Superfície da via', 'Tipo de pavimento', 'Tipo de pista', 'Traçado',
    'Tipo de Via'
]
num_features = ['Ano','Latitude', 'Longitude','Mes_sin', 'Mes_cos','dias_semana_sin','dias_semana_cos','horario_sin','horario_cos' #passar um scale nessas variáveis?
]

def load_data():
    df = pd.read_csv('CSVs/train.csv')
    X = df[cat_features + num_features]
    y = df[target]
    return X, y

def get_model_pipeline(): # aqui estamos criando um pipeline apenas para agrupar diferentes tratativas no modelo com scalers, pré processamentos e outros além do modelo em si
    #caso seja só um modelo, é possível chamar ele direto no joblib abaixo
    cat_transformer = Pipeline([('TargetEncoder',ce.TargetEncoder())])# apenas um exemplo
    num_transformer = Pipeline([
        ('Imputer',SimpleImputer(strategy='mean')),# exemplo
        ('Scaler',StandardScaler())# exemplo
    ])

    processor = ColumnTransformer([
        ('categorical',cat_transformer,cat_features),# exemplo
        ('numeric',num_transformer,num_features)# exemplo
    ])
    pipeline = Pipeline(steps=[('processor',processor),('classifier',RandomForestClassifier())])
    return pipeline

def main():
    print('[INFO] Start train script...')
    print('[INFO] Loading data...')
    X,y=load_data()
    print('[INFO] Training model...')
    pipeline = get_model_pipeline()
    pipeline.fit(X,y)
    print('[INFO] Saving the model pipeline artifact')
    joblib.dump(pipeline,'Models/model_vo.joblib')
    print('Train Script finished')

if __name__ == '__main__':
    main()