from flask import Flask, request, jsonify
from datetime import datetime, timezone
from homework_model import Homework

app = Flask(__name__)

# options: simple list, pandas DF, or an actual DB table
homework_submissions = []

@app.route('/submit', methods=['POST'])
def submit_homework():
    data = request.json
    new_homework = Homework(
        id=len(homework_submissions) + 1,
        assignment_name=data['assignment_name'],
        student_name=data['student_name']
    )
    homework_submissions.append(new_homework)
    return jsonify({"message": "Homework submitted successfully"}), 201

@app.route('/student/submissions', methods=['GET'])
def view_student_submissions():
    student_name = request.args.get('student_name')
    if not student_name:
        return jsonify({"error": "Student name is required"}), 400
    
    grade_filter = request.args.get('grade')
    assignment_filter = request.args.get('assignment_name')
    
    filtered_submissions = [hw for hw in homework_submissions if hw.student_name == student_name]
    if grade_filter:
        filtered_submissions = [hw for hw in filtered_submissions if hw.final_grade == grade_filter]
    if assignment_filter:
        filtered_submissions = [hw for hw in filtered_submissions if hw.assignment_name == assignment_filter]
    
    return jsonify([hw.to_dict() for hw in filtered_submissions])

@app.route('/teacher/submissions', methods=['GET'])
def view_teacher_submissions():
    assignment_filter = request.args.get('assignment_name')
    student_filter = request.args.get('student_name')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    
    filtered_submissions = homework_submissions
    if assignment_filter:
        filtered_submissions = [hw for hw in filtered_submissions if hw.assignment_name == assignment_filter]
    if student_filter:
        filtered_submissions = [hw for hw in filtered_submissions if hw.student_name == student_filter]
    if from_date:
        filtered_submissions = [hw for hw in filtered_submissions if hw.submission_date >= from_date]
    if to_date:
        filtered_submissions = [hw for hw in filtered_submissions if hw.submission_date <= to_date]
    
    return jsonify([hw.to_dict() for hw in filtered_submissions])

@app.route('/grade/<int:homework_id>', methods=['POST'])
def grade_homework(homework_id):
    data = request.json
    for hw in homework_submissions:
        if hw.id == homework_id:
            hw.final_grade = data['final_grade']
            hw.teacher_notes = data.get('teacher_notes', '')
            hw.grading_date = datetime.utcnow().isoformat()
            return jsonify({"message": "Homework graded successfully"})
    return jsonify({"error": "Homework not found"}), 404