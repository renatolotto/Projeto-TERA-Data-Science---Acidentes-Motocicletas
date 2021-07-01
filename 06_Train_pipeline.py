# ML
from sklearn.ensemble import RandomForestClassifier #modelo usado
from sklearn.pipeline import Pipeline #para fazer o pipeline
from sklearn.compose import ColumnTransformer # separar cat e num
# from sklearn.impute import SimpleImputer #para inputar valores
from sklearn.preprocessing import StandardScaler, OneHotEncoder

#Core
import pandas as pd
import category_encoders as ce #lib para encodar as categoricas, tipo one hot encoder
import joblib # lib que serializa

target = 'Acidente Fatal',
cat_features = ['Município','Condições Climáticas']
num_features = ['Latitude', 'Longitude','Mes_sin', 'Mes_cos','dias_semana_sin','horario_sin','horario_cos']

def load_data():
    X = pd.read_csv('Models\X_train.csv')
    y = pd.read_csv('Models\y_train.csv')
    return X, y


def get_model_pipeline():
    # cat_transformer = Pipeline([('TargetEncoder',ce.TargetEncoder())])
    # num_transformer = Pipeline([('Imputer',SimpleImputer(strategy='mean'))])
    processor = ColumnTransformer(transformers=[('categorical',ce.TargetEncoder(),cat_features)])#,('numeric',num_transformer,num_features)])
    
    pipeline = Pipeline(steps=[('processor',processor),('classifier',RandomForestClassifier(class_weight='balanced'))])
    return pipeline

def main():
    print('[INFO] Start train script...')
    print('[INFO] Loading data...')
    X,y=load_data()
    print('[INFO] Training model...')
    pipeline = get_model_pipeline()
    pipeline.fit(X,y)
    print('[INFO] Saving the model pipeline artifact')
    joblib.dump(pipeline,'Models/model3_v0.joblib')
    print('[INFO] Train Script finished')

# def main():
#     print('[INFO] Start train script...')
#     print('[INFO] Loading data...')
#     X,y=load_data()
#     print('[INFO] Encoding features...')
#     encoder = ce.TargetEncoder(cols=cat_features,smoothing=0, return_df=True)#,smoothing=0, return_df=True
#     X_proc = encoder.fit_transform(X,y)
#     print('[INFO] Training model...')
#     classifier = RandomForestClassifier(class_weight='balanced')
#     classifier.fit(X_proc,y)
#     print('[INFO] Saving the encoder artifact')
#     joblib.dump(encoder,'Models/encoder_v0.joblib')
#     print('[INFO] Saving the model artifact')
#     joblib.dump(classifier,'Models/classifier_v0.joblib')
#     print('[INFO] Train Script finished')


if __name__ == '__main__':
    main()