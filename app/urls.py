from app.views import register,index,about,posts_view


urlpatterns = [ 
    {"path":"/register","views":register},
    {"path":"/","views":index},
    {"path":"/about","views":about},
    {"path":"/posts","views":posts_view},

]