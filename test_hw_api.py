import unittest
from app import app

class HomeworkAPITest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homework_submission(self):
        response = self.app.post('/submit', json={
            "assignment_name": "Math Homework",
            "student_name": "John Doe"
        })
        self.assertEqual(response.status_code, 201)
    
    def test_view_student_submission(self):
        response = self.app.post('/submit', json={
            "assignment_name": "Math Homework",
            "student_name": "Darth Vader"
        })

        response = self.app.get("/student/submissions?student_name=Darth Vader")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_view_student_submission_bad_request(self):
        response = self.app.get("/student/submissions")
        self.assertEqual(response.status_code, 400)

    def test_homework_submit_then_grade(self):
        self.app.post('/submit', json={
            "assignment_name": "English Homework",
            "student_name": "Alice"
        })
        response = self.app.post('/grade/1', json={
            "final_grade": "A",
            "teacher_notes": "Well done"
        })
        self.assertEqual(response.status_code, 200)

    def test_grade_nonexistent_homework(self):
        response = self.app.post('/grade/99', json={
            "final_grade": "B",
            "teacher_notes": "Good work"
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
