from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cargar el modelo y el codificador
with open('RNA_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('label_encoders.pkl', 'rb') as le_file:
    label_encoders = pickle.load(le_file)

# Cargar el escalador
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Convertir el JSON a un DataFrame
    df = pd.DataFrame([data])

    # Codificar las variables categóricas
    for column, le in label_encoders.items():
        df[column] = le.transform(df[column])
    
    # Escalar los datos
    df_scaled = scaler.transform(df)

    # Hacer la predicción
    prediction = model.predict(df_scaled)
    
    return jsonify({'prediction': 'Mayor de 50K' if prediction[0] == 1 else 'Menor o igual a 50K'})

if __name__ == '__main__':
    app.run(debug=True)
