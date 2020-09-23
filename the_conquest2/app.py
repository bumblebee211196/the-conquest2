from flask import render_template, request

from the_conquest2 import app, Teams
from the_conquest2.database import validate_and_commit_data, query_team


# CORE functionalities

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/registered_teams', methods=['GET'])
def show_teams():
    _teams = Teams.query.all()
    teams = []
    for team in _teams:
        if team.status == 'verified':
            teams.append({
                'name': team.name,
                'roster': [team.player1, team.player2, team.player3, team.player4, team.player5, team.player6,
                           team.player7]
            })
    return render_template('regsitered_teams.html', teams=teams)


@app.route('/submit', methods=['POST'])
def submit_form():
    return validate_and_commit_data(request)


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
