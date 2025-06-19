from flask import Flask, render_template, redirect, url_for, request, flash
from forms import LoginForm, SignupForm, CommentForm, PictureForm, SettingsForm, VerifyForm, PasswordForm
import os
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, text
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FLASK-SECRET-KEY")
csrf = CSRFProtect(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE-URI")
db.init_app(app)

app.config["UPLOAD_FOLDER"] = "static/images/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "jfif"}
app.config["MAX_CONTENT_LENGTH"] = 8 * 1000 * 1000

url = os.environ.get("API-URL")
i_d_ = os.environ.get("ID-INSTANCE")
key = os.environ.get("API-TOKEN-INSTANCE")
number = os.environ.get("NUMBER")

load_dotenv()

config = cloudinary.config(secure=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    first_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String(), unique=True)
    password: Mapped[str] = mapped_column(String())
    picture_number: Mapped[int] = mapped_column(Integer(), default=0, server_default=text("0"))
    picture_url: Mapped[str] = mapped_column(String(), nullable=True)
    comments = relationship("Comment", back_populates="user")


class Comment(UserMixin, db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] = mapped_column(DateTime())
    comment: Mapped[str] = mapped_column(String())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")


with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route("/")
def home():
    return render_template("index.html")


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


@app.route("/comments")
def comments():
    posts = db.session.execute(db.select(Comment).order_by(Comment.id.desc())).scalars().all()
    return render_template("comments.html", comments=posts)


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
            data = request.form
            db_emails = db.session.query(User.email).all()
            for email in db_emails:
                if data["email"] == email[0]:
                    flash("This Account Already Exists Here.")
                    return redirect(url_for("sign_up"))
            hashed_password = generate_password_hash(
                password=data["password"],
                method="pbkdf2",
                salt_length=8
            )
            user = User(
                first_name=data["first_name"].title(),
                last_name=data["last_name"].title(),
                email=data["email"],
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            user = db.session.execute(db.select(User).where(User.email == data["email"])).scalar()
            login_user(user)
            requests.post(
                f"{url}/waInstance{i_d_}/sendMessage/{key}",
                json={
                    "chatId": f"{number}@c.us",
                    "message": f"{data['first_name']} {data["last_name"]} Signed Up!"
                },
                headers={'Content-Type': 'application/json'}
            )
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


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = db.session.execute(db.select(User).where(User.id == current_user.id)).scalar()
    settings_form = SettingsForm(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )
    if request.method == "POST":
        if settings_form.validate_on_submit():
            data = request.form
            with app.app_context():
                user = db.session.execute(db.select(User).where(User.id == current_user.id)).scalar()
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.email = data["email"]
                db.session.commit()
            return redirect(url_for("account"))
    return render_template("settings.html", form=settings_form)


@app.route("/add-comment", methods=["GET", "POST"])
@login_required
def add_comment():
    comment_form = CommentForm()
    if request.method == "POST":
        if comment_form.validate_on_submit():
            data = request.form
            with app.app_context():
                comment = Comment(
                    datetime=datetime.now(timezone.utc),
                    comment=data["comment"],
                    user_id = current_user.id
                )
                db.session.add(comment)
                db.session.commit()
                requests.post(
                    f"{url}/waInstance{i_d_}/sendMessage/{key}",
                    json={
                        "chatId": f"{number}@c.us",
                        "message": f"{current_user.first_name} {current_user.last_name} added a comment: "
                                   f"{data['comment']}"
                    },
                    headers={'Content-Type': 'application/json'}
                )
            return redirect(url_for("account"))
    return render_template("add-comment.html", form=comment_form)


@app.route("/edit-comment/<int:i_d>", methods=["GET", "POST"])
@login_required
def edit_comment(i_d):
    comment = db.session.execute(db.select(Comment).where(Comment.id == i_d)).scalar()
    comment_form = CommentForm(comment=comment.comment)
    if request.method == "POST":
        if comment_form.validate_on_submit():
            data = request.form
            with app.app_context():
                comment = db.session.execute(db.select(Comment).where(Comment.id == i_d)).scalar()
                comment.comment = data["comment"]
                db.session.commit()
                requests.post(
                    f"{url}/waInstance{i_d_}/sendMessage/{key}",
                    json={
                        "chatId": f"{number}@c.us",
                        "message": f"{current_user.first_name} {current_user.last_name} edited a comment: "
                                   f"{data['comment']}"
                    },
                    headers={'Content-Type': 'application/json'}
                )
            return redirect(url_for("account"))
    return render_template("edit-comment.html", i_d=i_d, form=comment_form)


@app.route("/confirm-delete/<int:i_d>")
@login_required
def confirm_delete(i_d):
    pending_comment = db.session.execute(db.select(Comment).where(Comment.id == i_d)).scalar()
    return render_template("confirm-delete.html", comment=pending_comment)


@app.route("/delete/<int:i_d>")
@login_required
def delete(i_d):
    comment = db.session.execute(db.select(Comment).where(Comment.id == i_d)).scalar()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("account"))


@app.route("/profile-picture")
@login_required
def profile_picture():
    return render_template("profile-picture.html")


def valid_picture(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload-picture", methods=["GET", "POST"])
@login_required
def upload_picture():
    picture_form = PictureForm()
    if request.method == "POST":
        if "picture" not in request.files:
            flash("No file part")
            return redirect(url_for("upload_picture"))
        profile_pic = request.files["picture"]
        pic_name = profile_pic.filename
        if pic_name == "":
            flash("No file selected")
            return redirect(url_for("upload_picture"))
        if profile_pic and valid_picture(pic_name):
            if current_user.picture_url:
                cloudinary.uploader.destroy(f"{current_user.id}-{current_user.picture_number}")
            lad = db.get_or_404(User, current_user.id)
            picture_no = lad.picture_number
            cloudinary.uploader.upload(profile_pic, public_id=f"{current_user.id}-{picture_no}", unique_filename=False, overwrite=True)
            pic_url = CloudinaryImage(f"{current_user.id}-{picture_no}").build_url()
            user = db.get_or_404(User, current_user.id)
            user.picture_url = pic_url.rsplit("/", 1)[0] + "/q_auto/f_auto/c_scale,w_500/" + pic_url.rsplit("/", 1)[1]
            user.picture_number = picture_no + 1
            db.session.commit()
            requests.post(
                f"{url}/waInstance{i_d_}/sendFileByUrl/{key}",
                json={
                    "chatId": f"{number}@c.us",
                    "urlFile": f"{current_user.picture_url}",
                    "fileName": f"{current_user.first_name}-{current_user.last_name}.png",
                    "caption": f"{current_user.first_name} {current_user.last_name} uploaded a picture."
                },
                headers={'Content-Type': 'application/json'}
            )
        else:
            flash("File format not supported")
            return redirect(url_for("upload_picture"))
        return redirect(url_for("account"))
    return render_template("upload-picture.html", form=picture_form)


@app.route("/confirm-delete-picture")
@login_required
def confirm_remove():
    return render_template("confirm-remove.html")


@app.route("/delete-picture")
@login_required
def delete_picture():
    user = db.get_or_404(User, current_user.id)
    user.picture_url = None
    db.session.commit()
    return redirect(url_for("profile_picture"))


# @app.route("/verify-email")
# def verify_email():
#     verify_form = VerifyForm()
#     return render_template("verify-email.html", form=verify_form)


if __name__ == "__main__":
    app.run(debug=True)
