from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Datos de ejemplo
productos = []
categorias = []
proveedores = []
bodegas = []

@app.route('/')
def index():
    return render_template('index.html', view='home', productos=productos, categorias=categorias, proveedores=proveedores, bodegas=bodegas)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            "id": len(productos) + 1,
            "nombre": request.form['nombre'],
            "descripcion": request.form['descripcion'],
            "precio": float(request.form['precio']),
            "stock": int(request.form['stock']),
            "categoria": request.form['categoria'],
            "proveedor": request.form['proveedor']
        }
        productos.append(nuevo_producto)
        return redirect(url_for('index'))
    return render_template('agregar_producto.html', categorias=categorias, proveedores=proveedores)

@app.route('/agregar_categoria', methods=['GET', 'POST'])
def agregar_categoria():
    if request.method == 'POST':
        nueva_categoria = {
            "id": len(categorias) + 1,
            "nombre": request.form['nombre'],
            "descripcion": request.form['descripcion'],
            "productos": []
        }
        categorias.append(nueva_categoria)
        return redirect(url_for('index'))
    return render_template('agregar_categoria.html')

@app.route('/agregar_proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == 'POST':
        nuevo_proveedor = {
            "id": len(proveedores) + 1,
            "nombre": request.form['nombre'],
            "direccion": request.form['direccion'],
            "telefono": request.form['telefono'],
            "productos": []
        }
        proveedores.append(nuevo_proveedor)
        return redirect(url_for('index'))
    return render_template('agregar_proveedor.html')

@app.route('/agregar_bodega', methods=['GET', 'POST'])
def agregar_bodega():
    if request.method == 'POST':
        nueva_bodega = {
            "id": len(bodegas) + 1,
            "nombre": request.form['nombre'],
            "ubicacion": request.form['ubicacion'],
            "capacidad_max": int(request.form['capacidad_max']),
            "productos": []
        }
        bodegas.append(nueva_bodega)
        return redirect(url_for('index'))
    return render_template('agregar_bodega.html')

@app.route('/producto/<int:id>')
def producto(id):
    prod = next((p for p in productos if p["id"] == id), None)
    return render_template('index.html', view='producto', producto=prod)

@app.route('/categoria/<int:id>')
def categoria(id):
    cat = next((c for c in categorias if c["id"] == id), None)
    productos_cat = [p for p in productos if p["categoria"] == cat["nombre"]]
    return render_template('index.html', view='categoria', categoria=cat, productos=productos_cat)

@app.route('/proveedor/<int:id>')
def proveedor(id):
    prov = next((p for p in proveedores if p["id"] == id), None)
    productos_prov = [p for p in productos if p["proveedor"] == prov["nombre"]]
    return render_template('index.html', view='proveedor', proveedor=prov, productos=productos_prov)

@app.route('/bodega/<int:id>')
def bodega(id):
    bod = next((b for b in bodegas if b["id"] == id), None)
    productos_bod = [p for p in productos if p["id"] in bod["productos"]]
    return render_template('index.html', view='bodega', bodega=bod, productos=productos_bod)

@app.route('/reportes')
def reportes():
    stock_total = sum(p["stock"] for p in productos)
    stock_por_categoria = {c["nombre"]: sum(p["stock"] for p in productos if p["categoria"] == c["nombre"]) for c in categorias}
    stock_por_proveedor = {p["nombre"]: sum(prod["stock"] for prod in productos if prod["proveedor"] == p["nombre"]) for p in proveedores}
    stock_por_bodega = {b["nombre"]: sum(prod["stock"] for prod in productos if prod["id"] in b["productos"]) for b in bodegas}
    return render_template('index.html', view='reportes', stock_total=stock_total, stock_por_categoria=stock_por_categoria, stock_por_proveedor=stock_por_proveedor, stock_por_bodega=stock_por_bodega)

if __name__ == "__main__":
    app.run(port=5001)  # Cambia el puerto al 5001 (o cualquier otro puerto disponible)

