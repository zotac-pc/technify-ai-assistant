def generate_study_plan(results_data: dict) -> str:
    if not results_data: return 'No academic data available.'
    results = results_data if isinstance(results_data, list) else results_data.get('results', [])
    weak   = [r for r in results if r.get('percentage', 100) < 60]
    strong = [r for r in results if r.get('percentage', 0) >= 75]
    plan = 'PERSONALIZED STUDY PLAN\n' + '='*30 + '\n\n'
    if weak:
        plan += 'PRIORITY (Weak Subjects - Need Extra Attention):\n'
        for w in weak:
            plan += f"  - {w.get('course_name','Unknown')}: "
            plan += f"{w.get('percentage',0)}% - Study 2 hours/day\n"
    if strong:
        plan += '\nSTRONG Subjects (Maintain Performance):\n'
        for s in strong:
            plan += f"  - {s.get('course_name','Unknown')}: "
            plan += f"{s.get('percentage',0)}% - Review 30 min/day\n"
    plan += '\nRECOMMENDED SCHEDULE:\n'
    plan += '  Mon/Wed/Fri: Focus on weak subjects\n'
    plan += '  Tue/Thu: Review strong subjects\n'
    plan += '  Sat: Practice problems and past papers\n'
    plan += '  Sun: Rest and light revision\n'
    return plan
