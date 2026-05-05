from flask import Flask, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)
DATA_FILE = "items.txt"

def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return [line.rstrip("\n") for line in f if line.strip()]

def save_items(items):
    with open(DATA_FILE, "w") as f:
        f.write("\n".join(items))

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>My List</title></head>
<body>
    <h1>My List</h1>

    <form method="POST" action="/add">
        <input type="text" name="item" placeholder="New item..." required>
        <button type="submit">Add</button>
    </form>

    {% if items %}
        <ul>
        {% for item in items %}
            <li>
                {{ item }}
                <form method="POST" action="/delete/{{ loop.index0 }}" style="display:inline">
                    <button type="submit">Delete</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No items yet.</p>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE, items=load_items())

@app.route("/add", methods=["POST"])
def add():
    item = request.form.get("item", "").strip()
    if item:
        items = load_items()
        items.append(item)
        save_items(items)
    return redirect(url_for("index"))

@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    items = load_items()
    if 0 <= index < len(items):
        items.pop(index)
        save_items(items)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
