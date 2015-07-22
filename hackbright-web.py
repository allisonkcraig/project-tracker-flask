from flask import Flask, request, render_template

import ab_hackbright

app = Flask(__name__)

@app.route('/student-search')
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = ab_hackbright.get_student_by_github(github)
    return render_template("student_info.html", first=first, last=last, github=github)
    

@app.route("/student-add-confirm", methods=['POST'])
def student_add():
    """Confirm that you added new student"""

    fname_input = request.form.get('first_name_h')
    lname_input = request.form.get('last_name_h')
    github_input = request.form.get('github_h')


    # student_info = make_new_student(fname_input, lname_input, github_input)
    student_tuple = ab_hackbright.make_new_student(fname_input, lname_input, github_input)
    first = student_tuple[0]
    last = student_tuple[1] 
    github = student_tuple[2]

    return render_template("student-add-confirm.html", firstname_j=first, lastname_j=last, github_j=github)


@app.route("/new-student-add")
def new_student():
    """Form to add student to database."""
    return render_template('new-student-add.html')
    

@app.route("/project")
def get_project():
    """Show information of project, query by title."""
    
    pass

@app.route("/git-grade")
def git_grade():
    """Show grade information on given project from student's github username."""

    pass

@app.route("/add-grade")
def add_grade():
    """Add grade for project linked to student git-hub."""

    pass


if __name__ == "__main__":
    app.run(debug=True)