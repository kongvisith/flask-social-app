import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)  # ✅ ត្រឹមត្រូវ

app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Store posts in memory
posts = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content", "")
        image_file = request.files.get("image")

        image_filename = None
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
            image_file.save(image_path)

        posts.append({
            "content": content,
            "image": image_filename,
            "likes": 0,
            "comments": []
        })
        return redirect("/")

    return render_template("index.html", posts=posts)

@app.route("/like/<int:post_id>")
def like(post_id):
    if 0 <= post_id < len(posts):
        posts[post_id]["likes"] += 1
    return redirect("/")

@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):
    comment_text = request.form.get("comment", "")
    if 0 <= post_id < len(posts) and comment_text:
        posts[post_id]["comments"].append(comment_text)
    return redirect("/")

if __name__ == "__main__":  # ✅ ត្រឹមត្រូវ
    app.run(host="0.0.0.0", port=5000, debug=True)