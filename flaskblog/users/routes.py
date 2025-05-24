from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from .utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """Handle user registration.
    
    Processes registration form, validates input, hashes password,
    and creates new user account. Redirects authenticated users.
    
    Returns:
        Response: Either:
            - Redirect to home (if authenticated)
            - Redirect to login (after successful registration)
            - Rendered register template (with form errors if any)
            
    Notes:
        Uses bcrypt for password hashing.
        Flash messages indicate success/failure to user.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}!", "success")
        return redirect(url_for("users.login"))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handles user authentication.
    
    This function renders the login form and processes form submissions.
    If the user is already authenticated, they are redirected to the home page.
    
    Methods:
        GET: Renders the login form
        POST: Processes the login form data and authenticates the user
        
    Returns:
        GET: Rendered login template
        POST: Redirect to next page or home page on successful login
    
    Redirects:
        - To home page if user is already authenticated
        - To next page or home page after successful login
    
    Security Features:
        - Validates the next parameter to prevent open redirect vulnerabilities
        - Handles database exceptions with appropriate error messages
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
        except Exception as e:
            flash("An error occurred while processing your login. Please try again later", "danger")
            return redirect(url_for("users.login"))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Logged in successfully", "success")

            # Ensure 'next_page' is an internal path.
            # Prevent open redirect vulnerability and phishing or malicious site redirections 
            if next_page and not next_page.startswith('/'):
                next_page = None
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Invalid credentials. Please check your email and password", "danger")
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    """
    Handles user logout.
    
    This function logs out the current user and redirects to the login page.
    
    Returns:
        Redirect to login page
    """
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Handles user account management.
    
    This function renders the account form and processes form submissions.
    Users can update their username, email, and profile picture.
    
    Methods:
        GET: Renders the account form pre-populated with current user data
        POST: Processes the account form data and updates the user profile
        
    Returns:
        GET: Rendered account template with pre-populated form
        POST: Redirect to account page on successful update
    
    Decorators:
        login_required: Ensures that only authenticated users can access this route
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated successfully!", "success")
        return redirect(url_for("users.account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    """Displays posts by a specific user.
    
    This function retrieves and displays all posts by a specific user with pagination.
    
    Args:
        username (str): The username of the user whose posts to display
        
    URL Parameters:
        page (int): The page number for pagination (default: 1)
        
    Returns:
        Rendered user_posts template with paginated posts
    Raises:
        404: If the specified username does not exist
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_password_request():
    """
    Handles password reset requests.
    
    This function renders the reset request form and processes form submissions.
    If the user is already authenticated, they are redirected to the home page.
    
    Methods:
        GET: Renders the reset request form
        POST: Processes the reset request form data and sends a reset email
        
    Returns:
        GET: Rendered reset_request template
        POST: Redirect to login page after sending reset email
    
    Redirects:
        - To home page if user is already authenticated
        - To login page after sending reset email
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            return redirect(url_for("users.login"))
        else:
            flash("Email not found. Please check your email and try again", "danger")
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password_token(token):
    """
    Processes password reset tokens.
    
    This function verifies the reset token and processes the reset password form.
    If the user is already authenticated, they are redirected to the home page.
    
    Args:
        token (str): The password reset token to verify
        
    Methods:
        GET: Renders the reset password form
        POST: Processes the reset password form data and updates the user's password
        
    Returns:
        GET: Rendered reset_token template
        POST: Redirect to login page after updating password
    
    Redirects:
        - To home page if user is already authenticated
        - To reset_token route if token is invalid or expired
        - To login page after updating password
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid or expired token. Please try again", "danger")
        return redirect(url_for("users.reset_token"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated successfully!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)