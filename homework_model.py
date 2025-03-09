import datetime
from datetime import datetime, timezone

class Homework:
    def __init__(self, id, assignment_name, student_name):
        self.id = id
        self.assignment_name = assignment_name
        self.student_name = student_name
        self.submission_date = datetime.now(timezone.utc).isoformat()
        self.grading_date = None
        self.final_grade = None
        self.teacher_notes = ""

    def to_dict(self):
        return {
            "id": self.id,
            "assignment_name": self.assignment_name,
            "student_name": self.student_name,
            "submission_date": self.submission_date,
            "grading_date": self.grading_date,
            "final_grade": self.final_grade,
            "teacher_notes": self.teacher_notes
        }