
import pandas as pd

LEADERBOARD_FILE = "leaderboard.csv"

def load_leaderboard():
    try:
        return pd.read_csv(LEADERBOARD_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Score"])

def save_leaderboard(df):
    df.sort_values(by="Score", ascending=False).to_csv(LEADERBOARD_FILE, index=False)
