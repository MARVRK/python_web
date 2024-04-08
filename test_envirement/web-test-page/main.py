# from jinja2 import Template

# name = 'Bill'
# age = 28

# tm = Template("My name is {{ name }} and I am {{ age }}")
# msg = tm.render(name=name, age=age)

# print(msg)  # My name is Bill and I am 28
###########################################\


# from jinja2 import Template

# persons = [
#     {'name': 'Andrej', 'age': 34},
#     {'name': 'Mark', 'age': 17},
#     {'name': 'Thomas', 'age': 44},
#     {'name': 'Lucy', 'age': 14},
#     {'name': 'Robert', 'age': 23},
#     {'name': 'Dragomir', 'age': 54}
# ]

# rows_tmp = Template("""{% for person in persons -%}
#     {{ person.name }} {{ person.age }}
# {% endfor %}""")

# print(rows_tmp.render(persons=persons))

#############################################
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from pathlib import Path
import os

BASE_DIR = Path()

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        match pr_url.path:
            case '/':
                self.send_html_file("index.html")
            case '/contact':
                self.send_html_file("contact.html")
            case '/blog':
                self.send_html_file("blog.html")
            case _:
                file = BASE_DIR.joinpath(pr_url.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html_file("404.html")


    def send_html_file(self, path, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(path, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, path, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(path, 'rb') as fd:
            self.wfile.write(fd.read())
    

def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 8000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


os.chdir('D:/Nextcloud/Courses_Python/Storage_Code/python_web/test_envirement/web-test-page')
path='D:/Nextcloud/Courses_Python/Storage_Code/python_web/test_envirement/web-test-page'
print(os.listdir())

if __name__ == '__main__':
    run()

