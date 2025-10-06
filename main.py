from flask import Flask, jsonify, Response, request
import xmltodict

app = Flask(__name__)

# Base de datos de estudiantes (ahora con ID auto-incremental)
students_db = [
    {
        "id": 1,
        "nombre": "Ana García",
        "carrera": "ISW", 
        "semestre": 1,
        "promedio": 8.5,
        "email": "ana.garcia@universidad.edu",
        "edad": 20,
        "activo": True
    },
    {
        "id": 2,
        "nombre": "Carlos López",
        "carrera": "ISW",
        "semestre": 2, 
        "promedio": 9.0,
        "email": "carlos.lopez@universidad.edu",
        "edad": 22,
        "activo": True
    }
]

# Contador para IDs auto-incrementales
next_id = 3

@app.route('/')
def hola_mundo():
    return """
    <h1>🏫 API de Estudiantes - Flask</h1>
    <p>Rutas disponibles:</p>
    <ul>
        <li><strong>GET</strong> <a href="/api/estudiantes">/api/estudiantes</a> - Todos los estudiantes</li>
        <li><strong>GET</strong> <a href="/api/estudiantes/1">/api/estudiantes/1</a> - Estudiante por ID</li>
        <li><strong>GET</strong> <a href="/api/estudiantes/filtrar">/api/estudiantes/filtrar</a> - Con filtros</li>
        <li><strong>POST</strong> /api/estudiantes - Crear nuevo estudiante</li>
        <li><strong>GET</strong> <a href="/api/campus/xml">/api/campus/xml</a> - Versión XML</li>
    </ul>
    <p>Usa Postman para probar el método POST</p>
    """

# 📊 GET - TODOS LOS ESTUDIANTES
@app.route('/api/estudiantes', methods=['GET'])
def todos_estudiantes():
    return jsonify({
        "total_estudiantes": len(students_db),
        "estudiantes": students_db
    })

# ➕ POST - CREAR NUEVO ESTUDIANTE
@app.route('/api/estudiantes', methods=['POST'])
def crear_estudiante():
    global next_id
    
    try:
        # Obtener datos del request (JSON)
        datos = request.get_json()
        
        # Validar que vengan los datos requeridos
        if not datos:
            return jsonify({"error": "No se enviaron datos"}), 400
        
        if 'nombre' not in datos or 'carrera' not in datos:
            return jsonify({"error": "Faltan campos obligatorios: nombre, carrera"}), 400
        
        # Crear nuevo estudiante
        nuevo_estudiante = {
            "id": next_id,
            "nombre": datos['nombre'],
            "carrera": datos['carrera'],
            "semestre": datos.get('semestre', 1),
            "promedio": datos.get('promedio', 0.0),
            "email": datos.get('email', ''),
            "edad": datos.get('edad', 18),
            "activo": datos.get('activo', True)
        }
        
        # Agregar a la base de datos
        students_db.append(nuevo_estudiante)
        next_id += 1
        
        # Respuesta de éxito
        return jsonify({
            "mensaje": "Estudiante creado exitosamente",
            "estudiante": nuevo_estudiante,
            "total_estudiantes": len(students_db)
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Error al crear estudiante: {str(e)}"}), 500

# 🔍 GET - ESTUDIANTE POR ID
@app.route('/api/estudiantes/<int:estudiante_id>')
def estudiante_por_id(estudiante_id):
    for estudiante in students_db:
        if estudiante["id"] == estudiante_id:
            return jsonify({
                "encontrado": True,
                "estudiante": estudiante
            })
    
    return jsonify({
        "encontrado": False,
        "error": f"Estudiante con ID {estudiante_id} no encontrado"
    }), 404

# 🎯 GET - FILTRAR ESTUDIANTES
@app.route('/api/estudiantes/filtrar')
def filtrar_estudiantes():
    carrera = request.args.get('carrera', '').upper()
    nombre = request.args.get('nombre', '').lower()
    semestre = request.args.get('semestre', '')
    
    estudiantes_filtrados = []
    for estudiante in students_db:
        cumple_carrera = not carrera or estudiante['carrera'] == carrera
        cumple_nombre = not nombre or nombre in estudiante['nombre'].lower()
        cumple_semestre = not semestre or str(estudiante['semestre']) == semestre
        
        if cumple_carrera and cumple_nombre and cumple_semestre:
            estudiantes_filtrados.append(estudiante)
    
    return jsonify({
        "filtros_aplicados": {
            "carrera": carrera if carrera else "todas",
            "nombre": nombre if nombre else "ninguno",
            "semestre": semestre if semestre else "todos"
        },
        "total_encontrados": len(estudiantes_filtrados),
        "estudiantes": estudiantes_filtrados
    })

# 📄 GET - VERSIÓN XML
@app.route("/api/campus/xml")
def student_xml():
    data = {
        'estudiantes': {
            'estudiante': students_db
        }
    }
    xml_data = xmltodict.unparse(data, pretty=True)
    return Response(xml_data, mimetype='application/xml')

if __name__ == '__main__':
    print("🚀 Servidor Flask con POST iniciado!")
    print("📍 URL: http://127.0.0.1:5000")
    print("\n📝 Ejemplos POST para probar en Postman:")
    print("   POST http://127.0.0.1:5000/api/estudiantes")
    print("   Body (JSON):")
    print('   {"nombre": "Laura Torres", "carrera": "LIS", "semestre": 2}')
    app.run(debug=False, host='0.0.0.0', port=5000)
