from faker import Faker
from random import randint
import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from models import db, Recipe, User

class TestRecipe:
    '''Recipe in models.py'''

    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():
            Recipe.query.delete()
            db.session.commit()

            user = User(username="TitleTestUser")
            user.password_hash = "password123"
            db.session.add(user)
            db.session.commit()

            # Try to create a recipe without a title
            with pytest.raises(TypeError):
                recipe = Recipe(
                    instructions="A" * 60,
                    minutes_to_complete=10,
                    user_id=user.id
                )

            # Correct way to create the recipe with a title
            recipe = Recipe(
                title="Valid Recipe",
                instructions="A" * 60,
                minutes_to_complete=10,
                user_id=user.id
            )
            db.session.add(recipe)
            db.session.commit()

            assert recipe.title == "Valid Recipe"
            
class TestRecipeIndex:
    '''RecipeIndex resource in app.py'''

    def test_lists_recipes_with_200(self):
        '''returns a list of recipes associated with the logged in user and a 200 status code.'''

        with app.app_context():
            # Clear previous data
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            fake = Faker()

            # Create a user and commit to the database to ensure user.id is generated
            user = User(
                username="Slagathor",
                bio=fake.paragraph(nb_sentences=3),
                image_url=fake.url(),
            )
            user.password_hash = 'secret'
            db.session.add(user)
            db.session.commit()  # Commit to generate user.id

            # Refresh the user object to make sure user.id is available
            db.session.refresh(user)

            recipes = []
            for i in range(15):
                instructions = fake.paragraph(nb_sentences=8)

                # Include the user_id when creating the recipe
                recipe = Recipe(
                    title=fake.sentence(),
                    instructions=instructions,
                    minutes_to_complete=randint(15, 90),
                    user_id=user.id  # Correctly associate the recipe with the user
                )
                db.session.add(recipe)
                recipes.append(recipe)

            db.session.commit()

            # Query the database to verify recipes were created
            user_recipes = Recipe.query.filter_by(user_id=user.id).all()

            # Assert the number of recipes created and linked to the user
            assert len(user_recipes) == 15
            assert all(recipe in user_recipes for recipe in recipes)