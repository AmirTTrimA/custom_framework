import http.server
import os
import sys
sys.path.append(os.path.abspath('C:\\Users\\BEROOZDG\\OneDrive\\Desktop\\مکتب\\project\\framework'))
from jinja2 import Environment, FileSystemLoader
from urllib.parse import parse_qsl, urlparse
from app.session.session import get_session
from http.cookies import SimpleCookie
from core.routing import resolve


class MyHandler(http.server.SimpleHTTPRequestHandler):
    """handler class for GET and POST"""

    def do_GET(self):
        view_func, kwargs = self.new_method()
        if view_func:
            response = view_func(self, **kwargs)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_error(404, "Page not found")

    def posts_data(self):
        content_length = int(self.headers.get("content-Length"))
        return self.rfile.read(content_length)

    def form_data(self):
        self.POST = dict(parse_qsl(self.posts_data().decode("utf-8")))

    def do_POST(self):
        view_func, kwargs = resolve(self.path)
        if view_func:
            self.form_data()
            response = view_func(self, **kwargs)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_error(404, "Page not found")

    def new_method(self):
        view_func, kwargs = resolve(self.path)
        return view_func, kwargs
    
    def set_cookie(self,name,value):
        self.send_header('Set-Cookie', f'{name}={value}; HttpOnly; Path=/')

    def delete_cookie(self,name,value):
        self.send_header('Set-Cookie', f'{name}=; Max-Age=0; Path=/')
    
    def parse_cookies(self):
        if 'Cookie' in self.headers:
            cookie = SimpleCookie(self.headers['Cookie'])
            if 'session_id' in cookie:
                return cookie['session_id'].value
        return None

    def get_current_user(self):
        session_id = self.parse_cookies()
        if session_id:
            session = get_session(session_id)
            if session:
                return session
        return None

def run_server(urlpatterns):
    """http server starter"""
    PORT = 8000
    with http.server.HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()


def render_template(template_name, context):
    """render jinja templates"""
    template_dir = os.path.join(os.getcwd(), "app", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(context)
