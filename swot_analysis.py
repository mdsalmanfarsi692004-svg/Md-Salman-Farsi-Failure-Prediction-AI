def generate_swot(market, financial, competition, technical, operational):
    swot = {"Strengths": [], "Weaknesses": [], "Opportunities": [], "Threats": []}
    
    # Logic based on 1-5 scale (1-2 is Good, 4-5 is Bad)
    if technical <= 2: swot["Strengths"].append("Strong technical capability")
    if operational <= 2: swot["Strengths"].append("Smooth operational plan")
    
    if financial >= 4: swot["Weaknesses"].append("Limited financial resources")
    if technical >= 4: swot["Weaknesses"].append("Lack of technical expertise")
    
    if market <= 2: swot["Opportunities"].append("High market demand")
    if competition <= 2: swot["Opportunities"].append("Low market competition")
    
    if competition >= 4: swot["Threats"].append("Strong existing competitors")
    if market >= 4: swot["Threats"].append("Low customer interest")
    
    # Fallbacks if empty
    if not swot["Strengths"]: swot["Strengths"].append("Dedicated project team")
    if not swot["Weaknesses"]: swot["Weaknesses"].append("Initial setup challenges")
    if not swot["Opportunities"]: swot["Opportunities"].append("Potential for market expansion")
    if not swot["Threats"]: swot["Threats"].append("Unforeseen market changes")
        
    return swot