from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db initialization
from .activity_review import ActivityReview