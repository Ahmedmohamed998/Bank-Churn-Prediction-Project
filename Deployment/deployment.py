import streamlit as st
import pickle as pkl
import numpy as np
import time
models = {'logistic': pkl.load(open('notebooks/logistic.pkl', 'rb')),
          'Ada': pkl.load(open('notebooks/Ada.pkl', 'rb')),
          'Gradient': pkl.load(open('notebooks/Gradient.pkl', 'rb')),
          'knn': pkl.load(open('notebooks/knn.pkl', 'rb')),
          'svm': pkl.load(open('notebooks/svm.pkl', 'rb')),
          'stacking': pkl.load(open('notebooks/stacking.pkl', 'rb')),
          'XG': pkl.load(open('notebooks/XG.pkl', 'rb')),
          'decision_tree': pkl.load(open('notebooks/decision_tree.pkl', 'rb')),
          'bagging_different': pkl.load(open('notebooks/bagging_different.pkl', 'rb')),
          'Random_forest': pkl.load(open('notebooks/Random_forest.pkl', 'rb'))}

models_names = ['logistic', 'Ada', 'Gradient', 'knn', 'svm', 'stacking', 'XG', 'decision_tree', 'bagging_different', 'Random_forest']
scaler = pkl.load(open('notebooks/robustscaler.pkl', 'rb'))
power = pkl.load(open('notebooks/powertransformer.pkl', 'rb'))
input_features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard','IsActiveMember', 'EstimatedSalary']
col1_features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure']
col2_features = ['Balance','NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
cat_features = ['Geography', 'Gender']

def load_encoder(feature):
     return pkl.load(open(f'notebooks/{feature}.pkl', 'rb'))  
def main():
    st.title(":bank: Bank Churn Prediction") 
    col1, col2 = st.columns(2)
    inputs = {}
    
    for feature in col1_features:
        with col1:
            if feature in cat_features:
                 en = load_encoder(feature)
                 if hasattr(en, 'categories_'):
                    options = en.categories_[0].tolist()
                    inputs[feature] = st.selectbox(feature, options)
                 elif hasattr(en, 'classes_'):
                    options = en.classes_.tolist()
                    inputs[feature] = st.selectbox(feature, options)
            else:
                inputs[feature] = st.text_input(feature)
                
    for feature in col2_features:
        with col2:
            if feature in cat_features:
                 en = load_encoder(feature)
                 options = en.categories_[0].tolist()
                 inputs[feature] = st.selectbox(feature, options)
            elif feature in  ['HasCrCard', 'IsActiveMember']:
                inputs[feature] = st.selectbox(feature,[0,1])
            else:
                inputs[feature] = st.text_input(feature)
    model_choice = st.selectbox("Choose Model", models_names)
    model = models[model_choice]

    if st.button('Predict'):
        with st.spinner('Making prediction...'):
            time.sleep(0.8)
            features = []
            for feature in input_features:
                value = inputs[feature]
                if feature in cat_features:
                    en = load_encoder(feature)
                    value = en.transform(np.array([[value]]))[0]
                features.append(value)

            features = np.array(features, dtype='object').reshape(1, -1)
            features_scaled = power.transform(features)
            features_scaled = scaler.transform(features_scaled)

            y_pred = model.predict(features_scaled)
            if y_pred == 1:
                st.error('The customer is likely to churn.')
            else:
                st.success('The customer is likely to stay.')

if __name__ == '__main__':
    main()
