from flask import Flask, redirect, render_template, request, url_for # type: ignore

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

productos = []
categorias = []
proveedores = []
bodegas = []




@app.route('/registro_producto', methods=['GET', 'POST'])
def registro_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock_inicial = int(request.form['stock_inicial'])
        categoria = request.form['categoria']

        producto = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'stock_inicial': stock_inicial,
            'categoria': categoria
        }

        productos.append(producto)
        return redirect(url_for('index'))
    else:
        return render_template('registro_producto.html')


@app.route('/registro_categoria', methods=['GET', 'POST'])
def registro_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        categoria = {'nombre': nombre, 'descripcion': descripcion}
        categorias.append(categoria)
        return redirect(url_for('index'))
    else:
        return render_template('registro_categoria.html')


@app.route('/registro_proveedor', methods=['GET', 'POST'])
def registro_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        productos_suministrados = request.form[
            'productos_suministrados'].split(',')

        proveedor = {
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono,
            'productos_suministrados': productos_suministrados
        }

        proveedores.append(proveedor)
        return redirect(url_for('index'))
    else:
        return render_template('registro_proveedor.html')


@app.route('/registro_bodega', methods=['GET', 'POST'])
def registro_bodega():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad_maxima = int(request.form['capacidad_maxima'])
        productos_almacenados = request.form['productos_almacenados'].split(
            ',')

        bodega = {
            'nombre': nombre,
            'ubicacion': ubicacion,
            'capacidad_maxima': capacidad_maxima,
            'productos_almacenados': productos_almacenados
        }

        bodegas.append(bodega)
        return redirect(url_for('index'))
    else:
        return render_template('registro_bodega.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
