import os
import shutil

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = "content"
OUTPUT_DIR = "dist/garden"
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"


def build():
    # 1. Подготовка папки назначения
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Копирование статики (логотип, css)
    out_static = os.path.join(OUTPUT_DIR, "static")
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, out_static)

    # 3. Настройка шаблонизатора Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("base.html")

    # 4. Рендеринг всех заметок из Обсидиана
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                post = frontmatter.load(filepath)

                # Парсим Markdown
                html_content = markdown.markdown(
                    post.content, extensions=["fenced_code", "tables", "nl2br"]
                )

                title = post.get("title", file.replace(".md", "").capitalize())

                rendered_html = template.render(title=title, content=html_content)

                # Формируем имя выходящего файла
                rel_dir = os.path.relpath(root, CONTENT_DIR)
                target_dir = (
                    os.path.join(OUTPUT_DIR, rel_dir) if rel_dir != "." else OUTPUT_DIR
                )
                os.makedirs(target_dir, exist_ok=True)

                out_filename = (
                    "index.html"
                    if file.lower() == "index.md"
                    else file.replace(".md", ".html")
                )
                out_path = os.path.join(target_dir, out_filename)

                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(rendered_html)

    print("=== DIGITAL GARDEN УСПЕШНО СОБРАН В ПИТОНЕ ===")


if __name__ == "__main__":
    build()
