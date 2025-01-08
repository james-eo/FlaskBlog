from flaskblog import app, db, User, Post


with app.app_context():
    # create tables
    db.create_all()
    print("Database created successfully")

    # create users
    user_1 = User(username='Clark', email="smith@company.com", password="password")
    user_2 = User(username='John', email="jonhn@company.com", password="password")
    user_3 = User(username='Jane', email="jane@company.com", password="password")
    
    # add users to the database
    db.session.add_all([user_1, user_2, user_3]) 

    # commit the changes
    db.session.commit()