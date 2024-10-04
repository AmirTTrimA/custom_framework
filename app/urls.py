from app.views import register, login, index, posts_view, css, post


urlpatterns = [
    {"path": "/register", "views": register},
    {"path": "/login", "views": login},
    {"path": "/", "views": index},
    {"path": "/post/", "views": post},
    {"path": "/posts", "views": posts_view},
    {"path": "/css", "views": css},
]
