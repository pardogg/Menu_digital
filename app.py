from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Lista para almacenar los pedidos temporalmente
pedidos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pedidos', methods=['GET', 'POST'])
def gestionar_pedidos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        orden = request.form['orden']
        pedidos.append({'nombre': nombre, 'orden': orden, 'estado': 'En preparación'})
        return redirect(url_for('gestionar_pedidos'))
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/actualizar_pedido', methods=['POST'])
def actualizar_pedido():
    data = request.json
    pedido_id = int(data['pedido_id'])
    pedidos[pedido_id]['estado'] = 'Listo'
    return jsonify({'message': 'Pedido actualizado'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
