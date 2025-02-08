from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para manejar sesiones

# Simulación de base de datos (en un caso real, usar una base de datos real)
productos = [
    {"nombre": "Pizza", "descripcion": "Deliciosa pizza de pepperoni", "precio": 12000, "imagen": "pizza.jpg"},
    {"nombre": "Hamburguesa", "descripcion": "Hamburguesa con queso y papas", "precio": 15000, "imagen": "hamburguesa.jpg"},
    {"nombre": "Pasta", "descripcion": "Pasta Alfredo con pollo", "precio": 18000, "imagen": "pasta.jpg"},
]

usuarios = {}  # Diccionario para almacenar usuarios (email como clave)
pedidos = []  # Lista de pedidos

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/registro', methods=['POST'])
def registro():
    email = request.form.get('email')
    password = request.form.get('password')
    nombre = request.form.get('nombre')
    apartamento = request.form.get('apartamento')

    if not email or not password or not nombre or not apartamento:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('index'))

    try:
        apartamento = int(apartamento)  # Asegurar que sea un número entero
    except ValueError:
        flash("El apartamento debe ser un número entero", "danger")
        return redirect(url_for('index'))

    if email in usuarios:
        flash("El usuario ya está registrado, por favor inicie sesión", "warning")
        return redirect(url_for('index'))

    # Registrar usuario con contraseña encriptada
    usuarios[email] = {
        "password": generate_password_hash(password),
        "nombre": nombre,
        "apartamento": apartamento
    }

    flash("Registro exitoso. Ahora puedes hacer pedidos.", "success")
    return redirect(url_for('index'))

@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    email = request.form.get('email')
    orden = request.form.get('orden')

    if not email or not orden:
        flash("Debes estar registrado para hacer un pedido.", "danger")
        return redirect(url_for('index'))

    if email not in usuarios:
        flash("El usuario no está registrado, por favor regístrate primero.", "danger")
        return redirect(url_for('index'))

    pedido = {"nombre": usuarios[email]["nombre"], "orden": orden, "apartamento": usuarios[email]["apartamento"], "estado": "En preparación"}
    pedidos.append(pedido)
    
    flash("Pedido realizado con éxito.", "success")
    return redirect(url_for('index'))

@app.route('/cocina')
def cocina():
    return render_template('cocina.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
