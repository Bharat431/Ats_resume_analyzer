import requests
import json

print("\n" + "="*80)
print(" "*20 + "ATS RESUME AGENT - API TEST")
print("="*80)

# Test data
resume = """Senior Python Developer with 10 years experience in machine learning and cloud architecture. 
Improved system performance by 45%. Led team of 7 engineers. 
Experience with FastAPI, AWS, Docker, Kubernetes, PostgreSQL. 
Education: MS Computer Science from MIT."""

jd = """Senior Python Developer required. 
Requirements: 8+ years Python, machine learning expertise, AWS cloud experience, team leadership background. 
Preferred: FastAPI, Kubernetes, microservices architecture."""

print("\n[TEST INPUT]")
print(f"\nResume:\n{resume}")
print(f"\nJob Description:\n{jd}")


url = "http://127.0.0.1:5000/analyze"
payload = {"resume": resume, "jd": jd}

print("\n" + "-"*80)
print("[SENDING API REQUEST]")
print("-"*80)

try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        results = response.json()
        
        print("\n[API RESPONSE - SUCCESS]")
        print(json.dumps(results, indent=2))
        
        print("\n[ANALYSIS RESULTS]")
        if "results" in results:
            r = results["results"]
            print(f"""
Keyword Score:         {r['keyword_score']:>8.2f} / 4000.00 (40% weight)
Semantic Score:        {r['semantic_score']:>8.2f} / 3000.00 (30% weight)
Format Score:          {r['format_score']:>8.2f} / 2000.00 (20% weight)
Bullet Quality Score:  {r['bullet_score']:>8.2f} / 1000.00 (10% weight)
{"─"*70}
TOTAL SCORE:           {r['final_score']:>8.2f} / 10,000
MATCH PERCENTAGE:      {(r['final_score']/10000)*100:>7.1f}%
""")
            
            percentage = (r['final_score'] / 10000) * 100
            if percentage >= 80:
                assessment = "🟢 EXCELLENT MATCH"
            elif percentage >= 60:
                assessment = "🟡 GOOD MATCH"
            elif percentage >= 40:
                assessment = "🟠 FAIR MATCH"
            else:
                assessment = "🔴 POOR MATCH"
            
            print(f"ASSESSMENT:            {assessment}\n")
            
            if "ai_suggestions" in results:
                print(f"[AI SUGGESTIONS]\n{results['ai_suggestions']}\n")
    else:
        print(f"\n[ERROR] Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")

print("\n" + "="*80)
print("API Test Complete")
print("="*80 + "\n")
