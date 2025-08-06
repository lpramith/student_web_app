from flask import Flask, render_template, request, redirect, url_for
import student_db
import csv
import io
from flask import make_response

from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
student_db.connect()  # ensure table exists

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    students = student_db.view()
    return render_template('view.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        grade = request.form['grade']
        student_db.insert(name, email, course, grade)
        return redirect(url_for('view'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    student_db.delete(id)
    return redirect(url_for('view'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        grade = request.form['grade']
        student_db.update(id, name, email, course, grade)
        return redirect(url_for('view'))
    else:
        student = [s for s in student_db.view() if s[0] == id][0]
        return render_template('edit.html', student=student)
@app.route('/export/csv')
def export_csv():
    students = student_db.view()

    # CSV generation
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Email', 'Course', 'Grade'])  # header
    cw.writerows(students)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=students.csv"
    output.headers["Content-type"] = "text/csv"
    return output
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@app.route('/export/pdf')
def export_pdf():
    students = student_db.view()

    # Create a PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 40, "Student Records")

    p.setFont("Helvetica", 10)
    y = height - 80
    p.drawString(40, y, "ID")
    p.drawString(80, y, "Name")
    p.drawString(200, y, "Email")
    p.drawString(340, y, "Course")
    p.drawString(440, y, "Grade")

    y -= 20
    for s in students:
        if y < 50:  # page break
            p.showPage()
            y = height - 50
        p.drawString(40, y, str(s[0]))
        p.drawString(80, y, s[1])
        p.drawString(200, y, s[2])
        p.drawString(340, y, s[3])
        p.drawString(440, y, s[4])
        y -= 20

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="students.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
