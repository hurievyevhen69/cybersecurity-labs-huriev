import sqlite3
import datetime
import os
import textwrap

DB_PATH = "demo_sql_injection.db"
LOG_PATH = "attack.log"

def log_event(kind: str, input_value: str, extra: str = ""):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {kind} | input={repr(input_value)}"
    if extra:
        line += f" | {extra}"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            group_name TEXT NOT NULL,
            avg_grade REAL NOT NULL,
            email TEXT NOT NULL
        )
    """)

    users = [
        ("admin", "admin123", "Адміністратор Системи", "admin@demo.local", "+380987123341"),
        ("user", "qwerty", "Користувач Звичайний", "user@demo.local", "+380998900123"),
        ("vadim", "pass2026", "Вадим Макаренко", "vadim@demo.local", "+380509918203"),
    ]
    cur.executemany("INSERT INTO users(username,password,full_name,email,phone) VALUES(?,?,?,?,?)", users)

    students = [
        ("Гур'єв Євген Романович", "KI-21", 91.5, "yevhen@uni.local"),
        ("Петренко Іван Іванович", "KI-21", 78.0, "ivan@uni.local"),
        ("Шевченко Марія Олегівна", "KI-22", 88.2, "maria@uni.local"),
        ("Коваль Андрій Сергійович", "KI-23", 69.9, "andrii@uni.local"),
    ]
    cur.executemany("INSERT INTO students(full_name,group_name,avg_grade,email) VALUES(?,?,?,?)", students)

    conn.commit()
    conn.close()

def get_conn():
    return sqlite3.connect(DB_PATH)

def vulnerable_login(username: str, password: str):
    conn = get_conn()
    cur = conn.cursor()
    query = f"SELECT id, username, full_name, email, phone FROM users WHERE username = '{username}' AND password = '{password}'"
    log_event("VULN_LOGIN_QUERY", username + " | " + password, extra=f"sql={query}")
    try:
        cur.execute(query)
        row = cur.fetchone()
        conn.close()
        return row, query
    except Exception as e:
        conn.close()
        log_event("VULN_LOGIN_ERROR", username + " | " + password, extra=str(e))
        return None, query

def safe_login(username: str, password: str):
    conn = get_conn()
    cur = conn.cursor()
    query = "SELECT id, username, full_name, email, phone FROM users WHERE username = ? AND password = ?"
    log_event("SAFE_LOGIN_ATTEMPT", username + " | " + password)
    try:
        cur.execute(query, (username, password))
        row = cur.fetchone()
        conn.close()
        return row, query
    except Exception as e:
        conn.close()
        log_event("SAFE_LOGIN_ERROR", username + " | " + password, extra=str(e))
        return None, query

def vulnerable_student_search(name_like: str):
    conn = get_conn()
    cur = conn.cursor()
    query = f"SELECT id, full_name, group_name, avg_grade, email FROM students WHERE full_name LIKE '%{name_like}%'"
    log_event("VULN_SEARCH_QUERY", name_like, extra=f"sql={query}")
    try:
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows, query
    except Exception as e:
        conn.close()
        log_event("VULN_SEARCH_ERROR", name_like, extra=str(e))
        return [], query

def safe_student_search(name_like: str):
    conn = get_conn()
    cur = conn.cursor()
    query = "SELECT id, full_name, group_name, avg_grade, email FROM students WHERE full_name LIKE ?"
    log_event("SAFE_SEARCH_ATTEMPT", name_like)
    try:
        cur.execute(query, (f"%{name_like}%",))
        rows = cur.fetchall()
        conn.close()
        return rows, query
    except Exception as e:
        conn.close()
        log_event("SAFE_SEARCH_ERROR", name_like, extra=str(e))
        return [], query

def print_user(row):
    if not row:
        print("Результат: ❌ Доступ заборонено (0 збігів).")
        return
    uid, username, full_name, email, phone = row
    print("Результат: ✅ Успішний вхід!")
    print(f"  id={uid}")
    print(f"  username={username}")
    print(f"  full_name={full_name}")
    print(f"  email={email}")
    print(f"  phone={phone}")

def print_students(rows):
    if not rows:
        print("Результат: (0 записів).")
        return
    print(f"Результат: знайдено {len(rows)} запис(ів):")
    for r in rows:
        sid, full_name, group_name, avg_grade, email = r
        print(f"  #{sid} | {full_name} | {group_name} | {avg_grade} | {email}")

def demo():
    init_db()

    print("=== SQL-ін’єкції: демонстрація вразливої та захищеної версій ===")
    print(f"БД створено: {DB_PATH}")
    print(f"Лог атак:    {LOG_PATH}")
    print("\nДані для тесту (в БД):")
    print("  users: admin/admin123, user/qwerty, vadim/pass2026")
    print("  students: 4 записи\n")

    print("=== 1) Вразлива АВТОРИЗАЦІЯ (рядок підставляється в SQL) ===")
    u = input("Введіть username: ").strip()
    p = input("Введіть password: ").strip()
    row, q = vulnerable_login(u, p)
    print("\n(Вразливий SQL-запит, який виконався):")
    print(textwrap.fill(q, width=100))
    print_user(row)

    print("\nПідказка для ін’єкції (введіть як password):  ' OR '1'='1")
    print("Або як username:  admin' --")
    print("(Це для демонстрації, НЕ для реальних систем.)")

    print("\n=== 2) Захищена АВТОРИЗАЦІЯ (prepared statement) ===")
    u2 = input("Введіть username: ").strip()
    p2 = input("Введіть password: ").strip()
    row2, q2 = safe_login(u2, p2)
    print("\n(Захищений запит):")
    print(q2)
    print_user(row2)

    print("\n=== 3) Вразливий ПОШУК студентів (LIKE + пряме підставлення) ===")
    s = input("Пошук по ПІБ (фрагмент): ").strip()
    rows, q3 = vulnerable_student_search(s)
    print("\n(Вразливий SQL-запит, який виконався):")
    print(textwrap.fill(q3, width=100))
    print_students(rows)

    print("\nПідказка для ін’єкції в пошук (щоб витягнути ВСІ записи):  %' OR '1'='1")
    print("Або для провокації помилки:  '")

    print("\n=== 4) Захищений ПОШУК студентів (prepared statement) ===")
    s2 = input("Пошук по ПІБ (фрагмент): ").strip()
    rows2, q4 = safe_student_search(s2)
    print("\n(Захищений запит):")
    print(q4)
    print_students(rows2)

    print("\n=== 5) Порівняння поведінки ===")
    print("- Вразлива версія: введення стає частиною SQL → можна змінити логіку запиту (обхід пароля, витік даних).")
    print("- Захищена версія: введення передається як параметр → ін’єкція не впливає на структуру запиту.")
    print(f"\nПеревірте файл логу: {LOG_PATH} (там видно спроби та SQL для вразливих викликів).")

if __name__ == "__main__":
    demo()
