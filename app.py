import os
from flask import Flask, request, redirect, url_for, render_template
import uuid # For generating unique filenames for uploaded images

# Initialize the Flask application
# We specify 'templates' and 'static' folders explicitly for clarity
app = Flask(__name__, template_folder='templates', static_folder='static')

# --- Configuration for File Uploads ---
# Define the folder where uploaded images will be stored
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# --- In-memory Data Storage ---
# This list will act as our "database" for posts.
# In a real application, you would use a proper database like PostgreSQL, MySQL,
# or NoSQL databases like MongoDB or Firebase Firestore.
# Each item in the list is a dictionary representing a post.
# {
#   'content': '...',
#   'image': 'filename.jpg' or None,
#   'likes': 0,
#   'comments': ['comment1', 'comment2']
# }
posts = []

# --- Helper Function for File Uploads ---
def allowed_file(filename):
    """
    Checks if a file's extension is allowed.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Handles the home page, displaying posts and allowing new post creation.
    - GET: Renders the index.html template with all existing posts.
    - POST: Processes new post submissions, including text content and image uploads.
    """
    if request.method == 'POST':
        content = request.form['content']
        image_filename = None

        # Check if an image file was uploaded
        if 'image' in request.files:
            file = request.files['image']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename != '' and allowed_file(file.filename):
                # Generate a unique filename to prevent overwrites
                unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                image_filename = unique_filename
            elif file.filename != '' and not allowed_file(file.filename):
                print(f"File {file.filename} not allowed. Only {ALLOWED_EXTENSIONS} are permitted.")
                # You might want to add a message to the user here
                # For this simple app, we'll just skip saving the image
                pass

        # Create a new post dictionary
        new_post = {
            'content': content,
            'image': image_filename,
            'likes': 0,
            'comments': []
        }
        posts.append(new_post)
        print(f"New post created: {new_post}")
        # Redirect to the home page to show the updated list of posts
        return redirect(url_for('home'))

    # For GET requests, render the home page with the current posts
    return render_template('index.html', posts=posts)

@app.route('/like/<int:post_id>')
def like_post(post_id):
    """
    Handles liking a post.
    - post_id: The index of the post in the 'posts' list.
    """
    if 0 <= post_id < len(posts):
        posts[post_id]['likes'] += 1
        print(f"Post {post_id} liked. Total likes: {posts[post_id]['likes']}")
    else:
        print(f"Attempted to like invalid post ID: {post_id}")
    # Redirect back to the home page
    return redirect(url_for('home'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    """
    Handles adding a comment to a post.
    - post_id: The index of the post in the 'posts' list.
    """
    if 0 <= post_id < len(posts):
        comment_text = request.form['comment']
        if comment_text:
            posts[post_id]['comments'].append(comment_text)
            print(f"Comment added to post {post_id}: {comment_text}")
        else:
            print(f"Empty comment submitted for post {post_id}")
    else:
        print(f"Attempted to comment on invalid post ID: {post_id}")
    # Redirect back to the home page
    return redirect(url_for('home'))

# --- Main Application Run ---
if __name__ == '__main__':
    # Create the 'static/uploads' directory if it doesn't exist.
    # This is crucial for storing uploaded images.
    uploads_dir = os.path.join(app.root_path, UPLOAD_FOLDER)
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"Created uploads directory: {uploads_dir}")

    # Create the 'templates' directory if it doesn't exist
    templates_dir = os.path.join(app.root_path, 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"Created templates directory: {templates_dir}")

    # Create the 'static' directory if it doesn't exist (for style.css)
    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"Created static directory: {static_dir}")

    # Run the Flask app in debug mode.
    # debug=True allows for automatic reloading on code changes and provides a debugger.
    app.run(debug=True)
