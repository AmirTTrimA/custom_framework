import http.server
from jinja2 import Environment, FileSystemLoader
from core.routing import resolve
import os
from urllib.parse import parse_qsl,urlparse

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        view_func, kwargs = self.new_method()
        if view_func:
            self.form_data()
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
        self.POST=dict(parse_qsl(self.posts_data().decode("utf-8")))

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
        return view_func,kwargs

def run_server(urlpatterns):
    PORT = 8000
    with http.server.HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

def render_template(template_name, context):
    template_dir = os.path.join(os.getcwd(), 'app', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(context)
