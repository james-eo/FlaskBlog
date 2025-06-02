from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """Form class for creating or updating a blog post.

    Attributes:
        title (StringField): Field for the post title. Required.
        content (TextAreaField): Field for the post content. Required.
        submit (SubmitField): Submit button labeled 'Post'.
    """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')