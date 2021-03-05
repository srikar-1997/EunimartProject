from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(200), nullable = False, primary_key = True)
    hash = db.Column(db.String(200), nullable = False)
    
    def __init__(self, email, hash):
        self.email = email
        self.hash = hash


class Candidates(db.Model):
    __tablename__ = "candidates"
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    no_of_votes = db.Column(db.Integer, nullable = False)
    
    def __init__(self, id, noOfVotes):
        self.id = id
        self.hash = hash
