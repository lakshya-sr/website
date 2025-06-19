from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import re
import shutil
import os

logging = True

def log(msg):
    if logging:
        print(msg)

def load_projects():
    file = 'projects.json'
    with open(file) as f:
        projects = json.load(f)
        return projects

def load_blogs():
    file = 'blogs.json'
    with open(file) as f:
        blogs = json.load(f)
        for blog in blogs:
            with open(f"blogs/{blog['contents']}") as f2:
                blog['contents'] = f2.read()
            blog['images'] = re.findall("!\[]\((.*)\)", blog['contents'])

        return blogs

def load_services():
    file = 'services.json'
    with open(file) as f:
        return json.load(f)

def render_markdown(text, path):
    import markdown
    contents = markdown.markdown(text)
    return contents

def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
    except FileNotFoundError as e:
        log(str(e))

def escape_title(title):
    title = title.lower()
    for c in "_ ,;":
        title = title.replace(c,"-")
    return title

def prepare_build_dir():
    shutil.rmtree('build/blogs')
    shutil.rmtree('build/static')
    os.mkdir('build/blogs')
    files = os.listdir('build')
    for file in files:
        if file.endswith('.html') or file.endswith('.pdf'):
            os.remove(f"build/{file}")
    shutil.copytree('static', 'build/static')
    resume = "../resume/resume.pdf"
    shutil.copy(resume, 'build/resume.pdf')
    shutil.copy('CNAME', 'build/CNAME')


prepare_build_dir()

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

home = env.get_template("index.html")
with open("build/index.html", "w") as f:
    f.write(home.render())

projects_list = load_projects()
projects = env.get_template("projects.html")
with open("build/projects.html", "w") as f:
    f.write(projects.render(projects_list=projects_list))

blogs_list = load_blogs()
for blog in blogs_list:
    filename = escape_title(blog['title']) + '.html'
    contents = render_markdown(blog['contents'], path='static')
    template = env.get_template('blog-template.html')
    with open(f'build/blogs/{filename}', "w") as f:
        f.write(template.render(contents=contents, title=blog['title']))
    for image in blog['images']:
        copy_file(f'static/{image}', f'build/static/{image}')
    blog['link'] = f"blogs/{filename}"
blog = env.get_template('blog.html')
with open('build/blog.html', "w") as f:
    f.write(blog.render(blogs_list=blogs_list))

services = env.get_template('services.html')
with open('build/services.html', "w") as f:
    f.write(services.render(services=load_services()))


