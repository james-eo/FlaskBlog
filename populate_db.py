import json
from flaskblog import db, app
from flaskblog.models import Post, User

# Load posts from JSON
with open('posts.json') as f:
    posts = json.load(f)

# Use a default user for all posts
# Fetch the first user or a specific user by email/username
default_user = User.query.first()  

if not default_user:
    raise ValueError("No default user found. Please create a user in the database.")

# Add posts to the database
for post in posts:
    if not Post.query.filter_by(title=post['title']).first():
        new_post = Post(
            title=post['title'],
            content=post['content'],
             # Assign the default user's ID to the post
            user_id=default_user.id 
        )
        db.session.add(new_post)

# Commit all changes
db.session.commit()
print("Database populated with posts from posts.json")