from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login.
 
    This function retrieves the user from the database using the user ID.
    If the user is found, it returns the User object; otherwise, it returns None.
    
    Args:
        user_id (str): The user ID stored in the session
        
    Returns:
        User or None: The User object if found, None otherwise
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User model for storing user account information.
    
    Attributes:
        id (int): Primary key, unique identifier for the user
        username (str): Unique username, maximum 20 characters
        email (str): Unique email address, maximum 120 characters
        password (str): Hashed password, maximum 120 characters
        image_file (str): Profile picture filename, defaults to "default.jpg"
        posts (relationship): One-to-many relationship with Post model
        
    Inherits:
        db.Model: SQLAlchemy model base class
        UserMixin: Flask-Login mixin providing default user session methods
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """Generates a password reset token for the user."""
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        s.dumps({'user_id': self.id})
        return s
    
    @staticmethod
    def verify_reset_token(token):
        """Verifies a password reset token and returns the user if valid."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """String representation of the User object."""
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    Post model for storing blog post information.
    
    Attributes:
        id (int): Primary key, unique identifier for the post
        title (str): Post title, maximum 100 characters
        date_posted (datetime): Timestamp when the post was created, defaults to current UTC time
        content (str): Post content, stored as text with no length limit
        user_id (int): Foreign key referencing the User who created the post
        author (User): Backref relationship to the User model
    
    Inherits:
        db.Model: SQLAlchemy model base class
        
    Relationships:
        author: Many-to-one relationship with User model (accessed via backref)
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    def __repr__(self):
        """String representation of the Post object."""
        return f"Post('{self.title}', '{self.date_posted}')"