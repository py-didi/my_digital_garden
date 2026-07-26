import json
import os
import re
import shutil

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = "content"
OUTPUT_DIR = "garden"
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"


def parse_wikilinks(text):
    def replacer(match):
        target = match.group(1).strip()
        label = match.group(2).strip() if match.group(2) else target

        if target.lower() in ["index", "home", "welcome"]:
            url = "/garden/"
        else:
            url = f"/garden/{target}.html"

        return f'<a href="{url}" class="internal-link">{label}</a>'

    pattern = r"\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]"
    return re.sub(pattern, replacer, text)


def build():
    # 1. Очищаем/создаем папку garden
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Копируем статику
    out_static = os.path.join(OUTPUT_DIR, "static")
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, out_static)

    # 3. Сканируем папку static/logos/
    logos_dir = os.path.join(STATIC_DIR, "logos")
    logo_files = []

    if os.path.exists(logos_dir):
        for file in os.listdir(logos_dir):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                logo_files.append(f"/garden/static/logos/{file}")

    # Фоллбэк, если папка пуста или её нет
    if not logo_files:
        logo_files = ["/garden/static/logo.png"]

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("base.html")

    # 4. Собираем посты для бокового меню
    posts = []
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                post = frontmatter.load(filepath)

                rel_dir = os.path.relpath(root, CONTENT_DIR)
                out_filename = (
                    "index.html"
                    if file.lower() == "index.md"
                    else file.replace(".md", ".html")
                )

                url = (
                    f"/garden/{rel_dir}/{out_filename}"
                    if rel_dir != "."
                    else f"/garden/{out_filename}"
                )
                if file.lower() == "index.md" and rel_dir == ".":
                    url = "/garden/"

                title = post.get("title", file.replace(".md", "").capitalize())
                posts.append(
                    {
                        "title": title,
                        "url": url,
                        "is_index": file.lower() == "index.md" and rel_dir == ".",
                    }
                )

    posts.sort(key=lambda x: (0 if x["is_index"] else 1, x["title"]))

    # 5. Генерация HTML
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                post = frontmatter.load(filepath)

                content_with_links = parse_wikilinks(post.content)

                html_content = markdown.markdown(
                    content_with_links, extensions=["fenced_code", "tables", "nl2br"]
                )

                title = post.get("title", file.replace(".md", "").capitalize())
                rel_dir = os.path.relpath(root, CONTENT_DIR)
                out_filename = (
                    "index.html"
                    if file.lower() == "index.md"
                    else file.replace(".md", ".html")
                )

                current_url = (
                    f"/garden/{rel_dir}/{out_filename}"
                    if rel_dir != "."
                    else f"/garden/{out_filename}"
                )
                if file.lower() == "index.md" and rel_dir == ".":
                    current_url = "/garden/"

                target_dir = (
                    os.path.join(OUTPUT_DIR, rel_dir) if rel_dir != "." else OUTPUT_DIR
                )
                os.makedirs(target_dir, exist_ok=True)

                rendered_html = template.render(
                    title=title,
                    content=html_content,
                    posts=posts,
                    current_url=current_url,
                    logos_json=json.dumps(logo_files),  # Передаем JSON-массив логотипов
                )

                out_path = os.path.join(target_dir, out_filename)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(rendered_html)

    print(f"=== СКОМПИЛИРОВАНО (Найдено логотипов: {len(logo_files)}) ===")


if __name__ == "__main__":
    build()
