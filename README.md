# Flying Club

### Context
While revisiting my undergraduate assignments, this Flying Club project from the Software Engineering class (taken in early 2019) intrigued me. The task was to develop a web application to meet the business needs of a flying club. My group used SQLite for database, HTML, CSS, and Vanilla JavaScript on the front-end. However, I don't quite remember the technology we adopted on the backend. As no one from the group had any experience with web development then, completing the project was challenging.

Since then, I have worked for a few years as a Software Developer. So while revisiting this project, I set out to develop a Backend solution with the knowledge I gathered from my experience in the industry.

## Introduction
This project was built using Python/Flask and uses MongoDB as a database. This project is a Backend solution for the business needs of a Flying Club. The application registers three types of users:
- Pilots
- Instructors
- Students

A student is defined by a combination of `name`, `address`, and `date_of_birth`. Pilots have their `license_number` additionally. Instructors are pilots with certification. Thus, they must also inform their `institution_name` and the `diploma_issue_date`.

In the flying club, `instructors` give flying lessons to `students` and grade them with numbers between 1 (lowest grade) to 4 (highest). After completing a `minimum flying hours`, with 85% of the hours graded highly (with either a 3 or 4), a student can issue a license and become a pilot.

## First Steps
The project was built in Python 3.8 and uses `Pipenv` to manage dependenciens (run `pip install pipenv` on the command line to install it). After cloning the repository, run `pipenv shell` and `pipenv install -d` to create a virtual environment and insall the dependencies in it.

For the project to run locally, you will need a `.env` file and include the following environment variables:
```
PYTHONPATH=.
FLASK_APP=api.py
SECRET_KEY=any-random-key // Your secret key
MINIMUM_FLYING_HOURS=150 // 150 was the default value in our assignment, but it can vary
```

The `SECRET_KEY` is the key that will be used to generate `JWT` to establish authentication between client and server. `MINIMUM_FLYING_HOURS` is the the minimum hours of flight that a `student` has to complete to become a `pilot`.

To run the application in a production environment, the `.env` file would also need to include:
```
ENV=production
HOST=mongo-host // Your mongo host
USER=mongo-user // Your mongo user
PASSWORD=mongo-password // Your mongo password
DATABASE=mongo-database // YOur mongo database
```
