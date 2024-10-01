from app.views import (
    register,login,
    index,about,posts_view)


urlpatterns = [ 
    {"path":"/register","views":register},
    {"path":"/login","views":login},
    {"path":"/","views":index},
    {"path":"/about","views":about},
    {"path":"/posts","views":posts_view},

]