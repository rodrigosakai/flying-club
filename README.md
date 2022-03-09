# Flying Club

### Context
While revisiting my undergraduate assignments, this Flying Club project from the Software Engineering class (taken in early 2019) intrigued me. The task was to develop a web application to meet the business needs of a flying club. My group used SQLite for database, HTML, CSS, and Vanilla JavaScript on the front-end. However, I don't quite remember the technology we adopted on the backend. As no one from the group had any experience with web development then, completing the project was challenging.

Since then, I have worked for a few years as a Software Developer. So while revisiting this project, I set out to develop a Backend solution with the knowledge I gathered from my experience in the industry.

## Introduction
This project was built using Python/Flask and uses MongoDB as a database. This project is a Backend solution for the business needs of a Flying Club. The application registers three types of users:
- Pilots
- Instructors
- Students

A student is defined by a combination of `name`, `address`, and `date_of_birth`. Pilots have their `license_number` additionally. Instructors are pilots with additional certification. Thus, they must inform their `institution_name` and the `diploma_issue_date`.

In the flying club, `instructors` give flying lessons to `students` and grade them with numbers between 1 (lowest grade) to 4 (highest). After completing a `minimum flying hours`, with 85% of the hours graded highly (with either a 3 or 4), a student can issue a license and become a pilot.

## 
