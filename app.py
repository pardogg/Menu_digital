from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('menu.html')

@app.route('/opcion1')
def opcion1():
    return "Función 1: Aquí puedes ver el contenido de la opción 1"

@app.route('/opcion2')
def opcion2():
    return "Función 2: Aquí puedes ver el contenido de la opción 2"

@app.route('/opcion3')
def opcion3():
    return "Función 3: Aquí puedes ver el contenido de la opción 3"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
