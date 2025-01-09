from flaskblog import app, db, User, Post


# with app.app_context():
#     # create tables
#     db.create_all()
#     print("Database created successfully")

#     # create users
#     user_1 = User(username='Clark', email="smith@company.com", password="password")
#     user_2 = User(username='John', email="jonhn@company.com", password="password")
#     user_3 = User(username='Jane', email="jane@company.com", password="password")

    
    
#     # add users to the database
#     db.session.add_all([user_1, user_2, user_3]) 

#     # commit the changes
#     db.session.commit()

# user = User.query.first()
# # create posts

# # post_1 = Post(title='Blog Post 1', content='First post content', user_id=user.id)
# post_2 = Post(title='Blog Post 2', content='Second post content', user_id=user.id)
# post_3 = Post(title='Blog Post 3', content='Third post content', user_id=user.id)

# # add posts to the database

# db.session.add_all([post_2, post_3])

# # commit the changes

# db.session.commit()

# # close the session
# db.session.close()

# delete the database
db.drop_all()
print("Database deleted successfully")

# Create the database with new tables
db.create_all()
print("Database created successfully")

