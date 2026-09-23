def calculate_feasibility(avg_risk_score):
    # Directly map average risk (1-5) to feasibility percentage
    score = 100 - ((avg_risk_score - 1) * 20)
    return round(max(0, min(100, score)))

def get_feasibility_status(score):
    # PPT Brackets
    if score >= 80: return "Highly Feasible"
    elif score >= 60: return "Feasible"
    elif score >= 40: return "Moderately Feasible"
    else: return "Not Feasible"