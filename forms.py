from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, URLField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, InputRequired, URL


class LoginForm(FlaskForm):
    email = EmailField(
        validators=[DataRequired()],
        render_kw={"class": "field", "placeholder": "", "autocomplete": "email"}
    )
    password = PasswordField(
        validators=[DataRequired()],
        render_kw={"class": "field", "placeholder": ""}
    )
    button = SubmitField(label="Login", render_kw={"class": "text button login-button"})


class SignupForm(FlaskForm):
    first_name = StringField(
        label="First Name",
        validators=[DataRequired(), Length(max=1000)],
        render_kw={"class": "field signup-field", "placeholder": "Your First Name"}
    )
    last_name = StringField(
        label="Last Name",
        validators=[DataRequired(), Length(max=1000)],
        render_kw={"class": "field signup-field", "placeholder": "Your Last Name"}
    )
    email = EmailField(
        label="Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "field signup-field", "placeholder": "e.g. name@email.com"}
    )
    password = PasswordField(
        label="Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={"class": "field signup-field", "placeholder": "8 characters or more"}
    )
    privacy = BooleanField(
        validators=[InputRequired(message="You have not agreed to the Privacy Policy.")],
        render_kw={"class": "checkbox"}
    )
    button = SubmitField(label="Sign Up", render_kw={"class": "text button signup-button signup-field"})


class TestimonyForm(FlaskForm):
    website = URLField(
        label="URL of website built",
        validators=[DataRequired(), URL()],
        render_kw={"class": "field add-field website-url", "placeholder": "e.g. https://website.com"}
    )
    testimony = TextAreaField(
        label="Testimony",
        validators=[DataRequired()],
        render_kw={"class": "field add-field", "placeholder": "Your Testimony"}
    )
    button = SubmitField(label="Submit", render_kw={"class": "text button add-button"})


class PictureForm(FlaskForm):
    picture = FileField(render_kw={"class": "text"})
    button = SubmitField(label="Upload", render_kw={"class": "button upload-button"})
