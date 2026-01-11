🏏 IPL Playing XI Predictor (Strategy-Aware)
============================================

A **strategy-aware IPL Playing XI prediction engine** built using **Python, Pandas, SQLite, and Streamlit**.

The system generates a **cricket-realistic Playing XI** for any IPL team based on **Aggressive, Balanced, or Defensive** strategies, while strictly enforcing official IPL-style constraints.

This project is designed for **hackathons, analytics demos, and learning constraint-based team selection systems**.

🚀 Features
-----------

### ✅ Hard IPL Constraints (Always Enforced)

*   **Exactly 11 players** in the Playing XI.
    
*   **Exactly 4 overseas players** (Maximum).
    
*   **At least 3 pure bowlers** (Based on CSV role text, not assumptions).
    
*   **At least 1 wicketkeeper**.
    
*   **Impact Player is never a wicketkeeper.**
    

### 🧠 Strategy-Aware Selection

*   **Aggressive**: Prefers batters with high strike rates; bowling is respected but secondary.
    
*   **Balanced**: Maintains a balanced weighting between batting and bowling metrics.
    
*   **Defensive**: Prioritizes reliable batters (high average) and bowlers with strong economy rates.
    

### 🎳 Cricket-Correct Bowler Detection

*   Bowlers are detected using **actual role values from the CSV**.
    
*   Keywords detected: Bowler, Fast, Pace, Medium, Spin, Spinner, Leg Break, Off Break, Orthodox, Left Arm, Right Arm.
    
*   Bowling statistics are used **only for ranking**, not for classification.
    
*   All-rounders are explicitly excluded from the "pure bowler" count to ensure bowling depth.
    

### 🖥️ Interactive UI (Streamlit)

*   Team selection dropdown.
    
*   Strategy toggle (Aggressive/Balanced/Defensive).
    
*   Formatted Playing XI table.
    
*   Impact Player recommendation display.
    

📂 Project Structure
--------------------
   ├── app_final.py                 # Main Streamlit application  ├── player_name_cleaned_fixed.csv # Squad + role + nationality data  ├── stats_corrected.csv          # IPL stats (2008–2025)  ├── ipl_predictor.db             # Auto-generated SQLite database  └── README.md                    # Project documentation   `

📊 Dataset Description
----------------------

### 1\. player\_name\_cleaned\_fixed.csv

Contains squad-level information:

*   Player\_Name: Name of the athlete.
    
*   Team: Current IPL franchise.
    
*   Nationality: India / Overseas.
    
*   Primary\_Role: (Bowler, Batter, All-Rounder, Wicketkeeper).
    

### 2\. stats\_corrected.csv

Contains historical IPL statistics (2008–2025):

*   Batting\_SR / Batting\_Avg
    
*   Bowling\_Econ / Bowling\_SR
    
*   Balls\_Faced (To filter for sample size)
    

> \[!WARNING\]
> 
> IPL 2026 data is intentionally excluded. All statistics represent historical IPL performance only.

🧠 Core Logic Overview
----------------------

### Pure Bowler Detection (Critical Design)

A player is considered a **pure bowler** if their role text indicates bowling but does **not** include "All-Rounder". This avoids false negatives caused by IPL-era data variance.

### 🧩 Playing XI Selection Logic

The engine builds the team in a strict, constraint-first order to prevent invalid squads:

1.  **Select 3 best pure bowlers** (Ensures minimum bowling requirement).
    
2.  **Select 4 overseas players** (Fills the quota with highest-ranked internationals).
    
3.  **Select 1 wicketkeeper** (If not already selected).
    
4.  **Fill remaining slots** using strategy-based scores.
    
5.  **Final Validation**: Ensure exactly 11 players.
    

⚙️ How to Run Locally
---------------------

### 🔧 Prerequisites

*   Python 3.9 or higher
    
*   pip (Python package manager)
    

### 📦 Install Dependencies

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install streamlit pandas numpy   `

### ▶️ Run the Application

Bash

streamlit run app_final.py   `

_The SQLite database (ipl\_predictor.db) is created automatically on the first run._

🧪 Debugging & Validation
-------------------------

To verify bowler detection against your specific dataset, you can run:

Python

df["is_pure_bowler"] = df.apply(is_pure_bowler_row, axis=1)  print(df[df["is_pure_bowler"]][["Player_Name", "Primary_Role"]])   `

🏆 Comparison: Why This Project is Different
--------------------------------------------

**FeatureTypical IPL PredictorsThis ProjectLogic Type**Heuristic-based**Constraint-basedRule Validity**May violate rules (e.g. 5 overseas)**Always valid XIData Handling**Hardcoded logic**CSV-drivenOutput**Unstable/Random**Deterministic & Strategy-Aware**

🔮 Future Enhancements
----------------------

*   🏟️ **Venue-based Playing XI**: Adjust selection based on pitch behavior (Spin vs Pace).
    
*   💀 **Death-over specialist selection**: Weighted scores for bowling in overs 16–20.
    
*   ⚔️ **Match-up based logic**: Adjust XI based on the opponent's weaknesses.
    
*   💡 **Explainability**: Add a section "Why this player was picked."
    

📜 Disclaimer
-------------

This project is built for **educational, analytical, and hackathon purposes only**. It does not represent official IPL team selection decisions.

🙌 Author
---------

Built with ❤️ by **Ankur Pratap Singh** _Using Python, Pandas, SQLite, and Streamlit_
