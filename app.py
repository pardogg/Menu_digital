from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secreto_seguro"  # Necesario para gestionar sesiones

# Simulación de base de datos de productos
productos = [
    {"nombre": "Pizza", "descripcion": "Deliciosa pizza de pepperoni", "precio": 12000, "imagen": "pizza.jpg"},
    {"nombre": "Hamburguesa", "descripcion": "Hamburguesa con queso y papas", "precio": 15000, "imagen": "hamburguesa.jpg"},
    {"nombre": "Pasta", "descripcion": "Pasta Alfredo con pollo", "precio": 18000, "imagen": "pasta.jpg"},
]

pedidos = []  # Lista para almacenar los pedidos

# Simulación de base de datos de usuarios
usuarios = {
    "admin@restaurante.com": {"password": generate_password_hash("admin123"), "rol": "cocinero"},
    "usuario@cliente.com": {"password": generate_password_hash("cliente123"), "rol": "cliente"}
}

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    if "usuario" not in session:
        flash("Debes iniciar sesión para hacer un pedido", "danger")
        return redirect(url_for('login'))

    nombre = request.form.get('nombre')
    orden = request.form.get('orden')

    if not nombre or not orden:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('index'))

    pedido = {"nombre": nombre, "orden": orden, "estado": "En preparación"}
    pedidos.append(pedido)
    flash("Pedido realizado con éxito", "success")
    return redirect(url_for('index'))

@app.route('/cocina')
def cocina():
    if "usuario" not in session or session.get("rol") != "cocinero":
        flash("Acceso denegado. Solo el personal de cocina puede acceder.", "danger")
        return redirect(url_for('login'))
    
    return render_template('cocina.html', pedidos=pedidos)

@app.route('/actualizar_pedido', methods=['POST'])
def actualizar_pedido():
    if "usuario" not in session or session.get("rol") != "cocinero":
        return jsonify({"error": "Acceso denegado"}), 403

    try:
        pedido_id = int(request.json.get('pedido_id'))
        if 0 <= pedido_id < len(pedidos):
            pedidos[pedido_id]['estado'] = "Listo"
            return jsonify({"message": "Pedido actualizado"})
        else:
            return jsonify({"error": "Pedido no encontrado"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "ID de pedido inválido"}), 400

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = usuarios.get(email)
        if usuario and check_password_hash(usuario["password"], password):
            session["usuario"] = email
            session["rol"] = usuario["rol"]
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('index'))
        else:
            flash("Credenciales incorrectas", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
