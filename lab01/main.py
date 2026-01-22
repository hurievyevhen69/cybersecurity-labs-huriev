import re
from datetime import datetime

def normalize_text(text):
    return text.lower().strip()

def extract_date_parts(date_str):
    parts = re.findall(r'\d+', date_str)
    if len(parts) >= 3:
        return {
            'day': parts[0],
            'month': parts[1],
            'year': parts[2],
            'short_year': parts[2][-2:]
        }
    return {}

def check_personal_data(password, name, surname, birthdate, email):
    password_lower = normalize_text(password)
    issues = []
    
    if name and normalize_text(name) in password_lower:
        issues.append(f"Пароль містить ім'я '{name}'")
    
    if surname and normalize_text(surname) in password_lower:
        issues.append(f"Пароль містить прізвище '{surname}'")
    
    date_parts = extract_date_parts(birthdate)
    for key, value in date_parts.items():
        if value in password_lower:
            issues.append(f"Пароль містить частину дати народження ({value})")
            break
    
    if email:
        email_name = email.split('@')[0]
        if normalize_text(email_name) in password_lower:
            issues.append("Пароль містить частину email")
    
    return issues

def evaluate_complexity(password):
    score = 0
    feedback = []
    
    length = len(password)
    if length >= 12:
        score += 3
    elif length >= 8:
        score += 2
        feedback.append("Збільште довжину до 12+ символів")
    else:
        score += 1
        feedback.append("Пароль занадто короткий (мінімум 8 символів)")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Додайте малі літери")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Додайте великі літери")
    
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Додайте цифри")
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        score += 2
    else:
        feedback.append("Додайте спеціальні символи (!@#$%^&* тощо)")
    
    common_patterns = ['123', 'abc', 'qwerty', 'password', 'admin', '111', '000']
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 2
        feedback.append("Уникайте простих послідовностей та словникових слів")
    
    return max(1, min(10, score)), feedback

def get_security_level(score):
    if score >= 8:
        return "Високий"
    elif score >= 5:
        return "Середній"
    else:
        return "Низький"

def analyze_password():
    print("=== АНАЛІЗ БЕЗПЕКИ ПАРОЛЯ ===\n")
    
    password = input("Введіть пароль: ")
    name = input("Введіть ім'я: ")
    surname = input("Введіть прізвище: ")
    birthdate = input("Введіть дату народження (ДД.ММ.РРРР): ")
    email = input("Введіть email: ")
    
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТИ АНАЛІЗУ")
    print("="*50 + "\n")
    
    personal_issues = check_personal_data(password, name, surname, birthdate, email)
    
    print("1. ПЕРЕВІРКА ПЕРСОНАЛЬНИХ ДАНИХ:")
    if personal_issues:
        print("   ⚠️  ЗНАЙДЕНО ПРОБЛЕМИ:")
        for issue in personal_issues:
            print(f"   - {issue}")
    else:
        print("   ✓ Персональні дані не виявлено")
    
    score, complexity_feedback = evaluate_complexity(password)
    
    print(f"\n2. ОЦІНКА СКЛАДНОСТІ:")
    print(f"   Бал: {score}/10")
    print(f"   Рівень безпеки: {get_security_level(score)}")
    
    print(f"\n3. РЕКОМЕНДАЦІЇ ДЛЯ ПОКРАЩЕННЯ:")
    
    all_recommendations = []
    
    if personal_issues:
        all_recommendations.append("Уникайте використання особистих даних у паролі")
    
    all_recommendations.extend(complexity_feedback)
    
    if all_recommendations:
        for i, rec in enumerate(all_recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   ✓ Пароль відповідає всім вимогам безпеки!")
    
    print("\n" + "="*50)
    print(f"ЗАГАЛЬНА ОЦІНКА: {score}/10 ({get_security_level(score)} рівень)")
    print("="*50 + "\n")

if __name__ == "__main__":
    analyze_password()
