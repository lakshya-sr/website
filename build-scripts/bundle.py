  
import re
import sys
import os

def substitute_files(contents):
    def replace_with_file(match):
        filename = match.group(1)
        try:
            with open(filename) as f:
                return f.read()
        except FileNotFoundError:
            return f"<!--[File {filename} not found]-->"

    return re.sub(r"<!--{{(.*?)}}-->", replace_with_file, contents)

def add_blogs(contents, blog_directory):
    blog_files = [i for i in os.scandir(path=blog_directory) if i.is_file()]

    def insert_blog_index(match):
        res = "<section id=\"blogs\">\n"
        for blog in blog_files:
            with open(blog) as f:
                contents = f.read()
                title = re.findall(r"<title>(.*)</title>", contents)[0]
                summary = re.findall(r'<section id="summary">(.*)</section>', contents)[0]

            res += f"\t\t<a href=\"blogs/{blog.name}\">\n\t\t\t<article>\n\t\t\t\t<h3>{title}</h3>\n\t\t\t\t<p>{summary}</p>\n\t\t\t</article>\n\t\t</a>".replace("\t", "    ")
        res += "</section>\n"
        return res
    
    return re.sub(r"<!--\[\[.*?\]\]-->", insert_blog_index, contents)


if __name__ == "__main__":
    build_dir = "./build"
    blogs_dir = "./blogs"
    for file in sys.argv[1:]:
        with open(file, "r") as f:
            content = f.read()
            new_text = add_blogs(substitute_files(content), blogs_dir)
            
        with open(f"{build_dir}/{file}", "w") as f:
            f.write(new_text)
