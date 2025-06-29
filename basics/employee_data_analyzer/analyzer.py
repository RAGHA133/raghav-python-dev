def read_employees(file_path):
    employees = []
    with open(file_path, "r") as file:
        next(file)
        for line in file:
            name,age,dept,salary = line.strip().split(",")
            employees.append({
                "name": name,
                "age": int(age),
                "department": dept,
                "salary": int(salary)
            })
    return employees

def filter_by_department(employees, department):
    return [emp for emp in employees if emp["department"].lower() == department.lower()]

def calculate_average_salary(employees):
    if not employees:
        return 0
    total_salary = sum(emp["salary"] for emp in employees)
    return total_salary / len(employees)

def highest_paid_employee(employees):
    return max(employees, key=lambda emp: emp["salary"])


if __name__ == "__main__":
    emp_list = read_employees("employees.csv")

    print("All Employees:")
    for emp in emp_list:
        print(emp)

    dept = input("\nEnter department to filter by (e.g., Engineering): ")
    filtered = filter_by_department(emp_list, dept)
    print(f"\nEmployees in {dept} department:")
    for emp in filtered:
        print(emp)

    avg_salary = calculate_average_salary(filtered)
    print(f"\nAverage salary in {dept}: {avg_salary:.2f}")

    top_emp = highest_paid_employee(emp_list)
    print(f"\nHighest paid employee: {top_emp['name']} - ₹{top_emp['salary']}")