import pytest
from app import app
from config.db import db
from config.db.models import User

@pytest.fixture
def client():
    # Set up Flask test client and application context
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "postgresql://postgres:123qwe@localhost:5432/test_cryptoTradingBot"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Ensure tables are created before running tests
        yield client

        with app.app_context():
            db.drop_all()  # Clean up the database after tests

def test_user_creation(client):
    with app.app_context():  # Explicitly use the app context for database operations
        new_user = User(username="test_user", email="test_user@example.com")
        db.session.add(new_user)
        db.session.commit()

        # Query the database to verify the user was added
        user = User.query.filter_by(username="test_user").first()
        assert user is not None
        assert user.email == "test_user@example.com"
