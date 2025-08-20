import sys
students = {
    "Math": [("Alice", 67)],
    "Science": [("Steaven", 78), ("Sara", 92)],
    "English": [("Matthew", 45)]
}
def addStudents(students,n):
    for i in range(n):
        name = input("Enter the name of the student: ")
        subject = input("enter the name of the subject: ")
        grade = input("Enter the grade for the class: ")
        if subject not in students:
            students[subject] = []
        students[subject].append((name,grade))


def viewStudents(students):
    for subject, info in students.items():
        print(subject,":",info)

options = "Hello"
while(options):
    options = input("Welcome, what do you want to do? ")
    if(options == "add user"):
        n = int(input("How many students do you want to add: "))
        addStudents(students,n)
    if(options=="view users"):
        viewStudents(students)
    if(options=="exit"):
        sys.exit(0)