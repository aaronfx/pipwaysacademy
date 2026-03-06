from ..extensions import db


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text)

    instructor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class CourseEnrollment(db.Model):

    __tablename__ = "course_enrollments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
