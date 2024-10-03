# from jinja2 import Environment,FileSystemLoader
# import os

# class MyHandler(http.server.SimpleHTTPRequestHandler):

#     def parse_cookies(self):

#         if 'cookie' in self.headers:
#             cookie = SimpleCookie(self.headers['cookie'])
#             if 'session_id' in cookie:
#                 return cookie['session_id'].value
#         return None
    
#     def get_current_user(self):


#     def set_cookie(self,name,value):

#         self.semd_header()'set-Cookie,f'{name}={value}    