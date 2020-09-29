import shortuuid
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from database import make_db_connection
from mail_client import MailClient

app = Flask(__name__)
make_db_connection(app)
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
    player1_id = db.Column(db.BIGINT)
    player2_id = db.Column(db.BIGINT)
    player3_id = db.Column(db.BIGINT)
    player4_id = db.Column(db.BIGINT)
    player5_id = db.Column(db.BIGINT)
    player6_id = db.Column(db.BIGINT)
    player7_id = db.Column(db.BIGINT)
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


def query_team(**kwargs):
    return Teams.query.filter_by(**kwargs).first()


# CORE functionalities

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/registered_teams', methods=['GET'])
def show_teams():
    _teams = Teams.query.all()
    teams = []
    for team in _teams:
        teams.append({
            'name': team.name,
            'status': team.status,
            'roster': [team.player1, team.player2, team.player3, team.player4, team.player5, team.player6,
                       team.player7]
        })
    return render_template('regsitered_teams.html', teams=teams)


@app.route('/submit', methods=['POST'])
def submit_form():
    team = Teams()
    count, title = 5, 'Oops!'
    team_reg_id = shortuuid.uuid()
    team.reg_id = team_reg_id
    team.name = team_name = request.form['team_name']
    team.mobile = request.form['mobile']
    query = Teams.query.filter_by(name=team_name).first()
    if query:
        return render_template('response.html', title=title,
                               message=f'Team "{team_name}" is already registered. Try using other names(s).')
    team.email = email = request.form['email']
    query = query_team(email=email)
    if query:
        return render_template('response.html', title=title,
                               message=f'Email "{email}" is already registered. Try using another email.')
    team.player1, team.player1_id = request.form['player1'], request.form['player1_id']
    query = query_team(player1_id=team.player1_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player1_id}" is already registered in the Team '
                                       f'{query.name}')
    team.player2, team.player2_id = request.form['player2'], request.form['player2_id']
    query = query_team(player2_id=team.player2_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player2_id}" is already registered in the Team '
                                       f'{query.name}')
    team.player3, team.player3_id = request.form['player3'], request.form['player3_id']
    query = query_team(player3_id=team.player3_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player3_id}" is already registered in the Team '
                                       f'{query.name}')
    team.player4, team.player4_id = request.form['player4'], request.form['player4_id']
    query = query_team(player4_id=team.player4_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player4_id}" is already registered in the Team '
                                       f'{query.name}')
    team.player5, team.player5_id = request.form['player5'], request.form['player5_id']
    query = query_team(player5_id=team.player5_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player5_id}" is already registered in the Team '
                                       f'{query.name}')
    if request.form.get('player6'):
        team.player6, team.player6_id = request.form['player6'], request.form['player6_id']
        query = query_team(player6_id=team.player6_id)
        if query:
            return render_template('response.html', title=title,
                                   message=f'Player with ID "{team.player6_id}" is already registered in the Team '
                                           f'{query.name}')
        count += 1
    if request.form.get('player7'):
        team.player7, team.player7_id = request.form['player7'], request.form['player7_id']
        query = query_team(player7_id=team.player7_id)
        if query:
            return render_template('response.html', title=title,
                                   message=f'Player with ID "{team.player7_id}" is already registered in the Team '
                                           f'{query.name}')
        count += 1
    team.receipt = request.form['receipt']
    team.players = count
    team.status = 'not_verified'
    try:
        db.session.add(team)
        db.session.commit()
    except Exception as ex:
        print(f'Error in registering the team {team_name}')
        print(ex)
        title = 'Oops!'
        message = f'Error in registaring the Team "{team_name}". Please try again sometime.'
    else:
        if team.name:
            MailClient.send_registration_cofirmation(email, team_name, team_reg_id)
            title = 'Registration Successfull'
            message = f'Team "{team_name}" has been registered successfully. Your team\'s registration ID is ' \
                      f'{team_reg_id}. Kindly save this and use it to check the registration status of your team.'
        else:
            message = f'Error in registaring the Team "{team_name}". Please try again sometime.'
    return render_template('response.html', title=title, message=message)


@app.route('/team_status', methods=['GET', 'POST'])
def team_status():
    if request.method == 'GET':
        return render_template('registration_status.html')
    elif request.method == 'POST':
        reg_id = request.form['registration_id']
        team = query_team(reg_id=reg_id)
        if team:
            if team.status == 'verified':
                return render_template('response.html',
                                       title=f'Team Registration Status',
                                       message='Your team\'s payment has been verified. Below is your team details',
                                       team={
                                           'name': team.name,
                                           'roster': [team.player1, team.player2, team.player3, team.player4,
                                                      team.player5, team.player6, team.player7]
                                       })
            elif team.status == 'not_verified':
                return render_template('response.html',
                                       title=f'Team Registration Status',
                                       message='Your team\'s payment confirmation is pending.')
        else:
            return render_template('response.html', title='Oops!', message='No such team found.')


# ERRORs section


@app.errorhandler(404)
def page_not_found(_):
    return render_template('error.html',
                           title='Page Not Found!',
                           message='What you were looking for is just not there.'), 404


@app.errorhandler(500)
def internal_server_error(_):
    return render_template('error.html',
                           title='Oops!',
                           message='There seems to be a problem at our side. We will rectify it. For any other query, '
                                   'kindly contact our support'), 500


if __name__ == '__main__':
    app.run()
