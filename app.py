from flask import Flask, render_template, request, url_for, redirect, session
import flask_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
from flask_session import Session

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///home/vedant/Developer/python_projects/roman_wing_website/blog.db"
db = SQLAlchemy(app)
Session(app)

class Editor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password_hash = db.Column(db.String(50))
	email = db.Column(db.String(50))


class blog_post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	subtitle = db.Column(db.String(50))
	author = db.Column(db.String(20))
	date_posted = db.Column(db.DateTime)
	body = db.Column(db.Text)

@app.route("/")
def main_page():
	posts = blog_post.query.order_by(blog_post.date_posted.desc()).all()
	return render_template("index.html", posts=posts)

# Post-related stuff
@app.route("/new")
def make_new_post():
	if "id" not in session:
		return redirect("/")
	return render_template("new_post.html")

@app.route("/post_created", methods=["POST"])
def post_created():
	title = request.form["title"]
	subtitle = request.form["subtitle"]
	author = request.form["author"]
	body = request.form["body"]
	post = blog_post(title=title, subtitle=subtitle, author=author, body=body, date_posted=datetime.now())
	db.session.add(post)
	db.session.commit()
	return redirect("/post/{}".format(post.id))

@app.route("/post/<int:post_id>")
def get_post(post_id):
	post = blog_post.query.filter_by(id=post_id).one()
	return render_template("post.html", post=post)

# Login-related stuff
@app.route("/edtitorLogin")
def admin_loginPage():
	return render_template("login.html")

@app.route("/doLogin", methods=["POST"])
def do_login():
	username = request.form.get["username"]
	password = request.form["password"]
	user = Editor.query.filter_by(username=username).one()
	if bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
		session["id"] = user.id
		return redirect("/editor/{}".format(user.id))
	else:
		error = "Error: incorrect password"
		return render_template("login.html", error=error)

@app.route("/editor/<int:editor_id>")
def show_editor_tools(editor_id):
	if "id" not in session:
		return redirect("/")
	user = Editor.query.filter_by(id=editor_id).one()
	return render_template("editor_page.html", user=user)


if __name__ == "__main__":
	app.run(debug=True, load_dotenv=False)