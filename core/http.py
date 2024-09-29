import http.server
from jinja2 import Environment, FileSystemLoader
from framework.routing import resolve
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        view_func, kwargs = resolve(self.path)
        if view_func:
            response = view_func(self, **kwargs)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_error(404, "Page not found")

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
