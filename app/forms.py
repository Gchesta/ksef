from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, Required
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Keep me logged in")
    login_submit = SubmitField("Log In")

class SignupForm(FlaskForm):
    register_as = SelectField(u"Role", choices = [("", ""), ("Student", "Student"), ("Educator","Educator")])
    email = StringField("Email", validators=[DataRequired()])
    fullname = StringField("Fullname", validators=[DataRequired()])
    county = SelectField(u"County", choices = [("", ""), ("Nairobi", "Nairobi")])
    school = SelectField("School", choices = [("", "")])
    password = PasswordField("Password", validators=[ DataRequired(), EqualTo("password2", message = "Passwords must match")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    register_submit = SubmitField("Register")

class ProjectForm(FlaskForm):
    title = StringField("Project Title", validators=[DataRequired()])
    category = SelectField(u"Project Category", choices = [("", "")], validators=[DataRequired()])
    #first_presenter = StringField("First Presenter", validators=[DataRequired()])
    second_presenter = SelectField(u"Second Presenter", choices = [("", "")])
    #school = StringField("School", validators=[DataRequired()])

class SubCountyForm(FlaskForm):
    sub_county_name = StringField("SubCounty Name", validators=[DataRequired()])
    add_sub_county = SubmitField("Add Sub-County")


class SchoolForm(FlaskForm):
    sub_county_name = SelectField(u"Sub-County", choices = [("", ""), ("Dagoreti North", "Dagoreti North"),
    ("Dagoreti South", "Dagoreti South"), ("Embakasi Central", "Embakasi Central"), ("Embakasi East", "Embakasi East"),
    ("Embakasi North", "Embakasi North"), ("Embakasi South", "Embakasi South"), ("Embakasi West", "Embakasi West"),
    ("Kamukunji", "Kamukunji"), ("Kasarani", "Kasarani"), ("Kibera", "Kibera"), ("Lang'ata", "Lang'ata"),
    ("Makadara", "Makadara"), ("Mathare", "Mathare"), ("Roysambu", "Roysambu"), ("Ruaraka", "Ruaraka"),
    ("Starehe", "Starehe"), ("Westlands", "Westlands"), ("Kangemi", "Kangemi")])
    school_name = StringField("School Name", validators=[DataRequired()])
    add_school = SubmitField("Add School")

class CategoryForm(FlaskForm):
    category_name = StringField("Category Name", validators=[DataRequired()])
    add_category = SubmitField("Add New Category")

class AdjudicateSelectForm(FlaskForm):
    category = SelectField(u"Category", choices = [("", ""), ("Chemistry", "Chemistry")])
    show_projects = SubmitField("Show Projects")

class AdjudicationForm(FlaskForm):
    category = SelectField(u"Category", choices = [("", ""), ("Chemistry", "Chemistry")])
    show_projects = SubmitField("Show Projects")
