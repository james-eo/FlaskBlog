from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    """Render the home page with paginated blog posts.
    The posts are ordered by date in descending order, showing 5 posts per page.

    Query Params:
        page (int): Page number for pagination. Defaults to 1.

    Returns:
        Response: Rendered template with paginated posts.
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    """Render the about page.
    Returns:
        Response: Rendered template for the about page.
    """
    return render_template("about.html", title='About')