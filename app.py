from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='cliente')

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    productos = [
        {'nombre': 'Pizza', 'descripcion': 'Pizza con queso y tomate', 'precio': 10, 'imagen': 'pizza.jpg'},
        {'nombre': 'Hamburguesa', 'descripcion': 'Hamburguesa con carne y queso', 'precio': 8, 'imagen': 'burger.jpg'}
    ]
    return render_template('index.html', productos=productos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('index'))

@app.route('/cocina')
def cocina():
    if 'user_id' not in session or session.get('role') != 'cocinero':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('index'))
    return render_template('cocina.html')

@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    nombre = request.form['nombre']
    orden = request.form['orden']
    flash(f'Pedido realizado por {nombre}: {orden}', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
