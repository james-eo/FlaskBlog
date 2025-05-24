from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User



class RegistrationForm(FlaskForm):
    """Handles user registration with validation.
    
    Attributes:
        username (StringField): Username input with length validation.
        email (StringField): Email input with format validation.
        password (PasswordField): Password input.
        confirm_password (PasswordField): Must match password field.
        submit (SubmitField): Registration submission button.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Checks if username already exits.
        
        Args:
            username (str): The username to validate.
            
        Raises:
            ValidationError: If username already exists in database.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """Checks if email is already registered.
        
        Args:
            email (str): The email to validate.
            
        Raises:
            ValidationError: If email already exists in database.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    """Handles user login with validation.
    
    Attributes:
        email (StringField): Email input with format validation.
        password (PasswordField): Password input.
        remember (BooleanField): Option to remember user session.
        submit (SubmitField): Login submission button.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Handles user account updates with validation.

    Attributes:
        username (StringField): Username input with length validation.
        email (StringField): Email input with format validation.
        picture (FileField): Profile picture upload with file type validation.
        submit (SubmitField): Update submission button.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Checks if username already exists.
        Args:
            username (str): The username to validate.
        Raises:
            ValidationError: If username already exists in database.

        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """Checks if email is already registered.
        Args:
            email (str): The email to validate.
        Raises:
            ValidationError: If email already exists in database.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists. Please choose a different one.")
            

class ResetPasswordRequestForm(FlaskForm):
    """Handles password reset requests with validation.

    Attributes:
        email (StringField): Email input with format validation.
        submit (SubmitField): Password reset request submission button.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """Checks if email is registered.
        Args:
            email (str): The email to validate.
        Raises:
            ValidationError: If email does not exist in database.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    """Form to request a password reset.

    Fields:
        - email: Required, must be a registered email.
        - submit: Submit button.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')