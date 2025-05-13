from app import app, db, User

def add_user():
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username='sandeep123@gmail.com').first()
        if existing_user:
            print("User already exists!")
            return

        # Create new user
        user = User(
            username='sandeep123@gmail.com',
            email='sandeep123@gmail.com'
        )
        user.set_password('Sandeep@123')
        
        try:
            db.session.add(user)
            db.session.commit()
            print("User added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding user: {str(e)}")

if __name__ == '__main__':
    add_user() 