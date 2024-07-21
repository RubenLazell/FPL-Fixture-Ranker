from flask import Flask, request, render_template, send_file, session, redirect, url_for
import csv
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def mean(lst): 
    return sum(lst) / len(lst)

def converter(lst):
    return list(map(float, lst))

# Fixtures for the first five gameweeks
fixtures = {
    'GW1': {
        'Arsenal': {'opponent': 'Wolves', 'location': 'home', 'datetime': 'Aug 17, 10:00 AM'},
        'Aston Villa': {'opponent': 'West Ham', 'location': 'away', 'datetime': 'Aug 17, 12:30 PM'},
        'Bournemouth': {'opponent': 'Nottingham Forest', 'location': 'away', 'datetime': 'Aug 17, 10:00 AM'},
        'Brentford': {'opponent': 'Crystal Palace', 'location': 'home', 'datetime': 'Aug 18, 9:00 AM'},
        'Brighton': {'opponent': 'Everton', 'location': 'away', 'datetime': 'Aug 17, 10:00 AM'},
        'Chelsea': {'opponent': 'Man City', 'location': 'home', 'datetime': 'Aug 18, 11:30 AM'},
        'Crystal Palace': {'opponent': 'Brentford', 'location': 'away', 'datetime': 'Aug 18, 9:00 AM'},
        'Everton': {'opponent': 'Brighton', 'location': 'home', 'datetime': 'Aug 17, 10:00 AM'},
        'Fulham': {'opponent': 'Man United', 'location': 'away', 'datetime': 'Aug 16, 3:00 PM'},
        'Ipswich Town': {'opponent': 'Liverpool', 'location': 'home', 'datetime': 'Aug 17, 7:30 AM'},
        'Leicester City': {'opponent': 'Tottenham', 'location': 'home', 'datetime': 'Aug 19, 3:00 PM'},
        'Liverpool': {'opponent': 'Ipswich Town', 'location': 'away', 'datetime': 'Aug 17, 7:30 AM'},
        'Man City': {'opponent': 'Chelsea', 'location': 'away', 'datetime': 'Aug 18, 11:30 AM'},
        'Man United': {'opponent': 'Fulham', 'location': 'home', 'datetime': 'Aug 16, 3:00 PM'},
        'Newcastle': {'opponent': 'Southampton', 'location': 'home', 'datetime': 'Aug 17, 10:00 AM'},
        'Nottingham Forest': {'opponent': 'Bournemouth', 'location': 'home', 'datetime': 'Aug 17, 10:00 AM'},
        'Southampton': {'opponent': 'Newcastle', 'location': 'away', 'datetime': 'Aug 17, 10:00 AM'},
        'Tottenham': {'opponent': 'Leicester City', 'location': 'away', 'datetime': 'Aug 19, 3:00 PM'},
        'West Ham': {'opponent': 'Aston Villa', 'location': 'home', 'datetime': 'Aug 17, 12:30 PM'},
        'Wolves': {'opponent': 'Arsenal', 'location': 'away', 'datetime': 'Aug 17, 10:00 AM'}
    },
    'GW2': {
        'Arsenal': {'opponent': 'Aston Villa', 'location': 'away', 'datetime': 'Aug 24, 12:30 PM'},
        'Aston Villa': {'opponent': 'Arsenal', 'location': 'home', 'datetime': 'Aug 24, 12:30 PM'},
        'Bournemouth': {'opponent': 'Newcastle', 'location': 'home', 'datetime': 'Aug 25, 9:00 AM'},
        'Brentford': {'opponent': 'Liverpool', 'location': 'away', 'datetime': 'Aug 25, 11:30 AM'},
        'Brighton': {'opponent': 'Man United', 'location': 'home', 'datetime': 'Aug 24, 7:30 AM'},
        'Chelsea': {'opponent': 'Wolves', 'location': 'away', 'datetime': 'Aug 25, 9:00 AM'},
        'Crystal Palace': {'opponent': 'West Ham', 'location': 'home', 'datetime': 'Aug 24, 10:00 AM'},
        'Everton': {'opponent': 'Tottenham', 'location': 'away', 'datetime': 'Aug 24, 10:00 AM'},
        'Fulham': {'opponent': 'Leicester City', 'location': 'home', 'datetime': 'Aug 24, 10:00 AM'},
        'Ipswich Town': {'opponent': 'Man City', 'location': 'away', 'datetime': 'Aug 24, 10:00 AM'},
        'Leicester City': {'opponent': 'Fulham', 'location': 'away', 'datetime': 'Aug 24, 10:00 AM'},
        'Liverpool': {'opponent': 'Brentford', 'location': 'home', 'datetime': 'Aug 25, 11:30 AM'},
        'Man City': {'opponent': 'Ipswich Town', 'location': 'home', 'datetime': 'Aug 24, 10:00 AM'},
        'Man United': {'opponent': 'Brighton', 'location': 'away', 'datetime': 'Aug 24, 7:30 AM'},
        'Newcastle': {'opponent': 'Bournemouth', 'location': 'away', 'datetime': 'Aug 25, 9:00 AM'},
        'Nottingham Forest': {'opponent': 'Southampton', 'location': 'away', 'datetime': 'Aug 24, 10:00 AM'},
        'Southampton': {'opponent': 'Nottingham Forest', 'location': 'home', 'datetime': 'Aug 24, 10:00 AM'},
        'Tottenham': {'opponent': 'Everton', 'location': 'home', 'datetime': 'Aug 24, 10:00 AM'},
        'West Ham': {'opponent': 'Crystal Palace', 'location': 'away', 'datetime': 'Aug 24, 10:00 AM'},
        'Wolves': {'opponent': 'Chelsea', 'location': 'home', 'datetime': 'Aug 25, 9:00 AM'}
    },
    'GW3': {
        'Arsenal': {'opponent': 'Brighton', 'location': 'home', 'datetime': 'Aug 31, 7:30 AM'},
        'Aston Villa': {'opponent': 'Leicester City', 'location': 'away', 'datetime': 'Aug 31, 10:00 AM'},
        'Bournemouth': {'opponent': 'Everton', 'location': 'away', 'datetime': 'Aug 31, 10:00 AM'},
        'Brentford': {'opponent': 'Southampton', 'location': 'home', 'datetime': 'Aug 31, 10:00 AM'},
        'Brighton': {'opponent': 'Arsenal', 'location': 'away', 'datetime': 'Aug 31, 7:30 AM'},
        'Chelsea': {'opponent': 'Crystal Palace', 'location': 'home', 'datetime': 'Sep 1, 8:30 AM'},
        'Crystal Palace': {'opponent': 'Chelsea', 'location': 'away', 'datetime': 'Sep 1, 8:30 AM'},
        'Everton': {'opponent': 'Bournemouth', 'location': 'home', 'datetime': 'Aug 31, 10:00 AM'},
        'Fulham': {'opponent': 'Ipswich Town', 'location': 'away', 'datetime': 'Aug 31, 10:00 AM'},
        'Ipswich Town': {'opponent': 'Fulham', 'location': 'home', 'datetime': 'Aug 31, 10:00 AM'},
        'Leicester City': {'opponent': 'Aston Villa', 'location': 'home', 'datetime': 'Aug 31, 10:00 AM'},
        'Liverpool': {'opponent': 'Man United', 'location': 'away', 'datetime': 'Sep 1, 11:00 AM'},
        'Man City': {'opponent': 'West Ham', 'location': 'away', 'datetime': 'Aug 31, 12:30 PM'},
        'Man United': {'opponent': 'Liverpool', 'location': 'home', 'datetime': 'Sep 1, 11:00 AM'},
        'Newcastle': {'opponent': 'Tottenham', 'location': 'home', 'datetime': 'Sep 1, 8:30 AM'},
        'Nottingham Forest': {'opponent': 'Wolves', 'location': 'home', 'datetime': 'Aug 31, 10:00 AM'},
        'Southampton': {'opponent': 'Brentford', 'location': 'away', 'datetime': 'Aug 31, 10:00 AM'},
        'Tottenham': {'opponent': 'Newcastle', 'location': 'away', 'datetime': 'Sep 1, 8:30 AM'},
        'West Ham': {'opponent': 'Man City', 'location': 'home', 'datetime': 'Aug 31, 12:30 PM'},
        'Wolves': {'opponent': 'Nottingham Forest', 'location': 'away', 'datetime': 'Aug 31, 10:00 AM'}
    },
    'GW4': {
        'Arsenal': {'opponent': 'Tottenham', 'location': 'away', 'datetime': 'Sep 15, 9:00 AM'},
        'Aston Villa': {'opponent': 'Everton', 'location': 'home', 'datetime': 'Sep 14, 12:30 PM'},
        'Bournemouth': {'opponent': 'Chelsea', 'location': 'home', 'datetime': 'Sep 14, 3:00 PM'},
        'Brentford': {'opponent': 'Man City', 'location': 'away', 'datetime': 'Sep 14, 10:00 AM'},
        'Brighton': {'opponent': 'Ipswich Town', 'location': 'home', 'datetime': 'Sep 14, 10:00 AM'},
        'Chelsea': {'opponent': 'Bournemouth', 'location': 'away', 'datetime': 'Sep 14, 3:00 PM'},
        'Crystal Palace': {'opponent': 'Leicester City', 'location': 'home', 'datetime': 'Sep 14, 10:00 AM'},
        'Everton': {'opponent': 'Aston Villa', 'location': 'away', 'datetime': 'Sep 14, 12:30 PM'},
        'Fulham': {'opponent': 'West Ham', 'location': 'home', 'datetime': 'Sep 14, 10:00 AM'},
        'Ipswich Town': {'opponent': 'Brighton', 'location': 'away', 'datetime': 'Sep 14, 10:00 AM'},
        'Leicester City': {'opponent': 'Crystal Palace', 'location': 'away', 'datetime': 'Sep 14, 10:00 AM'},
        'Liverpool': {'opponent': 'Nottingham Forest', 'location': 'home', 'datetime': 'Sep 14, 10:00 AM'},
        'Man City': {'opponent': 'Brentford', 'location': 'home', 'datetime': 'Sep 14, 10:00 AM'},
        'Man United': {'opponent': 'Southampton', 'location': 'away', 'datetime': 'Sep 14, 7:30 AM'},
        'Newcastle': {'opponent': 'Wolves', 'location': 'away', 'datetime': 'Sep 15, 11:30 AM'},
        'Nottingham Forest': {'opponent': 'Liverpool', 'location': 'away', 'datetime': 'Sep 14, 10:00 AM'},
        'Southampton': {'opponent': 'Man United', 'location': 'home', 'datetime': 'Sep 14, 7:30 AM'},
        'Tottenham': {'opponent': 'Arsenal', 'location': 'home', 'datetime': 'Sep 15, 9:00 AM'},
        'West Ham': {'opponent': 'Fulham', 'location': 'away', 'datetime': 'Sep 14, 10:00 AM'},
        'Wolves': {'opponent': 'Newcastle', 'location': 'home', 'datetime': 'Sep 15, 11:30 AM'}
    },
    'GW5': {
        'Arsenal': {'opponent': 'Man City', 'location': 'away', 'datetime': 'Sep 22, 11:30 AM'},
        'Aston Villa': {'opponent': 'Wolves', 'location': 'home', 'datetime': 'Sep 21, 10:00 AM'},
        'Bournemouth': {'opponent': 'Liverpool', 'location': 'away', 'datetime': 'Sep 21, 10:00 AM'},
        'Brentford': {'opponent': 'Tottenham', 'location': 'away', 'datetime': 'Sep 21, 10:00 AM'},
        'Brighton': {'opponent': 'Nottingham Forest', 'location': 'home', 'datetime': 'Sep 22, 9:00 AM'},
        'Chelsea': {'opponent': 'West Ham', 'location': 'away', 'datetime': 'Sep 21, 7:30 AM'},
        'Crystal Palace': {'opponent': 'Man United', 'location': 'home', 'datetime': 'Sep 21, 12:30 PM'},
        'Everton': {'opponent': 'Leicester City', 'location': 'away', 'datetime': 'Sep 21, 10:00 AM'},
        'Fulham': {'opponent': 'Newcastle', 'location': 'home', 'datetime': 'Sep 21, 10:00 AM'},
        'Ipswich Town': {'opponent': 'Southampton', 'location': 'away', 'datetime': 'Sep 21, 10:00 AM'},
        'Leicester City': {'opponent': 'Everton', 'location': 'home', 'datetime': 'Sep 21, 10:00 AM'},
        'Liverpool': {'opponent': 'Bournemouth', 'location': 'home', 'datetime': 'Sep 21, 10:00 AM'},
        'Man City': {'opponent': 'Arsenal', 'location': 'home', 'datetime': 'Sep 22, 11:30 AM'},
        'Man United': {'opponent': 'Crystal Palace', 'location': 'away', 'datetime': 'Sep 21, 12:30 PM'},
        'Newcastle': {'opponent': 'Fulham', 'location': 'away', 'datetime': 'Sep 21, 10:00 AM'},
        'Nottingham Forest': {'opponent': 'Brighton', 'location': 'away', 'datetime': 'Sep 22, 9:00 AM'},
        'Southampton': {'opponent': 'Ipswich Town', 'location': 'home', 'datetime': 'Sep 21, 10:00 AM'},
        'Tottenham': {'opponent': 'Brentford', 'location': 'home', 'datetime': 'Sep 21, 10:00 AM'},
        'West Ham': {'opponent': 'Chelsea', 'location': 'home', 'datetime': 'Sep 21, 7:30 AM'},
        'Wolves': {'opponent': 'Aston Villa', 'location': 'away', 'datetime': 'Sep 21, 10:00 AM'}
    }
}

@app.route('/')
def index():
    selected_gw = session.get('selected_gw', 'GW1')
    rankings = session.get('rankings', {})
    return render_template('index.html', fixtures=fixtures[selected_gw], selected_gw=selected_gw, rankings=rankings.get(selected_gw, {}))

@app.route('/select_gameweek', methods=['POST'])
def select_gameweek():
    # Save current rankings
    current_gw = session.get('selected_gw', 'GW1')
    if 'rankings' not in session:
        session['rankings'] = {}
    if current_gw not in session['rankings']:
        session['rankings'][current_gw] = {}

    for team in fixtures[current_gw].keys():
        session['rankings'][current_gw][team] = {
            'attack': request.form.get(f'{team}_attack', session['rankings'][current_gw].get(team, {}).get('attack', '')),
            'defense': request.form.get(f'{team}_defense', session['rankings'][current_gw].get(team, {}).get('defense', ''))
        }

    selected_gw = request.form['gameweek']
    session['selected_gw'] = selected_gw

    return render_template('index.html', fixtures=fixtures[selected_gw], selected_gw=selected_gw, rankings=session['rankings'].get(selected_gw, {}))

@app.route('/save_gameweek', methods=['POST'])
def save_gameweek():
    current_gw = request.form['gameweek']
    if 'rankings' not in session:
        session['rankings'] = {}
    if current_gw not in session['rankings']:
        session['rankings'][current_gw] = {}

    for team in fixtures[current_gw].keys():
        session['rankings'][current_gw][team] = {
            'attack': request.form[f'{team}_attack'],
            'defense': request.form[f'{team}_defense']
        }

    session['rankings'][current_gw] = session['rankings'][current_gw]
    return redirect(url_for('index'))

@app.route('/submit_rankings', methods=['POST'])
def submit_rankings():
    rankings = session.get('rankings', {})
    all_teams = list(fixtures['GW1'].keys())

    attack_ratings = []
    defense_ratings = []

    for gw in ['GW1', 'GW2', 'GW3', 'GW4', 'GW5']:
        gw_attack = [session['rankings'].get(gw, {}).get(team, {}).get('attack', '') for team in all_teams]
        gw_defense = [session['rankings'].get(gw, {}).get(team, {}).get('defense', '') for team in all_teams]
        attack_ratings.append(gw_attack)
        defense_ratings.append(gw_defense)

    csv_filename = 'user_rankings.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(all_teams)
        for row in attack_ratings:
            writer.writerow(row)
        for row in defense_ratings:
            writer.writerow(row)

    session['graphs_generated'] = True
    generate_graphs(csv_filename)

    return redirect(url_for('display_graphs'))

def generate_graphs(filepath):
    # Generate graphs based on the CSV file
    teams = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Chelsea', 
             'Crystal Palace', 'Everton', 'Fulham', 'Ipswich Town', 'Leicester City', 
             'Liverpool', 'Man City', 'Man United', 'Newcastle', 'Nottingham Forest', 
             'Southampton', 'Tottenham', 'West Ham', 'Wolves']
    
    data = {team: [] for team in teams}
    
    with open(filepath, 'r') as filename:
        file = csv.DictReader(filename)
        for col in file:
            for team in teams:
                if team in col:
                    data[team].append(col[team])

    att_averages_list = []
    def_averages_list = []
    for team in teams:
        team_data = data[team]
        while '' in team_data:
            team_data.remove('')
        att_list = converter(team_data[:len(team_data)//2])
        def_list = converter(team_data[len(team_data)//2:])
        att_averages_list.append(mean(att_list))
        def_averages_list.append(mean(def_list))

    with open(filepath, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            headers = row
            break

    att_dict = dict(zip(headers, att_averages_list))
    def_dict = dict(zip(headers, def_averages_list))

    sorted_att_dict = sorted(att_dict.items(), key=lambda x: x[1])
    sorted_def_dict = sorted(def_dict.items(), key=lambda x: x[1])

    sorted_att_dict = dict(sorted_att_dict)
    sorted_def_dict = dict(sorted_def_dict)

    # Abbreviations for the teams
    team_abbreviations = {
        'Arsenal': 'ARS', 'Aston Villa': 'AVL', 'Bournemouth': 'BOU', 'Brentford': 'BRE',
        'Brighton': 'BHA', 'Chelsea': 'CHE', 'Crystal Palace': 'CRY', 'Everton': 'EVE',
        'Fulham': 'FUL', 'Ipswich Town': 'IPS', 'Leicester City': 'LEI', 'Liverpool': 'LIV',
        'Man City': 'MCI', 'Man United': 'MUN', 'Newcastle': 'NEW', 'Nottingham Forest': 'NFO',
        'Southampton': 'SOU', 'Tottenham': 'TOT', 'West Ham': 'WHU', 'Wolves': 'WOL'
    }

    # Custom colormap from green to orange to red
    colors = [(0, 'green'), (0.5, 'orange'), (1, 'red')]
    n_bins = 100  # Discretizes the interpolation into bins
    cmap_name = 'green_orange_red'
    cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

    # Plotting Attacking Fixture Difficulty
    names_att = [team_abbreviations[name] for name in list(sorted_att_dict.keys())]
    values_att = list(sorted_att_dict.values())

    norm = mcolors.Normalize(vmin=min(values_att), vmax=max(values_att))
    colors = cmap(norm(values_att))

    plt.rcParams.update({'font.size': 6.5})
    plt.bar(range(len(att_dict)), values_att, tick_label=names_att, color=colors)
    plt.xlabel("Premier League Teams")
    plt.ylabel("Attacking Fixture Difficulty rating (Low = High Attacking Threat)")
    plt.title("Attacking Fixture Difficulty Rating For FPL 2024/25")
    plt.savefig('static/attacking_difficulty.png')
    plt.clf()  # Clear the current figure

    # Plotting Defensive Fixture Difficulty
    names_def = [team_abbreviations[name] for name in list(sorted_def_dict.keys())]
    values_def = list(sorted_def_dict.values())

    norm = mcolors.Normalize(vmin=min(values_def), vmax=max(values_def))
    colors = cmap(norm(values_def))

    plt.rcParams.update({'font.size': 6.5})
    plt.bar(range(len(def_dict)), values_def, tick_label=names_def, color=colors)
    plt.xlabel("Premier League Teams")
    plt.ylabel("Defensive Fixture Difficulty rating (Low = High Defensive Rating)")
    plt.title("Defensive Fixture Difficulty Rating For FPL 2024/25")
    plt.savefig('static/defensive_difficulty.png')
    plt.clf()  # Clear the current figure

@app.route('/graphs')
def display_graphs():
    if not session.get('graphs_generated', False):
        return redirect(url_for('index'))
    return render_template('graphs.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)