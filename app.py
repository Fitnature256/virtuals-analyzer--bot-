import streamlit as st
import pandas as pd

st.set_page_config(page_title="Virtuals Smart Bet Selector", layout="centered")
st.title("🧮 Virtuals Smart Bet Selector")
st.write("Upload your virtual results CSV to simulate smart bet suggestions.")

uploaded_file = st.file_uploader("Upload Match Results CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Preprocessing
    df['total_goals'] = df['home_goals'] + df['away_goals']
    df['goal_margin'] = abs(df['home_goals'] - df['away_goals'])

    # Team-wise goal averages
    home_avg = df.groupby('home_team')['home_goals'].mean()
    away_avg = df.groupby('away_team')['away_goals'].mean()

    st.subheader("📊 Team Goal Averages")
    st.write("Home Teams", home_avg)
    st.write("Away Teams", away_avg)

    # Match-by-match simulated logic
    st.subheader("🧳 Smart Bet Suggestions")
    suggestions = []
    for idx, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']
        hg = home_avg.get(home, 0)
        ag = away_avg.get(away, 0)

        if hg > 2.2 and ag < 1.2:
            pick = "Home Win"
        elif ag > 2.2 and hg < 1.2:
            pick = "Away Win"
        elif abs(hg - ag) < 0.3 and hg < 1.5:
            pick = "Draw"
        else:
            pick = "Avoid"

        suggestions.append({
            "Match": f"{home} vs {away}",
            "Suggested Pick": pick,
            "Home Avg": round(hg, 2),
            "Away Avg": round(ag, 2)
        })

    st.dataframe(pd.DataFrame(suggestions))

    st.info("These suggestions are based on statistical heuristics only. This does not guarantee outcomes.")
else:
    st.warning("Please upload a CSV with columns: home_team, away_team, home_goals, away_goals")
