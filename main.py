from flask import Flask, render_template, redirect, url_for, request, flash
from forms import LoginForm, SignupForm
import os
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, create_engine
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FLASK-SECRET-KEY")
csrf = CSRFProtect(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE-URI")
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String(), unique=True)
    password: Mapped[str] = mapped_column(String())


with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/flow")
def flow():
    return "This is Flow's access page."


@app.route("/designs")
def designs():
    return render_template("designs.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            data = request.form
            user = db.session.execute(db.select(User).where(User.email == data["email"])).scalar()
            if user:
                if check_password_hash(user.password, data["password"]):
                    login_user(user)
                    return redirect(url_for("account"))
                flash("Invalid Password, Please Try Again.")
                return redirect(url_for("login"))
            flash("Account Not Found.")
            return redirect(url_for("login"))
    return render_template("login.html", form=login_form)


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    signup_form = SignupForm()
    if request.method == "POST":
        if signup_form.validate_on_submit():
            print(request.form)
            data = request.form
            hashed_password = generate_password_hash(
                password=data["password"],
                method="pbkdf2",
                salt_length=8
            )
            user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            user = db.session.execute(db.select(User).where(User.email == data["email"])).scalar()
            login_user(user)
            return redirect(url_for("account"))
    return render_template("sign-up.html", form=signup_form)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")


@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)
