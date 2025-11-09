import os
from flask import Blueprint , render_template

template_dir = os.path.abspath("src/front_layer/templates")

users = Blueprint('users' , __name__ , template_folder=template_dir)

@users.route("/")
def ShowUserHome():
    return render_template("users_home.html")