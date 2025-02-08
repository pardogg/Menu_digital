from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import Cliente
from flask_login import login_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        apartamento = request.form['apartamento']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        nuevo_cliente = Cliente(nombre=nombre, email=email, apartamento=int(apartamento), password_hash=hashed_password)
        db.session.add(nuevo_cliente)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')
