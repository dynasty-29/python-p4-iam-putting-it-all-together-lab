from sqlalchemy.exc import IntegrityError
import pytest
from app import app
from models import db, User, Recipe

class TestUser:
    '''User in models.py'''

    def test_has_attributes(self):
        '''has attributes username, _password_hash, image_url, and bio.'''

        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username="Liz",
                image_url="https://example.com/image.jpg",
                bio="Sample bio for user Liz."
            )
            user.password_hash = "securepassword"
            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter_by(username="Liz").first()

            assert created_user.username == "Liz"
            assert created_user.image_url == "https://example.com/image.jpg"
            assert created_user.bio == "Sample bio for user Liz."

    def test_requires_username(self):
        '''requires each record to have a username.'''

        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User()
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_unique_username(self):
        '''requires each record to have a unique username.'''

        with app.app_context():
            User.query.delete()
            db.session.commit()

            user1 = User(username="Ben")
            user1.password_hash = "securepassword"
            db.session.add(user1)
            db.session.commit()

            user2 = User(username="Ben")
            user2.password_hash = "anotherpassword"
            with pytest.raises(IntegrityError):
                db.session.add(user2)
                db.session.commit()

    def test_has_list_of_recipes(self):
        '''has records with lists of recipes records attached.'''

        with app.app_context():
            User.query.delete()
            Recipe.query.delete()
            db.session.commit()

            user = User(username="Prabhdip")
            user.password_hash = "securepassword"
            db.session.add(user)
            db.session.commit()

            recipe1 = Recipe(
                title="Delicious Shed Ham",
                instructions="A" * 60,
                minutes_to_complete=60,
                user_id=user.id
            )
            recipe2 = Recipe(
                title="Hasty Party Ham",
                instructions="B" * 60,
                minutes_to_complete=30,
                user_id=user.id
            )

            db.session.add_all([recipe1, recipe2])
            db.session.commit()

            assert recipe1 in user.recipes
            assert recipe2 in user.recipes
