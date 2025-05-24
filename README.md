# Flask Blog

A full-featured blog application built with Flask, featuring user authentication, post management, and profile customization.

![Blog Home Page](https://images.pexels.com/photos/262508/pexels-photo-262508.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)

## Features

- User Authentication (Register, Login, Logout)
- Password Reset via Email
- User Profile Management
- Create, Read, Update, Delete Blog Posts
- Pagination
- User Profile Pictures
- Error Pages (404, 403, 500)

![Blog Features](https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)

## Technology Stack

- **Backend**: Flask
- **Database**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Password Hashing**: Bcrypt
- **Email Support**: Flask-Mail
- **Frontend**: Bootstrap 5
- **Image Processing**: Pillow

![Tech Stack](https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URI=sqlite:///site.db
   MAIL_SERVER=smtp.googlemail.com
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASSWORD=your_email_password
   ```
5. Initialize the database:
   ```bash
   python create_db.py
   ```
6. Run the application:
   ```bash
   python run.py
   ```

## Project Structure

```
flaskblog/
├── __init__.py
├── config.py
├── models.py
├── static/
│   ├── main.css
│   └── profile_pics/
├── templates/
│   ├── layout.html
│   ├── home.html
│   └── ...
├── users/
│   ├── forms.py
│   ├── routes.py
│   └── utils.py
├── posts/
│   ├── forms.py
│   └── routes.py
└── errors/
    └── handlers.py
```

![Project Structure](https://images.pexels.com/photos/1181298/pexels-photo-1181298.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)

## Features in Detail

### User Management
- User registration with username and email validation
- Secure password hashing
- User authentication
- Profile picture upload and automatic resizing
- Profile information updates

### Blog Posts
- Create, edit, and delete posts
- Rich text content
- Post pagination
- Author-specific post views
- Post update and deletion authorization

### Security Features
- Password hashing
- User session management
- CSRF protection
- Secure password reset
- Route protection

### Error Handling
- Custom error pages
- Proper error messages
- User-friendly error descriptions

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask Documentation
- Bootstrap Documentation
- Python Community
- Stack Overflow Community