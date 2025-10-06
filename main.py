from flask import Flask, jsonify, Response, request
import xmltodict

app = Flask(__name__)

# Base de datos de estudiantes
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

@app.route('/')
def hola_mundo():
    return "¡API Flask funcionando en Render! 🚀"

@app.route('/api/estudiantes')
def todos_estudiantes():
    return jsonify({
        "total_estudiantes": len(students_db),
        "estudiantes": students_db
    })

@app.route('/api/estudiantes/<int:estudiante_id>')
def estudiante_por_id(estudiante_id):
    for estudiante in students_db:
        if estudiante["id"] == estudiante_id:
            return jsonify({
                "encontrado": True,
                "estudiante": estudiante
            })
    return jsonify({"error": "Estudiante no encontrado"}), 404

@app.route('/api/estudiantes/filtrar')
def filtrar_estudiantes():
    carrera = request.args.get('carrera', '').upper()
    nombre = request.args.get('nombre', '').lower()
    
    estudiantes_filtrados = []
    for estudiante in students_db:
        cumple_carrera = not carrera or estudiante['carrera'] == carrera
        cumple_nombre = not nombre or nombre in estudiante['nombre'].lower()
        
        if cumple_carrera and cumple_nombre:
            estudiantes_filtrados.append(estudiante)
    
    return jsonify({
        "filtros_aplicados": {"carrera": carrera, "nombre": nombre},
        "total_encontrados": len(estudiantes_filtrados),
        "estudiantes": estudiantes_filtrados
    })

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
    app.run(debug=False, host='0.0.0.0', port=5000)
