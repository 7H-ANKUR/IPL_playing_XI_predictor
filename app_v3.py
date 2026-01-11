import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import os

DB_PATH = "ipl_predictor.db"

# ======================================================
# ROLE HELPERS (FINAL & VERIFIED)
# ======================================================
def is_wicketkeeper(role):
    if pd.isna(role):
        return False
    role = str(role).lower()
    return "wicketkeeper" in role


def is_pure_bowler_row(row):
    """
    Detect PURE bowlers using CSV role text only.
    Verified against your dataset.
    """
    role = str(row["Primary_Role"]).strip().lower()

    # Exclude all-rounders
    if "all-rounder" in role:
        return False

    role_keywords = [
        "bowler",
        "fast",
        "pace",
        "medium",
        "spin",
        "spinner",
        "leg break",
        "off break",
        "orthodox",
        "left arm",
        "right arm",
    ]

    return any(k in role for k in role_keywords)


# ======================================================
# DATABASE INITIALIZATION
# ======================================================
def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    squads = pd.read_csv("player_name_cleaned_fixed.csv")
    stats = pd.read_csv("stats_corrected.csv")

    squads["Player_Name"] = squads["Player_Name"].str.strip()
    stats["Player_Name"] = stats["Player_Name"].str.strip()

    stats = stats.sort_values("Balls_Faced", ascending=False).drop_duplicates("Player_Name")
    df = squads.merge(stats, on="Player_Name", how="left")

    med = stats.median(numeric_only=True)
    for c in ["Batting_SR", "Batting_Avg", "Bowling_Econ", "Bowling_SR", "Balls_Faced"]:
        df[c] = df[c].fillna(med[c])

    df["Experience_Score"] = np.log1p(df["Balls_Faced"])

    df.to_sql("players", sqlite3.connect(DB_PATH), if_exists="replace", index=False)


# ======================================================
# PLAYING XI ENGINE (CONSTRAINT-FIRST)
# ======================================================
def select_playing_xi(team, strategy):
    df = pd.read_sql(
        f"SELECT * FROM players WHERE Team = '{team}'",
        sqlite3.connect(DB_PATH)
    )

    # -------------------------
    # BASIC SCORES
    # -------------------------
    df["Bat_Score"] = df["Batting_SR"] * 0.6 + df["Batting_Avg"] * 0.4
    df["Bowl_Score"] = (1 / df["Bowling_Econ"]) * 0.6 + (1 / df["Bowling_SR"]) * 0.4

    if strategy == "Aggressive":
        df["Final_Score"] = df["Bat_Score"] * 0.7 + df["Bowl_Score"] * 0.2
    elif strategy == "Defensive":
        df["Final_Score"] = df["Batting_Avg"] * 0.6 + df["Bowl_Score"] * 0.3
    else:
        df["Final_Score"] = df["Bat_Score"] * 0.5 + df["Bowl_Score"] * 0.3

    # -------------------------
    # 1️⃣ SELECT 3 PURE BOWLERS
    # -------------------------
    bowlers = df[df.apply(is_pure_bowler_row, axis=1)] \
        .sort_values("Bowl_Score", ascending=False) \
        .head(3)

    # -------------------------
    # 2️⃣ SELECT 4 OVERSEAS
    # -------------------------
    overseas = df[
        (df["Nationality"] != "India") &
        (~df["Player_Name"].isin(bowlers["Player_Name"]))
    ].sort_values("Final_Score", ascending=False).head(4)

    # -------------------------
    # 3️⃣ SELECT WICKETKEEPER
    # -------------------------
    selected = pd.concat([bowlers, overseas]).drop_duplicates("Player_Name")

    keeper = df[
        df["Primary_Role"].apply(is_wicketkeeper) &
        (~df["Player_Name"].isin(selected["Player_Name"]))
    ].sort_values("Final_Score", ascending=False).head(1)

    selected = pd.concat([selected, keeper]).drop_duplicates("Player_Name")

    # -------------------------
    # 4️⃣ FILL REMAINING SLOTS
    # -------------------------
    remaining = 11 - len(selected)

    fillers = df[
        ~df["Player_Name"].isin(selected["Player_Name"])
    ].sort_values("Final_Score", ascending=False).head(remaining)

    xi = pd.concat([selected, fillers]).drop_duplicates("Player_Name").head(11)

    # -------------------------
    # IMPACT PLAYER (NON-WK)
    # -------------------------
    impact = df[
        (~df["Player_Name"].isin(xi["Player_Name"])) &
        (~df["Primary_Role"].apply(is_wicketkeeper))
    ].sort_values("Final_Score", ascending=False).head(1)

    return xi.reset_index(drop=True), impact


# ======================================================
# STREAMLIT UI
# ======================================================
st.set_page_config("IPL Playing XI Predictor", "🏏", layout="wide")

if not os.path.exists(DB_PATH):
    init_db()

st.title("🏏 IPL Playing XI Predictor")

with st.sidebar:
    teams = pd.read_sql(
        "SELECT DISTINCT Team FROM players",
        sqlite3.connect(DB_PATH)
    )["Team"].tolist()

    team = st.selectbox("Select Team", teams)
    strategy = st.select_slider(
        "Playing Style", ["Defensive", "Balanced", "Aggressive"],
        value="Balanced"
    )

if st.button("🚀 Generate Playing XI"):
    xi, impact = select_playing_xi(team, strategy)

    st.subheader(f"{team} – {strategy} Playing XI")
    st.table(xi[
        [
            "Player_Name", "Nationality", "Primary_Role",
            "Batting_SR", "Batting_Avg",
            "Bowling_Econ", "Bowling_SR"
        ]
    ])

    if not impact.empty:
        st.success(
            f"Impact Player: {impact.iloc[0]['Player_Name']} ({impact.iloc[0]['Primary_Role']})"
        )
