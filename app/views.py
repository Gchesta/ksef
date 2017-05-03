from datetime import date
from flask import render_template, url_for, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from app import app
from . import forms #LoginForm, SignupForm
from .models import Educator, Project, Category, SubCounty, School, engine
import werkzeug.security as ws
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

login_manager = LoginManager()
login_manager.init_app(app)

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

@login_manager.user_loader
def load_user(id):
    return dbsession.query(Educator).filter_by(id=id).first()

@app.route("/", methods=["GET", "POST"])
def home():
    sign_up_form = forms.SignupForm()
    login_form = forms.LoginForm()
    sub_county_schools = dbsession.query(School).all()
    schools_and_subcounties = [(school.sub_county_name + " - " + school.school_name) for school in sub_county_schools]
    schools_and_subcounties.sort()
    schools_and_subcounties = [""] + schools_and_subcounties
    sign_up_form.school.choices = [(school, school) for school in schools_and_subcounties]
    if sign_up_form.register_submit.data and sign_up_form.validate_on_submit():
        form = sign_up_form
        email = form.email.data
        user = dbsession.query(Educator).filter_by(email=email).first()
        if user:
            flash("User Already Exists")
            return render_template("home.html",login_form=login_form, sign_up_form=sign_up_form)
        school_on_form = form.school.data.strip()
        for sub_county_school in sub_county_schools:
            if school_on_form.startswith(sub_county_school.sub_county_name.strip()):
                school_on_form = school_on_form[(len(sub_county_school.sub_county_name.strip()) + 3):]
                new_educator = Educator(
                    sub_county_name=sub_county_school.sub_county_name.strip(),
                    register_as=form.register_as.data,
                    fullname=form.fullname.data,
                    email=form.email.data,
                    password_hash=ws.generate_password_hash(form.password.data),
                    county=form.county.data,
                    #sub_county=form.sub_county.data,
                    school=school_on_form,
                    date_signedup=date.today()
                )

                dbsession.add(new_educator)
                dbsession.commit()
                login_user(new_educator)
                return render_template("dashboard.html")


    elif login_form.login_submit.data and login_form.validate_on_submit():
        form = login_form
        user = dbsession.query(Educator).filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("User does not exist")
        return render_template("home.html",login_form=login_form, sign_up_form=sign_up_form)
    return render_template(
        "home.html",
        sign_up_form=sign_up_form,
        login_form=login_form,
        )

@app.route("/myprojects.html", methods=["GET", "POST"])
@login_required
def myprojects():
    form = forms.ProjectForm()
    name = current_user.fullname
    categories = [""] + [category.category_name for category in dbsession.query(Category).all()]
    form.category.choices = [(category, category) for category in categories]
    school_members = dbsession.query(Educator).filter_by(school=current_user.school).all()
    all_presenters = [person for person in school_members if person.register_as == "Student"]
    presenters = [""] + [user.fullname for user in all_presenters]
    presenters.remove(current_user.fullname)
    form.second_presenter.choices = [(presenter, presenter) for presenter in presenters]
    projects1 = dbsession.query(Project).filter_by(first_presenter=name).all()
    projects2 = dbsession.query(Project).filter_by(second_presenter=name).all()
    myprojects = projects1 + projects2
    if form.validate_on_submit():
        new_project = Project(
            school=current_user.school,
            category=form.category.data,
            title=form.title.data,
            first_presenter=current_user.fullname,
            second_presenter=form.second_presenter.data,
            date_registered=date.today(),
            average_score = 0,
            date_presented = "N/A"
        )
        dbsession.add(new_project)
        dbsession.commit()
        return redirect(url_for("myprojects"))
    return render_template("myprojects.html", form=form, myprojects=myprojects)

@app.route("/dashboard.html")
#@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout.html")
#@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/registered-students.html")
@login_required
def registered_students():
    school = current_user.school
    school_members = dbsession.query(Educator).filter_by(school=school).all()
    mystudents = [user for user in school_members if user.register_as == "Student"]

    return render_template("registered-students.html", mystudents=mystudents)

@app.route("/registered-students/approve/<int:id>")
@login_required
def approve_student(id):
    user = dbsession.query(Educator).filter_by(id=id).first()
    user.is_approved = True
    dbsession.commit()
    return redirect(url_for("registered_students"))

@app.route("/registered-students/unapprove/<int:id>")
@login_required
def unapprove_student(id):
    user = dbsession.query(Educator).filter_by(id=id).first()
    user.is_approved = False
    dbsession.commit()
    return redirect(url_for("registered_students"))

@app.route("/registered-students/delete/<int:id>")
@login_required
def delete_student(id):
    user = dbsession.query(Educator).filter_by(id=id).first()
    dbsession.delete(user)
    dbsession.commit()
    return redirect(url_for("registered_students"))

@app.route("/school-projects.html")
@login_required
def school_projects():
    school = current_user.school
    school_projects = dbsession.query(Project).filter_by(school=school).all()
    return render_template("school-projects.html", school_projects=school_projects)

@app.route("/school-projects/approve/<int:project_id>")
@login_required
def approve_project(project_id):
    project = dbsession.query(Project).filter_by(project_id=project_id).first()
    project.is_approved = True
    dbsession.commit()
    return redirect(url_for("school_projects"))

@app.route("/school-projects/delete/<int:project_id>")
@login_required
def delete_project(id):
    project = dbsession.query(Project).filter_by(project_id=project_id).first()
    dbsession.delete(project)
    dbsession.commit()
    return redirect(url_for("school_projects"))

@app.route("/adjudicate-projects.html")
@login_required
def adjudicate_projects():
    form1 = forms.AdjudicateSelectForm()
    categories = [""] + [category.category_name for category in dbsession.query(Category).all()]
    form1.category.choices = [(category, category) for category in categories]
    return render_template("adjudicate-projects.html", form1=form1)









@app.route("/sub-counties.html",  methods=["GET", "POST"])
#@login_required
def sub_counties():
    form = forms.SubCountyForm()
    sub_counties = [sub_county.sub_county_name for sub_county in dbsession.query(SubCounty).all()]
    sub_counties.sort()
    sub_counties = [""] + sub_counties
    if form.validate_on_submit():
        new_sub_county = SubCounty(
            sub_county_name=form.sub_county_name.data
        )
        dbsession.add(new_sub_county)
        dbsession.commit()
        return redirect(url_for("sub_counties"))
    return render_template("sub-counties.html", form=form,
    sub_counties=sub_counties)

@app.route("/categories.html",  methods=["GET", "POST"])
#@login_required
def categories():
    form = forms.CategoryForm()
    categories = [category for category in dbsession.query(Category).all()]
    if form.validate_on_submit():
        new_category = Category(
            category_name=form.category_name.data
        )
        dbsession.add(new_category)
        dbsession.commit()
        return redirect(url_for("categories"))
    return render_template("categories.html", form=form,
    categories=categories)


@app.route("/categories/delete/<int:category_id>")
@login_required
def delete_category(category_id):
    category = dbsession.query(Category).filter_by(category_id=category_id).first()
    dbsession.delete(category)
    dbsession.commit()
    return redirect(url_for("categories"))



"""@app.route("/zones")
#login_required
def zones():
    zones = dbsession.query(Zone).all()
    return render_template("zones.html", zones=zones)"""

@app.route("/schools.html",  methods=["GET", "POST"])
#@login_required
def schools():
    form = forms.SchoolForm()
    schools = dbsession.query(School).all()
    sub_counties = [sub_county.sub_county_name for sub_county in dbsession.query(SubCounty).all()]
    sub_counties.sort()
    sub_counties = [""] + sub_counties
    form.sub_county_name.choices = [(sub_county, sub_county) for sub_county in sub_counties]
    if form.validate_on_submit():
        new_school = School(
            sub_county_name=form.sub_county_name.data,
            school_name=form.school_name.data
        )
        dbsession.add(new_school)
        dbsession.commit()
        return redirect(url_for("schools"))
    return render_template("schools.html", schools=schools, form=form)
