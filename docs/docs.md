# Project Structure

- accounts: deals with authentication
- backend/core: deals with teacher endpoints
- backend/student_core: deals with student endpoints

# Endpoints

User Authentication

- `auth/token/student_signup/` - Register a student
- `auth/token/teacher_signup/` - Register a teacher
- `auth/token/refresh/` - Refresh a token
- `auth/token/verify/` - Verify a token

Teacher Endpoints

- `core/classrooms` - Create a classroom

Student Endpoints

- `auth/token/student_joinclass/` - Join a class

OUTDATED

- `auth/token/student_register/` - Used to join class

# Tables

- `User` - username, email, first name, last name, user type
- `Classroom` - teacher, name, code, student indexes (no. of students) eg. [1, 2, 3]
- `Enroll` - student id, classroom id, student index, score
- `Student profile` - student, class code, index, name, score

To keep track of leaderboard

- `Announcement` - classrooom, name, description

Announcement for each class

- `SubmissionStatuses` - task, student, status
- `Task` - classroom, name, description, status, display, max stars

Status for each task in a class

# To update changes

- `docker compose up`
- `docker ps` - to get the container id
- `docker exec -it <container id> sh`
- `python manage.py makemigrations`
- `python manage.py migrate`
  (to close interactive shell) - `ctrl + d`

# To create superuser

- `python manage.py createsuperuser`
