from flask import render_template, request, flash, redirect, url_for, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """Route to create a new blog post.

    GET: Renders the post creation form.
    POST: Validates and submits the form data to create a new post in the database.

    Returns:
        Response: Renders template or redirects to the homepage on success.
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created successfully!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    """Route to display a specific blog post by ID. 
    
    Args:
        post_id (int): The ID of the post to display.
    Returns:
        Response: Renders the post detail template with the post data.
    """
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """Update an existing blog post.

    Args:
        post_id (int): ID of the post to be updated.

    GET: Renders a form pre-filled with the post's current data.
    POST: Submits changes and updates the post in the database.

    Returns:
        Response: Redirect to the updated post or 403 if unauthorized.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated successfully!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post.
    Args:
        post_id (int): ID of the post to be deleted.
    Returns:
        Response: Redirects to the homepage after deletion
        or raises 403 if unauthorized.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted successfully!", "success")
    return redirect(url_for("main.home"))