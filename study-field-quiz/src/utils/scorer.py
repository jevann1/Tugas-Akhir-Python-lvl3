def calculate_score(answers, correct_answers):
    score = 0
    for answer, correct_answer in zip(answers, correct_answers):
        if answer == correct_answer:
            score += 1
    return score

def get_score_percentage(score, total_questions):
    if total_questions == 0:
        return 0
    return (score / total_questions) * 100

def determine_grade(score_percentage):
    if score_percentage >= 90:
        return 'A'
    elif score_percentage >= 80:
        return 'B'
    elif score_percentage >= 70:
        return 'C'
    elif score_percentage >= 60:
        return 'D'
    else:
        return 'F'