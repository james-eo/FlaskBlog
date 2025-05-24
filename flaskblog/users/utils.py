import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail



def save_picture(form_picture):
    """Process and save uploaded profile picture.
    
    Generates a random filename, resizes the image to 125x125 pixels,
    and saves it to the profile_pics directory.
    
    Args:
        form_picture (FileStorage): The image file uploaded via Flask-WTF.
        
    Returns:
        str: The generated filename for database storage.
        
    Example:
        >>> save_picture(uploaded_file)
        'a3f8bc9e.jpg'
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    image_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(image_size)

    image.save(picture_path)
    return picture_fn

def send_reset_email(user):
    """
    Sends a password reset email to the user.

    Args:
        user: User instance for whom the email is being sent.

    - Generates reset token and includes it in the email.
    """
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@ejiks.com", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_password_token', token=token, _external=True)}
If you did not make this request, please ignore this email and no changes will be made.
"""
    mail.send(msg)
    # flash(f"An email has been sent with instructions to reset your password", "info")
    # return redirect(url_for("login"))

