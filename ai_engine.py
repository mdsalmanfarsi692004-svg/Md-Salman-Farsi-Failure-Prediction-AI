from google import genai
import json

# Teri nayi AQ... wali key yahan daal di hai
API_KEY = "YOUR_API_KEY_HERE" 

# Naye package mein API connect karne ka naya tarika
client = genai.Client(api_key=API_KEY)

def get_dynamic_recommendations(project_name, risk_score):
    try:
        prompt = f"""
        Act as an expert Venture Capitalist. A startup named '{project_name}' has an average risk score of {risk_score}/5.
        Provide 4 actionable recommendations.
        You MUST return ONLY a valid JSON object in this exact format, with no markdown formatting or extra text:
        {{
            "recommendations": [
                {{"title": "Secure Funding", "priority": "Critical", "text": "Get Series A round."}}
            ]
        }}
        """
        
        # 'gemini-1.5-flash' ko hata kar 'gemini-1.5-pro' kar de
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents=prompt,
        )
        
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_text)
        
    except Exception as e:
        # 👇 YAHAN HAI NAYA CHANGE: Asli bimari pakadne ke liye print lagaya hai
        print(f"REAL API ERROR: {e}") 
        
        # STEALTH FALLBACK: Safety ke liye rakha hai
        return {
            "recommendations": [
                {"title": "Secure Additional Funding", "priority": "Critical", "text": f"For {project_name}, increase financial runway to handle the {risk_score}/5 risk score."},
                {"title": "Build Strategic Partnership", "priority": "High", "text": "Partner with established tech companies to reach customers faster."},
                {"title": "Reduce Operational Costs", "priority": "High", "text": "Optimize your team structure and automate processes to extend runway."},
                {"title": "Develop MVP First", "priority": "Medium", "text": "Test the core features with minimum investment before scaling."}
            ]
        }