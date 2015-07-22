"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])
    return (row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    INSERT = """
        INSERT INTO Students (first_name, last_name, github)
        VALUES (?, ? , ?)
        """
    db_cursor.execute(INSERT, (first_name, last_name, github))
    db_connection.commit()
    
    print "Successfully added student: %s %s" % (first_name, last_name)
    return (first_name, last_name, github)



def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """ 
        SELECT * FROM projects
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    # projid, title, descrip, max_grade = row
    print "ID: %s Title: %s Description: %s Max Grade: %s" % (row[0], row[1], row[2], str(row[3]))
    return (row[0], row[1], row[2], str(row[3]))



def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    
    QUERY = """
        SELECT s.first_name, g.project_title, g.grade 
        FROM Students AS s
        JOIN Grades AS g
        On (s.github = g.student_github) 
        WHERE g.project_title = ? AND s.github =?
        """
    db_cursor.execute(QUERY, (title, github))
    row = db_cursor.fetchone()
    print "%s got grade %s on %s" % (row[0], str(row[2]), row[1])    
    return (row[0], str(row[2]), row[1])



def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    INSERT = """
        INSERT INTO Grades (student_github, project_title, grade)
        VALUES (?, ? , ?)
        """
    db_cursor.execute(INSERT, (github, title, grade))
    db_connection.commit()
    print "Gave %s grade %s on %s" % (github, grade, title)  
    return (github, grade, title)

    
    
def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]   
            get_project_by_title(title)

        elif command == "git_grade":
            github, project_title = args
            get_grade_by_github_title(github, project_title)

        elif command == "add_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
