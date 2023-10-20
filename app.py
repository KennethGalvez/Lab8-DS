from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Cargar el modelo previamente entrenado
loaded_model = joblib.load('modelo_ridge.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
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

        return render_template('index.html', prediction=prediction)

    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
