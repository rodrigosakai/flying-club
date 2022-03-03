"""
SQL Alchemy models
"""

# from sqlalchemy import VARCHAR, Column, Integer, Date
# from sqlalchemy.orm import declarative_base


# Base = declarative_base()


# class Associate:
#     """
#     Abstract class from which Student, Pilot and Instructor derive
#     """

#     def __init__(self, name: str, address: str, date_of_birth: str):
#         self.name = name
#         self.address = address
#         self.date_of_birth = date_of_birth


# class Student(Base, Associate):
#     """
#     Students take flying classes from instructors.
#     After completing a certain amount of hours, they obtain their licences and become Pilots
#     """
#     __tablename__ = "associates.students"
#     id = Column(Integer, primary_key=True)
#     name = Column(VARCHAR(100))
#     address = Column(VARCHAR(150))
#     date_of_birth = Column(Date)

#     def __init__(self, name: str, address: str, date_of_birth: str):
#         Associate.__init__(name, address, date_of_birth)


# class Instructor(Base, Associate):
#     """
#     Instructors give flying lessons to students
#     """
#     __tablename__ = "associates.instructors"

#     id = Column(Integer, primary_key=True)
