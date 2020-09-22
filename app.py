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
    player1_id = db.Column(db.Integer)
    player2_id = db.Column(db.Integer)
    player3_id = db.Column(db.Integer)
    player4_id = db.Column(db.Integer)
    player5_id = db.Column(db.Integer)
    player6_id = db.Column(db.Integer)
    player7_id = db.Column(db.Integer)
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
    query = Teams.query.filter_by(name=team_name).first()
    if query:
        return render_template('response.html', message=f'Team "{team_name}" is already registered. '
                                                        f'Try using other names(s).')
    team.email = email = request.form['email']
    query = Teams.query.filter_by(email=email).first()
    if query:
        return render_template('response.html', message=f'Email "{email}" is already registered. '
                                                        f'Try using another email.')
    team.player1, team.player1_id = request.form['player1'], request.form['player1_id']
    query = Teams.query.filter_by(player1_id=team.player1_id).first()
    if query:
        return render_template('response.html', message=f'Player with ID "{team.player1_id}" is already registered in '
                                                        f'the Team {query.name}')
    team.player2, team.player2_id = request.form['player2'], request.form['player2_id']
    query = Teams.query.filter_by(player2_id=team.player2_id).first()
    if query:
        return render_template('response.html', message=f'Player with ID "{team.player2_id}" is already registered in '
                                                        f'the Team {query.name}')
    team.player3, team.player3_id = request.form['player3'], request.form['player3_id']
    query = Teams.query.filter_by(player3_id=team.player3_id).first()
    if query:
        return render_template('response.html', message=f'Player with ID "{team.player3_id}" is already registered in '
                                                        f'the Team {query.name}')
    team.player4, team.player4_id = request.form['player4'], request.form['player4_id']
    query = Teams.query.filter_by(player4_id=team.player4_id).first()
    if query:
        return render_template('response.html', message=f'Player with ID "{team.player4_id}" is already registered in '
                                                        f'the Team {query.name}')
    team.player5, team.player5_id = request.form['player5'], request.form['player5_id']
    query = Teams.query.filter_by(player5_id=team.player5_id).first()
    if query:
        return render_template('response.html', message=f'Player with ID "{team.player5_id}" is already registered in '
                                                        f'the Team {query.name}')
    if hasattr(request.form, 'player6'):
        team.player6, team.player6_id = request.form['player6'], request.form['player6_id']
        query = Teams.query.filter_by(player6_id=team.player6_id).first()
        if query:
            return render_template('response.html', message=f'Player with ID "{team.player6_id}" is already registered '
                                                            f'in the Team {query.name}')
        count += 1
    if hasattr(request.form, 'player7'):
        team.player7, team.player7_id = request.form['player7'], request.form['player7_id']
        query = Teams.query.filter_by(player7_id=team.player7_id).first()
        if query:
            return render_template('response.html', message=f'Player with ID "{team.player7_id}" is already registered '
                                                            f'in the Team {query.name}')
        count += 1
    team.receipt = request.form['receipt']
    team.players = count
    try:
        db.session.add(team)
        db.session.commit()
    except Exception:
        message = f'Error in registaring the Team "{team_name}". Please try again sometime.'
    else:
        if team.name:
            MailClient.send_registration_cofirmation(email, team_name)
            message = f'Team "{team_name}" registered successfully'
        else:
            message = f'Error in registaring the Team "{team_name}". Please try again sometime.'
    return render_template('response.html', message=message)


if __name__ == '__main__':
    app.run()
