"""views for each request passing data via models"""
from sqlalchemy.orm import Session
from app.migartions import engine

from core.http import render_template

from app.models import User, Address


def index(request):
    context = {"title": "Home", "message": "Welcome to the Home Page"}
    return render_template("index.html", context)


def about(request):
    context = {"title": "About", "message": "This is the About Page"}
    return render_template("about.html", context)


def register(request):
    """to handle data view in register.html"""
    if request.command == "POST":
        data = request.POST
        with Session(engine) as session:
            user = User(
                username=data["username"],
                password=data["password1"],
                email=data["email"],
            )
            session.add(user)
            session.commit()
        return render_template(
            "register.html",
            {"message": f'user {data["username"]} is registered successfully!'},
        )

    elif request.command == "GET":
        return render_template("register.html", {})


def posts_view(request):
    """to handle post view in posts.html"""
    contex = {}
    if request.command == "POST":
        new_post = request.POST.get("new_post")
        return render_template("posts.html", contex)

    elif request.command == "GET":
        return render_template("posts.html", contex)
