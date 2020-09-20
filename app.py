from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

from mail_client import MailClient

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{hostname}/{databasename}'.format(
    username=os.environ.get('USERNAME'),
    password=os.environ.get('PASSWORD'),
    hostname='remotemysql.com',
    databasename=os.environ.get('DATABASENAME'),
)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Teams(db.Model):
    name = db.Column(db.String(256), primary_key=True)
    players = db.Column(db.Integer)
    email = db.Column(db.String(256))
    player1 = db.Column(db.String(256))
    player2 = db.Column(db.String(256))
    player3 = db.Column(db.String(256))
    player4 = db.Column(db.String(256))
    player5 = db.Column(db.String(256))
    player6 = db.Column(db.String(256))
    player7 = db.Column(db.String(256))
    receipt = db.Column(db.String(256))

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


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    team = Teams()
    count = 5
    team.name = team_name = request.form['team_name']
    if Teams.query.filter_by(name=team_name).first():
        return 'Team name already registered. Try using other names(s).'
    team.email = email = request.form['email']
    team.player1 = request.form['player1']
    team.player2 = request.form['player2']
    team.player3 = request.form['player3']
    team.player4 = request.form['player4']
    team.player5 = request.form['player5']
    if hasattr(request.form, 'player6'):
        team.player6 = request.form['player6']
        count += 1
    else:
        team.player6 = '-'
    if hasattr(request.form, 'player7'):
        team.player7 = request.form['player7']
        count += 1
    else:
        team.player7 = '-'
    team.receipt = request.form['receipt']
    team.players = count
    try:
        db.session.add(team)
        db.session.commit()
    except Exception:
        return f'Error in registaring the Team {team_name}. Please try again sometime.'
    else:
        if team.name:
            MailClient.send_registration_cofirmation(email)
            return f'Team {team_name} registered successfully'
        else:
            return f'Error in registaring the Team {team_name}. Please try again sometime.'


if __name__ == '__main__':
    app.run()
