import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, root_path='./templates')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
sqlalchemy_database_uri = 'mysql+pymysql://{username}:{password}@{hostname}/{databasename}'.format(
    username=os.environ.get('DB_USERNAME'),
    password=os.environ.get('DB_PASSWORD'),
    hostname='remotemysql.com',
    databasename=os.environ.get('DB_NAME'),
)

app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Teams(db.Model):
    reg_id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    players = db.Column(db.Integer)
    email = db.Column(db.String(256))
    mobile = db.Column(db.String(10))
    player1 = db.Column(db.String(256))
    player2 = db.Column(db.String(256))
    player3 = db.Column(db.String(256))
    player4 = db.Column(db.String(256))
    player5 = db.Column(db.String(256))
    player6 = db.Column(db.String(256))
    player7 = db.Column(db.String(256))
    player1_id = db.Column(db.Integer)
    player2_id = db.Column(db.Integer)
    player3_id = db.Column(db.Integer)
    player4_id = db.Column(db.Integer)
    player5_id = db.Column(db.Integer)
    player6_id = db.Column(db.Integer)
    player7_id = db.Column(db.Integer)
    receipt = db.Column(db.String(256))
    status = db.Column(db.String(256))

    def __repr__(self):
        return f'Name: {self.name} ' \
               f'Email: {self.email}' \
               f'Players: {self.players}' \
               f'Player1: {self.player1} ' \
               f'Player2: {self.player2} ' \
               f'Player3: {self.player3} ' \
               f'Player4: {self.player4} ' \
               f'Player5: {self.player5} ' \
               f'Player6: {self.player6} ' \
               f'Player7: {self.player7} '
