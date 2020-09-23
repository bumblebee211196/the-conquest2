import shortuuid
from flask import render_template

from the_conquest2 import db, Teams
from the_conquest2.mail_client import MailClient


def query_team(**kwargs):
    return Teams.query.filter_by(**kwargs).first()


def validate_playerids(player_ids):
    _player_ids = [player_ids[0]]
    for i in range(1, len(player_ids)):
        if player_ids[i] in _player_ids:
            return False, _player_ids[i]
    return True,


def validate_and_commit_data(request):
    team = Teams()
    count, title = 5, 'Oops!'

    team.reg_id = team_reg_id = shortuuid.uuid()
    team.name = team_name = request.form['team_name']
    team.email = email = request.form['email']
    team.mobile = request.form['mobile']
    team.receipt = request.form['receipt']
    team.status = 'not_verified'

    team.player1, team.player1_id = request.form['player1'], request.form['player1_id']
    team.player2, team.player2_id = request.form['player2'], request.form['player2_id']
    team.player3, team.player3_id = request.form['player3'], request.form['player3_id']
    team.player4, team.player4_id = request.form['player4'], request.form['player4_id']
    team.player5, team.player5_id = request.form['player5'], request.form['player5_id']
    player_ids = [team.player1_id, team.player2_id, team.player3_id, team.player4_id, team.player5_id]
    if hasattr(request.form, 'player6'):
        team.player6, team.player6_id = request.form['player6'], request.form['player6_id']
        player_ids.append(team.player6_id)
        count += 1
    if hasattr(request.form, 'player7'):
        team.player7, team.player7_id = request.form['player7'], request.form['player7_id']
        player_ids.append(team.player7_id)
        count += 1
    team.players = count

    status, message = validate_playerids(player_ids)
    if not status:
        return render_template('response.html', title=title,
                               message=f'More than one player has the same Steam Friend ID {message}', )

    # Check name
    query = Teams.query.filter_by(name=team_name).first()
    if query:
        return render_template('response.html', title=title,
                               message=f'Team "{team_name}" is already registered. Try using other names(s).')
    # Check email
    query = query_team(email=email)
    if query:
        return render_template('response.html', title=title,
                               message=f'Email "{email}" is already registered. Try using another email.')
    # Check mobile
    query = query_team(mobile=team.mobile)
    if query:
        return render_template('response.html', title=title,
                               message=f'Mobile number "{team.mobile}" is already registered. '
                                       f'Try using another number.')
    # Check player1
    query = query_team(player1_id=team.player1_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player1_id}" is already registered in the Team '
                                       f'{query.name}')
    # Check player2
    query = query_team(player2_id=team.player2_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player2_id}" is already registered in the Team '
                                       f'{query.name}')
    # Check player3
    query = query_team(player3_id=team.player3_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player3_id}" is already registered in the Team '
                                       f'{query.name}')
    # Check player4
    query = query_team(player4_id=team.player4_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player4_id}" is already registered in the Team '
                                       f'{query.name}')
    # Check player5
    query = query_team(player5_id=team.player5_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player5_id}" is already registered in the Team '
                                       f'{query.name}')
    # Check player6
    query = query_team(player6_id=team.player6_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player6_id}" is already registered in the Team '
                                       f'{query.name}')
    # Check player7
    query = query_team(player7_id=team.player7_id)
    if query:
        return render_template('response.html', title=title,
                               message=f'Player with ID "{team.player7_id}" is already registered in the Team '
                                       f'{query.name}')

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
            title = 'Registration Successfull!'
            message = f'Team "{team_name}" has been registered successfully. Your team\'s registration ID is ' \
                      f'{team_reg_id}. Kindly save this and use it to check the registration status of your team.'
        else:
            message = f'Error in registaring the Team "{team_name}". Please try again sometime.'
    return render_template('response.html', title=title, message=message)
