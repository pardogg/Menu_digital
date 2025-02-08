from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de una base de datos (esto debería estar en una base de datos real)
productos = [
    {"nombre": "Pizza", "descripcion": "Deliciosa pizza de pepperoni", "precio": 12000, "imagen": "pizza.jpg"},
    {"nombre": "Hamburguesa", "descripcion": "Hamburguesa con queso y papas", "precio": 15000, "imagen": "hamburguesa.jpg"},
    {"nombre": "Pasta", "descripcion": "Pasta Alfredo con pollo", "precio": 18000, "imagen": "pasta.jpg"},
]

pedidos = []  # Lista para almacenar los pedidos

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    nombre = request.form.get('nombre')
    orden = request.form.get('orden')

    if nombre and orden:
        pedido = {"nombre": nombre, "orden": orden, "estado": "En preparación"}
        pedidos.append(pedido)
        return redirect(url_for('cocina'))  # Redirige a la cocina

    return redirect(url_for('index'))

@app.route('/cocina')
def cocina():
    return render_template('cocina.html', pedidos=pedidos)

@app.route('/actualizar_pedido', methods=['POST'])
def actualizar_pedido():
    pedido_id = int(request.json.get('pedido_id'))  # Obtiene el ID del pedido desde JS
    if 0 <= pedido_id < len(pedidos):
        pedidos[pedido_id]['estado'] = "Listo"
    return {"message": "Pedido actualizado"}

if __name__ == '__main__':
    app.run(debug=True)
