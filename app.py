from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="HaQOgK3vKr",
    password="HitYdCPu8c",
    hostname="remotemysql.com",
    databasename="HaQOgK3vKr",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
        return f"Name: {self.name} " \
               f"Player1: {self.player1} " \
               f"Player2: {self.player2} " \
               f"Player3: {self.player3} " \
               f"Player4: {self.player4} " \
               f"Player5: {self.player5} " \
               f"Player6: {self.player6} " \
               f"Player7: {self.player7} "


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    team = Teams()
    count = 5
    team.name = request.form['team_name']
    team.player1 = request.form['player1']
    team.player2 = request.form['player2']
    team.player3 = request.form['player3']
    team.player4 = request.form['player4']
    team.player5 = request.form['player5']
    if hasattr(request.form, 'player6'):
        team.player6 = request.form['player6']
        count += 1
    else:
        team.player6 = "-"
    if hasattr(request.form, 'player7'):
        team.player7 = request.form['player7']
        count += 1
    else:
        team.player7 = "-"
    team.receipt = request.form['receipt']
    team.players = count
    db.session.add(team)
    db.session.commit()
    if team.name:

        return "Team Registered Successfully"
    else:
        return "Error in registring the team. Try again"


if __name__ == '__main__':
    app.run()