from flask import Flask, render_template, request, jsonify
import sqlite3
import qrcode
import os

app = Flask(__name__)

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      item TEXT,
                      status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()
    conn.close()
    return render_template('index.html', menu=menu_items)

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (item, status) VALUES (?, ?)", (data['item'], 'En preparación'))
    conn.commit()
    conn.close()
    return jsonify({"message": "Pedido recibido"})

@app.route('/kitchen')
def kitchen():
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return render_template('kitchen.html', orders=orders)

@app.route('/update_order', methods=['POST'])
def update_order():
    data = request.json
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (data['status'], data['id']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Estado actualizado"})

def generate_qr():
    url = "http://localhost:5000"
    qr = qrcode.make(url)
    qr.save("static/qr_code.png")

if __name__ == '__main__':
    init_db()
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    generate_qr()
    app.run(debug=True)
