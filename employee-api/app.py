from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# --- Load Employees from JSON ---
def load_employees():
    with open("employees.json", "r") as file:
        return json.load(file)

# --- Root Route (Home) ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Employee API",
        "routes": {
            "/employees": "Get all employees",
            "/employees/department?dept=Engineering": "Filter by department",
            "/employees/highest-paid": "Get highest paid employee",
            "/employees/location?loc=Hyderabad": "Filter by location",
            "/employees/salary?min=50000": "Filter by minimum salary"
        }
    })

# --- All Employees ---
@app.route("/employees", methods=["GET"])
def get_all_employees():
    return jsonify(load_employees())

# --- Filter by Department ---
@app.route("/employees/department", methods=["GET"])
def get_by_department():
    dept = request.args.get("dept")
    if not dept:
        return jsonify({"error": "Please provide a department via 'dept' query param"}), 400
    data = load_employees()
    filtered = [emp for emp in data if emp["department"].lower() == dept.lower()]
    return jsonify(filtered)

# --- Highest Paid Employee ---
@app.route("/employees/highest-paid", methods=["GET"])
def highest_paid_employee():
    data = load_employees()
    top_emp = max(data, key=lambda emp: emp["salary"])
    return jsonify(top_emp)

# --- Search by Location ---
@app.route("/employees/location", methods=["GET"])
def search_by_location():
    loc = request.args.get("loc")
    if not loc:
        return jsonify({"error": "Please provide a location via 'loc' query param"}), 400
    data = load_employees()
    filtered = [emp for emp in data if emp["location"].lower() == loc.lower()]
    return jsonify(filtered)

# --- Filter by Salary Greater Than ---
@app.route("/employees/salary", methods=["GET"])
def filter_by_salary():
    min_salary = request.args.get("min")
    if not min_salary:
        return jsonify({"error": "Please provide min salary via 'min' query param"}), 400
    try:
        threshold = float(min_salary)
    except ValueError:
        return jsonify({"error": "Invalid salary value"}), 400
    data = load_employees()
    filtered = [emp for emp in data if emp["salary"] >= threshold]
    return jsonify(filtered)

if __name__ == "__main__":
    app.run(debug=True)
