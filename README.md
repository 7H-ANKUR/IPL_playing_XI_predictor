🏏 IPL Playing XI Predictor (Strategy-Aware)
============================================

A **strategy-aware IPL Playing XI prediction engine** built using **Python, Pandas, SQLite, and Streamlit**.

The system generates a **cricket-realistic Playing XI** for any IPL team based on **Aggressive, Balanced, or Defensive** strategies, while strictly enforcing official IPL-style constraints.

This project is designed for **hackathons, analytics demos, and learning constraint-based team selection systems**.

🚀 Features
-----------

### ✅ Hard IPL Constraints (Always Enforced)

- **Exactly 11 players** in the Playing XI.
- **Exactly 4 overseas players** (Maximum).
- **At least 3 pure bowlers** (Based on CSV role text, not assumptions).
- **At least 1 wicketkeeper**.
- **Impact Player is never a wicketkeeper.**

### 🧠 Strategy-Aware Selection

- **Aggressive**: Prefers batters with high strike rates; bowling is respected but secondary.
- **Balanced**: Maintains a balanced weighting between batting and bowling metrics.
- **Defensive**: Prioritizes reliable batters (high average) and bowlers with strong economy rates.

### 🎳 Cricket-Correct Bowler Detection

- Bowlers are detected using **actual role values from the CSV**.
- Keywords detected: `Bowler`, `Fast`, `Pace`, `Medium`, `Spin`, `Spinner`, `Leg Break`, `Off Break`, `Orthodox`, `Left Arm`, `Right Arm`.
- Bowling statistics are used **only for ranking**, not for classification.
- All-rounders are explicitly excluded from the **pure bowler** count to ensure bowling depth.

### 🖥️ Interactive UI (Streamlit)

- Team selection dropdown.
- Strategy toggle (Aggressive / Balanced / Defensive).
- Formatted Playing XI table.
- Impact Player recommendation display.


📊 Dataset Description
----------------------

### 1. player_name_cleaned_fixed.csv

Contains squad-level information:

- `Player_Name` – Name of the athlete
- `Team` – Current IPL franchise
- `Nationality` – India / Overseas
- `Primary_Role` – Bowler, Batter, All-Rounder, Wicketkeeper

### 2. stats_corrected.csv

Contains historical IPL statistics (2008–2025):

- `Batting_SR`, `Batting_Avg`
- `Bowling_Econ`, `Bowling_SR`
- `Balls_Faced` (used for sample-size stability)

> ⚠️ **WARNING**  
> IPL 2026 data is intentionally excluded.  
> All statistics represent historical IPL performance only.

🧠 Core Logic Overview
----------------------

### Pure Bowler Detection (Critical Design)

A player is considered a **pure bowler** if their role text indicates bowling but does **not** include `"All-Rounder"`.  
This avoids false negatives caused by IPL-era statistical variance.

### 🧩 Playing XI Selection Logic

The engine builds the team in a **strict, constraint-first order** to prevent invalid squads:

1. **Select 3 best pure bowlers** (ensures minimum bowling requirement).
2. **Select 4 overseas players** (fills the quota with highest-ranked internationals).
3. **Select 1 wicketkeeper** (if not already selected).
4. **Fill remaining slots** using strategy-based scores.
5. **Final validation**: ensure exactly 11 players.

⚙️ How to Run Locally
---------------------

### 🔧 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### 📦 Install Dependencies

```bash
pip install streamlit pandas numpy
🔮 Future Enhancements
----------------------

*   🏟️ **Venue-based Playing XI** – Pitch-specific adjustments (Spin vs Pace)
    
*   💀 **Death-over specialist selection** – Overs 16–20 weighting
    
*   ⚔️ **Match-up based logic** – Opposition-aware selection
    
*   💡 **Explainability** – “Why this player was picked”
    

📜 Disclaimer
-------------

This project is built for **educational, analytical, and hackathon purposes only**.It does **not** represent official IPL team selection decisions.

🙌 Author
---------

Built with ❤️ by **Ankur Pratap Singh**_Using Python, Pandas, SQLite, and Streamlit_

 If you want next, I can:  - Add **GitHub badges**  - Create a **LICENSE**  - Write **CONTRIBUTING.md**  - Add a **demo GIF / screenshots section**  Just tell me 👍   `

