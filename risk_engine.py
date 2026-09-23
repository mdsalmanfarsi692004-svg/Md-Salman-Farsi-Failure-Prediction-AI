def calculate_average_risk(market, financial, competition, technical, operational):
    # PPT Logic: Average = Sum of 5 risks / 5
    avg_score = (market + financial + competition + technical + operational) / 5
    return round(avg_score, 1)

def get_risk_status(avg_score):
    if avg_score >= 4:
        return "HIGH RISK"
    elif avg_score >= 2.5:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"

def calculate_success_probability(avg_score):
    # Convert 1-5 scale to percentage (1 -> ~100%, 5 -> ~20%)
    prob = max(0, 100 - ((avg_score - 1) * 20))
    return round(prob)