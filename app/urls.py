from app.views import (
    register,login,
    index,about,posts_view,css,post)


urlpatterns = [ 
    {"path":"/register","views":register},
    {"path":"/login","views":login},
    {"path":"/","views":index},
    # {"path":"/about","views":about},
    {"path":"/post","views":post},
    {"path":"/posts","views":posts_view},
    {"path":"/css","views":css}
]