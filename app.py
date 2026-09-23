from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection
from market_analysis import get_market_summary

# --- NEW MILESTONE 2 IMPORTS (1-5 Scale Logic) ---
from risk_engine import calculate_average_risk, get_risk_status, calculate_success_probability
from swot_analysis import generate_swot
from feasibility import calculate_feasibility, get_feasibility_status
# -------------------------------------------------

# --- NEW MILESTONE 3 IMPORT (AI Logic) ---
from ai_engine import get_dynamic_recommendations
# -------------------------------------------------

app = Flask(__name__)
app.secret_key = "ml-project-secret-key"


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    summary = get_market_summary()

    latest_project = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT startup_name, industry, business_model,
                   target_market, budget, project_description
            FROM projects
            ORDER BY id DESC
            LIMIT 1
            """
        )

        latest_project = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database error:", e)

    return render_template(
        "dashboard.html",
        summary=summary,
        latest_project=latest_project
    )


@app.route("/project", methods=["GET", "POST"])
def project():
    if request.method == "POST":
        startup_name = request.form.get("startup_name", "").strip()
        industry = request.form.get("industry", "").strip()
        business_model = request.form.get("business_model", "").strip()
        target_market = request.form.get("target_market", "").strip()
        budget = request.form.get("budget", "0").strip()
        description = request.form.get("description", "").strip()

        if not startup_name or not industry or not business_model:
            flash("Please fill all required fields.", "error")
            return redirect(url_for("project"))

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO projects
                (startup_name, industry, business_model,
                 target_market, budget, project_description)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    startup_name,
                    industry,
                    business_model,
                    target_market,
                    budget or 0,
                    description
                )
            )

            conn.commit()
            cursor.close()
            conn.close()

            flash("Project submitted successfully!", "success")
            return redirect(url_for("dashboard"))

        except Exception as e:
            print("Database error:", e)
            flash("Database connection failed. Check PostgreSQL settings.", "error")
            return redirect(url_for("project"))

    return render_template("project.html")


@app.route("/risk", methods=["GET", "POST"])
def risk():
    if request.method == "POST":
        # 1. Naye HTML Form (1-5 Scale) se values lena (Default = 3)
        market_risk = int(request.form.get("market_risk", 3))
        financial_risk = int(request.form.get("financial_risk", 3))
        competition_risk = int(request.form.get("competition_risk", 3))
        technical_risk = int(request.form.get("technical_risk", 3))
        operational_risk = int(request.form.get("operational_risk", 3))

        # 2. Naye Engines ko call karke calculations karna
        avg_risk = calculate_average_risk(market_risk, financial_risk, competition_risk, technical_risk, operational_risk)
        risk_status = get_risk_status(avg_risk)
        success_prob = calculate_success_probability(avg_risk)
        
        swot = generate_swot(market_risk, financial_risk, competition_risk, technical_risk, operational_risk)
        
        feasibility_score = calculate_feasibility(avg_risk)
        feasibility_status = get_feasibility_status(feasibility_score)

        # 3. PPT ke hisaab se Final Evaluation Text generate karna
        interpretation = f"The project has an average risk score of {avg_risk}. Based on the analysis, it is categorized as {feasibility_status.upper()}. Proper planning is required to address key weaknesses and threats."

        # 4. Results ko HTML page par bhej dena
        return render_template(
            "risk_assessment.html", 
            avg_risk=avg_risk, 
            risk_status=risk_status, 
            success_prob=success_prob, 
            swot=swot, 
            feasibility_score=feasibility_score,
            feasibility_status=feasibility_status,
            interpretation=interpretation,
            # 👇 YAHAN CHANGES HUE HAIN: User inputs wapas HTML ko bhej diye
            market_risk=market_risk,
            financial_risk=financial_risk,
            competition_risk=competition_risk,
            technical_risk=technical_risk,
            operational_risk=operational_risk
        )

    # Agar normal page load ho raha hai (GET request)
    return render_template("risk_assessment.html")


@app.route("/recommendations")
def recommendations():
    # Example ke liye dummy input. Asli app mein ye database ya session se aayega.
    project_name = "Prediction AI"
    avg_risk_score = 4.2  
    
    # 🧠 Gemini API Call / Offline Dummy Data
    ai_data = get_dynamic_recommendations(project_name, avg_risk_score)
    
    # ai_data ko HTML page mein pass kar rahe hain
    return render_template("recommendations.html", title="Recommendations", ai_data=ai_data)


if __name__ == "__main__":
    app.run(debug=True)