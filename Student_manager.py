# The Goal: Store 3 Students, show who passes and find the top scorer

# Task: Create a Python program that:

# Defines a Student class with a name and score.
# - Stores 3 students in a list.
# - Uses a loop to iterate through students.
# - Displays students with scores above 50.
# - Uses a top_scorer() function to find the highest scorer.

# How to submit
# Submission Instructions:
# - Submit your code on the assignment portal with screenshots of your code and output
# - Write and understand your own code
# - Students may be randomly selected to present and explain their code during class.
# - Late submissions may not be accepted.

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    
# Create a list of students
students = [
    Student("Bilal", 35),
    Student("Sami", 84),
    Student("Saad", 93)
]

# Display students with scores above 50
for student in students:
    if student.score > 50:
        print(f"{student.name}: {student.score}")

# Find the top scorer
def top_scorer(students_list):
    return max(students_list, key=lambda s: s.score)

top_student = top_scorer(students)
print(f"Top scorer: {top_student.name} with a score of {top_student.score}")


