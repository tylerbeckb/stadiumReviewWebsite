from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
# Creates database
db.create_all()