from flask import Flask, render_template, request, redirect, url_for, jsonify # type: ignore

app = Flask(__name__)

# Base de datos simulada con productos
productos = [
    {"nombre": "Pizza", "descripcion": "Pizza grande con queso y pepperoni", "precio": 10, "imagen": "pizza.jpg"},
    {"nombre": "Hamburguesa", "descripcion": "Hamburguesa con doble carne y queso", "precio": 8, "imagen": "hamburguesa.jpg"},
    {"nombre": "Pasta", "descripcion": "Pasta con salsa Alfredo y pollo", "precio": 9, "imagen": "pasta.jpg"},
    {"nombre": "Ensalada", "descripcion": "Ensalada fresca con aderezo de la casa", "precio": 7, "imagen": "ensalada.jpg"}
]

# Lista para almacenar pedidos
pedidos = []

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/pedido', methods=['POST'])
def realizar_pedido():
    nombre = request.form['nombre']
    orden = request.form['orden']
    pedidos.append({'nombre': nombre, 'orden': orden, 'estado': 'En preparación'})
    return redirect(url_for('index'))

@app.route('/cocina')
def cocina():
    return render_template('cocina.html', pedidos=pedidos)

@app.route('/actualizar_pedido', methods=['POST'])
def actualizar_pedido():
    data = request.json
    pedido_id = int(data['pedido_id'])
    pedidos[pedido_id]['estado'] = 'Listo'
    return jsonify({'message': 'Pedido actualizado'})

if __name__ == '__main__':
    app.run(debug=True)
