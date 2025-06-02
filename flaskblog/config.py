import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for Flask application.

    Loads environment variables using python-dotenv (.env file).

    Attributes:
        SECRET_KEY (str): Secret key for session and token encryption.
        SQLALCHEMY_DATABASE_URI (str): Database connection URI.
        MAIL_SERVER (str): Email server hostname.
        MAIL_PORT (int): Port used for email server (default 587 for TLS).
        MAIL_USE_TLS (bool): Enable TLS for email.
        MAIL_USERNAME (str): Email server login username.
        MAIL_PASSWORD (str): Email server login password.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORd')