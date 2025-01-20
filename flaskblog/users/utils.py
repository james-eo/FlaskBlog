import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    image_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(image_size)

    image.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@ejiks.com", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_password_token', token=token, _external=True)}
If you did not make this request, please ignore this email and no changes will be made.
"""
    mail.send(msg)
    # flash(f"An email has been sent with instructions to reset your password", "info")
    # return redirect(url_for("login"))

