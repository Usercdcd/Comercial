from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Datos simulados
categorias = {
    "Electrónica": [],
    "Ropa": []
}

proveedores = {
    "Proveedor A": [],
    "Proveedor B": []
}

bodegas = {
    "Bodega 1": {"capacidad": 100, "productos": {}},
    "Bodega 2": {"capacidad": 50, "productos": {}}
}

@app.route('/')
def index():
    # Renderiza la plantilla index.html con los datos de categorías, proveedores y bodegas
    return render_template('index.html', categorias=categorias, proveedores=proveedores, bodegas=bodegas)

@app.route('/agregar_producto_categoria', methods=['POST'])
def agregar_producto_categoria():
    # Agrega un producto a una categoría específica
    categoria = request.form['categoria']
    producto = request.form['producto']

    if categoria in categorias:
        categorias[categoria].append(producto)
        return redirect(url_for('index'))
    return jsonify({"message": "Categoría no encontrada"}), 404

@app.route('/eliminar_producto_categoria', methods=['POST'])
def eliminar_producto_categoria():
    # Elimina un producto de una categoría específica
    categoria = request.form['categoria']
    producto = request.form['producto']

    if categoria in categorias and producto in categorias[categoria]:
        categorias[categoria].remove(producto)
        return redirect(url_for('index'))
    return jsonify({"message": "Categoría o producto no encontrado"}), 404

@app.route('/agregar_producto_proveedor', methods=['POST'])
def agregar_producto_proveedor():
    # Agrega un producto a un proveedor específico
    proveedor = request.form['proveedor']
    producto = request.form['producto']

    if proveedor in proveedores:
        proveedores[proveedor].append(producto)
        return redirect(url_for('index'))
    return jsonify({"message": "Proveedor no encontrado"}), 404

@app.route('/eliminar_producto_proveedor', methods=['POST'])
def eliminar_producto_proveedor():
    # Elimina un producto de un proveedor específico
    proveedor = request.form['proveedor']
    producto = request.form['producto']

    if proveedor in proveedores and producto in proveedores[proveedor]:
        proveedores[proveedor].remove(producto)
        return redirect(url_for('index'))
    return jsonify({"message": "Proveedor o producto no encontrado"}), 404

@app.route('/agregar_producto_bodega', methods=['POST'])
def agregar_producto_bodega():
    # Agrega un producto a una bodega específica
    bodega = request.form['bodega']
    producto = request.form['producto']
    cantidad = int(request.form['cantidad'])

    if bodega in bodegas:
        bodega_data = bodegas[bodega]
        if sum(bodega_data['productos'].values()) + cantidad <= bodega_data['capacidad']:
            if producto in bodega_data['productos']:
                bodega_data['productos'][producto] += cantidad
            else:
                bodega_data['productos'][producto] = cantidad
            return redirect(url_for('index'))
        return jsonify({"message": "No hay suficiente espacio en la bodega"}), 400
    return jsonify({"message": "Bodega no encontrada"}), 404

@app.route('/retirar_producto_bodega', methods=['POST'])
def retirar_producto_bodega():
    # Retira un producto de una bodega específica
    bodega = request.form['bodega']
    producto = request.form['producto']
    cantidad = int(request.form['cantidad'])

    if bodega in bodegas and producto in bodegas[bodega]['productos']:
        if bodegas[bodega]['productos'][producto] >= cantidad:
            bodegas[bodega]['productos'][producto] -= cantidad
            return redirect(url_for('index'))
        return jsonify({"message": "Cantidad a retirar excede el stock disponible"}), 400
    return jsonify({"message": "Bodega o producto no encontrado"}), 404

@app.route('/consultar_disponibilidad', methods=['GET'])
def consultar_disponibilidad():
    # Consulta la disponibilidad de un producto en una bodega específica
    bodega = request.args.get('bodega')
    producto = request.args.get('producto')

    if bodega in bodegas and producto in bodegas[bodega]['productos']:
        cantidad_disponible = bodegas[bodega]['productos'][producto]
        return jsonify({"producto": producto, "cantidad": cantidad_disponible}), 200
    return jsonify({"message": "Bodega o producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
