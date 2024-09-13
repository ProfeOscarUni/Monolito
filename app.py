from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

# Ruta para la URL raíz
@app.route('/')
def index():
    return jsonify({'mensaje': 'Bienvenido a la API de Electrodomésticos'})

# Rutas
@app.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'precio': p.precio} for p in productos])

@app.route('/carrito', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json()
    usuario_id = data['usuario_id']
    producto_id = data['producto_id']
    cantidad = data['cantidad']

    # Verificar si el producto existe
    
    # Crear un nuevo item en el carrito
    nuevo_item = Carrito(usuario_id=usuario_id, producto_id=producto_id, cantidad=cantidad)
    db.session.add(nuevo_item)
    db.session.commit()

    return jsonify({'mensaje': 'Producto agregado al carrito'}), 201

   
@app.route ('/carrito/<int:usuario_id>', methods=['GET'])
def obtener_carrito(usuario_id):
    try:
        carrito_items = Carrito.query.filter_by(usuario_id=usuario_id).all()
        productos_en_carrito = []
        for item in carrito_items:
            producto = Producto.query.get(item.producto_id)
            if producto:
                productos_en_carrito.append({'id':producto.id, 'nombre': producto.nombre, 'precio': producto.precio, 'cantidad':item.cantidad})
        return jsonify(productos_en_carrito), 200
    except Exception as e:
        print(f"Error al obtener el carrito: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500


@app.route('/pago', methods=['POST'])
def procesar_pago():
    # Aquí iría la lógica de procesamiento de pago
    return jsonify({'mensaje': 'Pago procesado exitosamente'}), 200

if __name__ == '__main__':
    # Crear la base de datos y las tablas si no existen
    with app.app_context():
        db.create_all()

    app.run(debug=True)
