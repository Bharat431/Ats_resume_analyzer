"""Report generation service for evaluation results"""

def generate_report(results):
    """Generate a formatted report from evaluation results"""
    final_score = results['final_score']
    percentage = (final_score / 10000) * 100
    
    # Determine match quality
    if percentage >= 80:
        quality = "Excellent"
    elif percentage >= 60:
        quality = "Good"
    elif percentage >= 40:
        quality = "Fair"
    else:
        quality = "Poor"
    
    report = f"""
===== ATS Resume Analysis Report =====

Final Score: {final_score} / 10,000 ({percentage:.1f}%)
Match Quality: {quality}

===== Score Breakdown =====
Keyword Score: {results['keyword_score']} (40%)
Semantic Score: {results['semantic_score']} (30%)
Format Score: {results['format_score']} (20%)
Bullet Quality: {results['bullet_score']} (10%)

===== Recommendations =====
"""
    
    if results['keyword_score'] < 800:
        report += "- Increase keyword density from job description\n"
    if results['semantic_score'] < 900:
        report += "- Improve semantic relevance to job requirements\n"
    if results['format_score'] < 1600:
        report += "- Add 'Experience' and 'Education' sections\n"
    if results['bullet_score'] < 800:
        report += "- Include more quantified achievements (%, numbers)\n"
    
    report += "\n" + "=" * 40
    return report