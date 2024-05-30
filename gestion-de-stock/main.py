# main.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para almacenar los registros de productos
productos = []

@app.route('/')
def index():
    # Mostrar una lista de productos con su información
    return render_template('index.html', productos=productos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        # Crear un nuevo producto y agregarlo a la lista de productos
        producto = {'nombre': nombre, 'precio': precio, 'stock': stock}
        productos.append(producto)

        return redirect(url_for('index'))
    else:
        return render_template('agregar_producto.html')

@app.route('/agregar_stock/<int:id_producto>', methods=['POST'])
def agregar_stock(id_producto):
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])

        # Buscar el producto por su ID
        producto = productos[id_producto]

        # Actualizar el stock del producto
        producto['stock'] += cantidad

        return redirect(url_for('index'))

@app.route('/retirar_stock/<int:id_producto>', methods=['POST'])
def retirar_stock(id_producto):
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])

        # Buscar el producto por su ID
        producto = productos[id_producto]

        # Verificar si hay suficiente stock para retirar
        if cantidad <= producto['stock']:
            # Actualizar el stock del producto
            producto['stock'] -= cantidad

        return redirect(url_for('index'))

@app.route('/valor_total_stock')
def valor_total_stock():
    total = sum(producto['precio'] * producto['stock'] for producto in productos)
    return f'Valor total del stock: {total}'

if __name__ == '__main__':
    app.run(debug=True)
