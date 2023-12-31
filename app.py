from flask import Flask, render_template, request
import joblib
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Cargar el modelo previamente entrenado
loaded_model = joblib.load('modelo_ridge.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    feature_importance_plot = None

    if request.method == 'POST':
        # Obtener los datos ingresados por el usuario
        area = float(request.form['area'])
        rooms = int(request.form['rooms'])
        bathroom = int(request.form['bathroom'])
        parking_spaces = int(request.form['parking_spaces'])
        animal = int(request.form['animal'])  # Ajusta esto según tus opciones
        furniture = int(request.form['furniture'])  # Ajusta esto según tus opciones

        # Realizar una predicción de precio de alquiler
        data = [[area, rooms, bathroom, parking_spaces, animal, furniture]]
        prediction = loaded_model.predict(data)[0]

        # Crear un gráfico de importancia de características
        feature_importance_plot = create_feature_importance_plot(loaded_model, data)

        return render_template('index.html', prediction=prediction, feature_importance_plot=feature_importance_plot.decode('utf8'))

    return render_template('index.html', prediction=None, feature_importance_plot=None)

def create_feature_importance_plot(model, data):
    features = ['area', 'rooms', 'bathroom', 'parking spaces', 'animal_not acept', 'furniture_not furnished']
    importances = model.coef_  # Obtener las importancias de las características del modelo
    plt.barh(features, importances)
    plt.xlabel('Importancia')
    plt.title('Importancia de las Características')
    
    # Convertir el gráfico a una representación base64 para mostrarlo en HTML
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.read())

if __name__ == '__main__':
    app.run(debug=True)
