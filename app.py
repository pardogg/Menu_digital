from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para manejar sesiones

# Simulación de base de datos (En producción, usar una base de datos real)
productos = [
    {"nombre": "Pizza", "descripcion": "Deliciosa pizza de pepperoni", "precio": 12000, "imagen": "pizza.jpg"},
    {"nombre": "Hamburguesa", "descripcion": "Hamburguesa con queso y papas", "precio": 15000, "imagen": "hamburguesa.jpg"},
    {"nombre": "Pasta", "descripcion": "Pasta Alfredo con pollo", "precio": 18000, "imagen": "pasta.jpg"},
]

usuarios = {}  # Diccionario para almacenar usuarios
pedidos = []  # Lista de pedidos

@app.route('/')
def index():
    try:
        return render_template('index.html', productos=productos)
    except Exception as e:
        return f"Error al renderizar la página: {str(e)}", 500

@app.route('/registro', methods=['POST'])
def registro():
    email = request.form.get('email').strip().lower()
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

    usuarios[email] = {
        "password": generate_password_hash(password),
        "nombre": nombre,
        "apartamento": apartamento
    }

    session['usuario'] = email  # Mantener al usuario autenticado
    flash("Registro exitoso. Ahora puedes hacer pedidos.", "success")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('index'))

@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    email = request.form.get('email', '').strip()
    orden = request.form.get('orden', '').strip()

    if not email or not orden:
        flash("Debes estar registrado y proporcionar un pedido.", "danger")
        return redirect(url_for('index'))
    
    orden = request.form.get('orden')
    if not orden:
        flash("No puedes hacer un pedido vacío.", "danger")
        return redirect(url_for('index'))

    # Validar que el producto exista en el catálogo
    if not any(p["nombre"] == orden for p in productos):
        flash("El producto seleccionado no está disponible.", "danger")
        return redirect(url_for('index'))

    pedido = {
        "nombre": usuarios[email]["nombre"],
        "orden": orden,
        "apartamento": usuarios[email]["apartamento"],
        "estado": "En preparación"
    }
    pedidos.append(pedido)

    flash("Pedido realizado con éxito.", "success")
    return redirect(url_for('index'))

@app.route('/cocina')
def cocina():
    try:
        return render_template('cocina.html', pedidos=pedidos if pedidos else [])
    except Exception as e:
        return f"Error al cargar la cocina: {str(e)}", 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Usa el puerto de Render si está disponible
    app.run(host='0.0.0.0', port=port)
