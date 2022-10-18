
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Parent, Student, Tutor, Location, Session
import datetime
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/show_all_parents", methods=["GET"])
@login_required
def show_all_parents():
    search_parent = request.args.get("search_parent")
    if search_parent:
        parents = Parent.query.filter(Parent.first_name.contains(search_parent) | Parent.last_name.contains(search_parent))
    else:
        parents = Parent.query.filter_by(archived="no")
    return render_template("show_all_parents.html", parents=parents, user=current_user)

@views.route("/show_all_parents_with_archive", methods=["GET"])
@login_required
def show_all_parents_with_archive():
    search_parent = request.args.get("search_parent")
    if search_parent:
        parents = Parent.query.filter(Parent.first_name.contains(search_parent) | Parent.last_name.contains(search_parent))
    else:
        parents = Parent.query.all()
    return render_template("show_all_parents_with_archive.html", parents=parents, user=current_user)

@views.route("/show_all_students", methods=["GET"])
@login_required
def show_all_students():
    search_student = request.args.get("search_student")
    if search_student:
        students = Student.query.filter(Student.first_name.contains(search_student) | Student.last_name.contains(search_student) | Student.parent_id.contains(search_student))
    else:
        students = Student.query.all()
    return render_template("show_all_students.html", students=students, user=current_user)

@views.route("/show_all_tutors", methods=["GET"])
@login_required
def show_all_tutors():
    search_tutor = request.args.get("search_tutor")
    if search_tutor:
        tutors = Tutor.query.filter(Tutor.first_name.contains(search_tutor) | Tutor.last_name.contains(search_tutor))
    else:
        tutors = Tutor.query.all()
    return render_template("show_all_tutors.html", tutors=tutors, user=current_user)

@views.route("/add_student", methods=["GET", "POST"])
@login_required
def add_student():
    search_parent = request.args.get("search_parent")
    if search_parent:
        parents = Parent.query.filter(Parent.first_name.contains(search_parent) | Parent.last_name.contains(search_parent))
    else:
        parents = Parent.query.all()
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        main_email = request.form.get("main_email")
        phone_number = request.form.get("phone_number")
        note = request.form.get("note")
        parent_id = request.form.get("parent_id")
        archived = "no"

        email_check = Student.query.filter_by(main_email=main_email).first()
        if email_check:
            flash("Email address already exists!", category="error")
        else:
            new_student = Student(first_name=first_name, last_name=last_name, main_email=main_email, phone_number=phone_number, note=note, parent_id=parent_id, archived=archived)
            db.session.add(new_student)
            db.session.commit()
            flash("Student added successfully!", category="success")
    return render_template("add_student.html", parents=parents, user=current_user)

@views.route("/add_parent", methods=["GET", "POST"])
@login_required
def add_parent():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        main_email = request.form.get("main_email")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")
        billing_email = request.form.get("billing_email")
        billing_address = request.form.get("billing_address")
        billing_city = request.form.get("billing_city")
        billing_state = request.form.get("billing_state")
        billing_zipcode = request.form.get("billing_zipcode")
        phone_number = request.form.get("phone_number")
        note = request.form.get("note")
        archived = "no"

        email_check = Parent.query.filter_by(main_email=main_email).first()
        if email_check:
            flash("Email address already exists!", category="error")
        elif main_email == "":
            flash("Please enter an email address.")
        else:
            new_parent = Parent(first_name=first_name, last_name=last_name, main_email=main_email, address=address, city=city, state=state, zipcode=zipcode, billing_email=billing_email, billing_address=billing_address, billing_city=billing_city, billing_state=billing_state, billing_zipcode=billing_zipcode, phone_number=phone_number, note=note, balance=0, archived=archived)
            db.session.add(new_parent)
            db.session.commit()
            flash("Parent added successfully!", category="success")
    return render_template("add_parent.html", user=current_user)

@views.route("/add_tutor", methods=["GET", "POST"])
@login_required
def add_tutor():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        main_email = request.form.get("main_email")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")
        phone_number = request.form.get("phone_number")
        note = request.form.get("note")
        is_admin = request.form.get("is_admin")
        archived = "no"
     
        email_check = Tutor.query.filter_by(main_email=main_email).first()
        if email_check:
            flash("Email address already exists!", category="error")
        else:
            new_tutor = Tutor(first_name=first_name, last_name=last_name, main_email=main_email, address=address, city=city, state=state, zipcode=zipcode, phone_number=phone_number, note=note, is_admin=is_admin, archived=archived)
            db.session.add(new_tutor)
            db.session.commit()
            flash("Tutor added successfully!", category="success")
    return render_template("add_tutor.html", user=current_user)

@views.route("/tutor_calendar")
@login_required
def tutor_calendar():
    sessions = []
    all_sessions = Session.query.all()
    for session in all_sessions:
        session_student = Student.query.filter_by(id=session.student_id).first()
        sessions.append({
            "title": f"{session_student.first_name} {session_student.last_name} ({session.duration})",
            "start": f"{session.date.strftime('%Y-%m-%d')}",
            "end": "",
            "url": f"",
        })
   
    return render_template("tutor_calendar.html", sessions=sessions, user=current_user)

@views.route("/add_tutoring_session", methods=["GET", "POST"])
@login_required
def add_tutoring_session():
    search_student = request.args.get("search_student")
    if search_student:
        students = Student.query.filter(Student.first_name.contains(search_student) | Parent.last_name.contains(search_student) | Parent.first_name.contains(search_student) | Student.first_name.contains(search_student))
    else:
        students = Student.query.all()
    tutors = Tutor.query.all()
    locations = Location.query.all()
    if request.method == "POST":
        student_id = request.form.get("student_id")
        date_unconverted = request.form.get("date")
        date = datetime.datetime.strptime(date_unconverted, '%Y-%m-%d')
        duration = request.form.get("duration")
        start_time_hour = request.form.get("start_time_hour")
        start_time_minute = request.form.get("start_time_minute")
        start_time_ampm = request.form.get("start_time_ampm")
        start_time = f"{start_time_hour}:{start_time_minute} {start_time_ampm}"
        end_time_hour = request.form.get("end_time_hour")
        end_time_minute = request.form.get("end_time_minute")
        end_time_ampm = request.form.get("end_time_ampm")
        end_time = f"{end_time_hour}:{end_time_minute} {end_time_ampm}"
        location_id = request.form.get("location_id")
        tutor_id = request.form.get("tutor_id")

        if Session.query.filter_by(id=student_id).first() and Session.query.filter_by(date=date).first():
            flash("Student has a session on this date.", category="error")
        else:
            new_session = Session(date=date, student_id=student_id, duration=duration, start_time=start_time, end_time=end_time, location_id=location_id, tutor_id=tutor_id)
            db.session.add(new_session)
            db.session.commit()
            flash("Session added successfully!", category="success")
    return render_template("add_tutoring_session.html", students=students, tutors=tutors, locations=locations, user=current_user)

@views.route("/add_location", methods=["GET", "POST"])
@login_required
def add_location():
    if request.method == "POST":
        name = request.form.get("name")
        hourly_rate = request.form.get("hourly_rate")
        pay_rate = request.form.get("pay_rate")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")
        note = request.form.get("note")
        archived = "no"

        if Location.query.filter_by(name=name).first():
            flash("Location already exists", category="error")
        else:
            new_location = Location(name=name, hourly_rate=hourly_rate, pay_rate=pay_rate, address=address, city=city, state=state, zipcode=zipcode, note=note, archived=archived)
            db.session.add(new_location)
            db.session.commit()
            flash("Location added successfully!", category="success")
    return render_template("add_location.html", user=current_user)

@views.route("/locations")
@login_required
def locations():
    locations = Location.query.all()
    return render_template("locations.html", locations = locations, user=current_user)

# Non-functional still in development
@views.route("/show_session")
@login_required
def show_session():
    return render_template("show_session.html", user=current_user)

# Non-functional still in development
@views.route("/generate_bill", methods=["GET", "POST"])
@login_required
def generate_bill():
    if request.method == "POST":
        month = request.form.get("month")
        year = request.form.get("year")
    return render_template("generate_bill.html", user=current_user)

@views.route("/all_sessions_for_parent", methods=["GET", "POST"])
@login_required
def all_sessions_for_parent():
    search_parent = request.args.get("search_parent")
    if search_parent:
        parents = Parent.query.filter(Parent.first_name.contains(search_parent) | Parent.last_name.contains(search_parent) | Parent.id.contains(search_parent))
    else:
        parents = Parent.query.all()
    all_sessions = []
    if request.method == "POST":
        parent_id = request.form.get("parent_id")
        students = Student.query.filter_by(parent_id=parent_id)
        for student in students:
            student_dict = {}
            student_dict["name"] = f"{student.first_name} {student.last_name}"
            student_dict["sessions"] = []
            student_sessions = Session.query.filter_by(student_id=student.id)
            student_dict["sessions"] = student_sessions
            count = 0
            total_session_hours = 0
            for session in student_sessions:
                count += 1
                total_session_hours += session.duration
            student_dict["total_session_hours"] = total_session_hours
            student_dict["session_count"] = count
            all_sessions.append(student_dict)
    return render_template("all_sessions_for_parent.html", parents=parents, all_sessions=all_sessions, user=current_user)

@views.route("/edit_parent/<int:id>", methods=["GET", "POST"])
@login_required
def edit_parent(id):
    parent = Parent.query.filter(Parent.id==id).first()
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        main_email = request.form.get("main_email")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")
        billing_email = request.form.get("billing_email")
        billing_address = request.form.get("billing_address")
        billing_city = request.form.get("billing_city")
        billing_state = request.form.get("billing_state")
        billing_zipcode = request.form.get("billing_zipcode")
        phone_number = request.form.get("phone_number")
        note = request.form.get("note")

        parent.first_name = first_name
        parent.last_name = last_name
        parent.main_email = main_email
        parent.address = address
        parent.city = city
        parent.state = state
        parent.zipcode = zipcode
        parent.billing_email = billing_email
        parent.billing_address = billing_address
        parent.billing_city = billing_city
        parent.billing_state = billing_state
        parent.billing_zipcode = billing_zipcode
        parent.phone_number = phone_number
        parent.note = note
        db.session.commit()
        flash("Parent Updated Successfully", category="success")
        return redirect(url_for("views.show_all_parents"))
    return render_template("edit_parent.html", user=current_user, parent=parent)

@views.route("/archive_parent/<int:id>", methods=["GET", "POST"])
@login_required
def archive_parent(id):
    parent = Parent.query.filter(Parent.id==id).first()
    if request.method == "POST":
        parent.archived = "yes"
        db.session.commit()
        flash("Parent Archived Successfully", category="success")
        return redirect(url_for("views.show_all_parents"))
    return render_template("archive_parent.html", user=current_user, parent=parent)

@views.route("/unarchive_parent/<int:id>", methods=["GET", "POST"])
@login_required
def unarchive_parent(id):
    parent = Parent.query.filter(Parent.id==id).first()
    if request.method == "POST":
        parent.archived = "no"
        db.session.commit()
        flash("Parent Un-Archived Successfully", category="success")
        return redirect(url_for("views.show_all_parents"))
    return render_template("unarchive_parent.html", user=current_user, parent=parent)