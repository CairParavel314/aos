# Flask real local server

# Import library
from flask import Flask, jsonify, Response, request

# Tool for work with XML files
import xmltodict

# Name of app
app = Flask(__name__)

# Data of users (students)

students_db = [
    # Data from student 1
    {
        "id": 1,
        "name": "Pedro Paramo",
        "carrer": "ISOFT",
        "quarter": 2,
        "grade": 9.0,
        "email": "pedro.paramo@univ.mx",
        "age": 19,
        "active": True,
    },
    # Data from student 2
    {
        "id": 2,
        "name": "Aureliano Buendia",
        "carrer": "LNA",
        "quarter": 3,
        "grade": 7.5,
        "email": "aurealiano.bd@univ.mx",
        "age": 22,
        "active": False,
    },
]


# Creating a route (web/app/site)
@app.route("/")  # Main page
def first_page():
    return """
        <h1> Students Server </h1>
        <p> Pages </p>
        <ul> 
            <li> <a href="/api/campus"> All campus </a> </li>
            <li> <a href="/api/campus/1"> Student 1 </a> </li>
            <li> <a href="/api/campus/2"> Student 2 </a> </li>
            <li> <a href="/api/campus/xml"> XML Format </a> </li>
        
        </ul>
           """


# Page to access all data
@app.route("/api/campus")
def campus():
    return jsonify({"stutdents_total": len(students_db), "students": students_db})


# Page to access one student
@app.route("/api/campus/<int:student_id>")
def student_for_id(student_id):
    # Search/get all the students
    for student in students_db:
        if student["id"] == student_id:
            return jsonify({"found": True, "student": student})
    return (
        jsonify(
            {
                "found": False,
                "error": f"Student with {student_id} not found",
                "student": student,
                "error_code": 404,
            }
        ),
        404,
    )


# Page to make request/filter
@app.route("/api/campus/filter")
def filter_students():
    # Stablish params
    carrer = request.args.get("carrer", "").upper()
    name = request.args.get("name", "").lower()
    quarter = request.args.get("quarter", "")
    active = request.args.get("active", "")

    filter_students = []

    for student in students_db:
        filter_carrer = not carrer or student["carrer"] == carrer
        filter_name = not name or name in student["name"].lower()
        filter_quarter = not quarter or str(student["quarter"]) == quarter
        filter_active = not active or str(student["active"]).lower() == active.lower()

        if filter_carrer and filter_name and filter_quarter and filter_active:
            filter_students.append(student)
            return jsonify(
                {"total_found": len(filter_students), "student": filter_students}
            )

#XML Format
@app.route("/api/campus/xml")
def student_xml():
    # Formato específico que xmltodict acepta bien
    data = {
        'response': {
            'status': 'success',
            'data': {
                'estudiantes': students_db
            }
        }
    }
    xml_data = xmltodict.unparse(data, pretty=True)
    return Response(xml_data, mimetype='application/xml')
    

# Starts the app
if __name__ == "__main__":
    app.run(debug=True)
