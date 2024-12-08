
import pandas as pd

# Function to calculate season performance rating
def season_performance(data, team):
    team_data = data[data['team'] == team]
    total_points = (team_data['result'] == 'W').sum() * 3 + (team_data['result'] == 'D').sum()
    total_matches = len(team_data)
    goals_scored = team_data['gf'].sum()
    goals_conceded = team_data['ga'].sum()
    performance_score = total_points / total_matches + (goals_scored - goals_conceded) / total_matches
    return performance_score

# Function to calculate home/away advantage rating
def home_away_rating(data, team, venue):
    venue_data = data[(data['team'] == team) & (data['venue'] == venue)]
    total_points = (venue_data['result'] == 'W').sum() * 3 + (venue_data['result'] == 'D').sum()
    total_matches = len(venue_data)
    if total_matches == 0:
        return 0  # No matches played in the venue
    avg_points = total_points / total_matches
    avg_goals = venue_data['gf'].mean()
    avg_conceded = venue_data['ga'].mean()
    return avg_points + (avg_goals - avg_conceded)

# Function to calculate head-to-head rating
def head_to_head_rating(data, team1, team2):
    h2h_data = data[(data['team'] == team1) & (data['opponent'] == team2)]
    if len(h2h_data) == 0:
        return 0  # No head-to-head data
    total_points = (h2h_data['result'] == 'W').sum() * 3 + (h2h_data['result'] == 'D').sum()
    total_matches = len(h2h_data)
    avg_points = total_points / total_matches
    avg_goals = h2h_data['gf'].mean() - h2h_data['ga'].mean()
    return avg_points + avg_goals

# Function to combine ratings and calculate probabilities
def calculate_probabilities(data, team1, team2):
    # Season performance
    sp1 = season_performance(data, team1)
    sp2 = season_performance(data, team2)

    # Home/away advantage
    ha1 = home_away_rating(data, team1, 'Home')
    ha2 = home_away_rating(data, team2, 'Away')

    # Head-to-head
    h2h1 = head_to_head_rating(data, team1, team2)
    h2h2 = head_to_head_rating(data, team2, team1)

    # Weighted ratings
    score1 = (sp1 + ha1 + h2h1) / 3
    score2 = (sp2 + ha2 + h2h2) / 3

    # Convert scores to probabilities
    total_score = score1 + score2
    prob1 = score1 / total_score if total_score > 0 else 0.5
    prob2 = score2 / total_score if total_score > 0 else 0.5

    return {"team1": team1, "prob1": prob1, "team2": team2, "prob2": prob2}

# Example prediction function
def predict_match(data, team1, team2):
    probabilities = calculate_probabilities(data, team1, team2)
    return probabilities
