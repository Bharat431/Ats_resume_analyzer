import json
import sys
sys.path.insert(0, '.')

from app.services.evaluation_service import evaluate

def run_benchmark():
    resume = """Python Developer with 5 years of experience in machine learning and data analysis. 
    Improved machine learning model accuracy by 35%. 
    Led team of 3 engineers in building production systems. 
    Experience with FastAPI, Django, PostgreSQL, and AWS. 
    Education: BS in Computer Science from Tech University.
    """
    
    jd = """Looking for Senior Python Developer. Required: 5+ years Python experience, 
    machine learning knowledge, experience with FastAPI or Django, AWS familiarity. 
    Preferred: Team leadership experience, published projects, strong SQL skills.
    """
    
    print("\n" + "="*70)
    print(" "*15 + "ATS RESUME AGENT - BENCHMARK RESULTS")
    print("="*70)
    
    print("\n[TEST DATA]")
    print(f"\nResume (truncated):\n{resume[:150]}...")
    print(f"\nJob Description (truncated):\n{jd[:150]}...")
    
    print("\n" + "-"*70)
    print("[RUNNING EVALUATION]")
    print("-"*70)
    
    results = evaluate(resume, jd)
    
    print("\n[SCORING RESULTS]")
    print(f"  Keyword Score:        {results['keyword_score']:>8.2f} pts (40% weight)")
    print(f"  Semantic Score:       {results['semantic_score']:>8.2f} pts (30% weight)")
    print(f"  Format Score:         {results['format_score']:>8.2f} pts (20% weight)")
    print(f"  Bullet Quality Score: {results['bullet_score']:>8.2f} pts (10% weight)")
    print("  " + "-"*50)
    print(f"  FINAL SCORE:          {results['final_score']:>8.2f} / 10,000")
    
    percentage = (results['final_score'] / 10000) * 100
    print(f"\n[MATCH PERCENTAGE]")
    print(f"  {percentage:.1f}%")
    
    if percentage >= 80:
        rating = "GREEN EXCELLENT MATCH"
    elif percentage >= 60:
        rating = "YELLOW GOOD MATCH"
    elif percentage >= 40:
        rating = "ORANGE FAIR MATCH"
    else:
        rating = "RED POOR MATCH"
    
    print(f"\n[ASSESSMENT] {rating}")
    
    print("\n" + "="*70)
    print("Benchmark Complete")
    print("="*70 + "\n")
    
    return results

if __name__ == "__main__":
    try:
        run_benchmark()
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
