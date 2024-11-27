import streamlit as st
import sqlite3
import bcrypt

DB_FILE = "user_data.db"

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            password TEXT,
            gender TEXT,
            age INTEGER,
            face_type TEXT,
            disc_result TEXT
        )
    """)
    conn.commit()
    conn.close()

# 비밀번호 해시 함수
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# 회원가입
def register_user(user_id, password, gender, age, face_type, disc_result):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (id, password, gender, age, face_type, disc_result)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, password, gender, age, face_type, disc_result))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# 사용자 정보 가져오기
def get_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# 회원가입 페이지
def register():
    st.title("회원가입 페이지")
    user_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    gender = st.radio("성별", ["남성", "여성", "기타"])
    age = st.number_input("나이", min_value=0, step=1)
    face_type = st.text_input("얼굴상")
    disc_result = st.text_input("DISC 검사 결과")

    if st.button("회원가입"):
        if user_id and password:
            hashed_pw = hash_password(password)
            if register_user(user_id, hashed_pw, gender, age, face_type, disc_result):
                st.success("회원가입 완료!")
            else:
                st.error("이미 사용 중인 아이디입니다.")
        else:
            st.error("모든 필드를 입력하세요.")

# 로그인 페이지
def login():
    st.title("로그인 페이지")
    user_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        user = get_user(user_id)
        if user and verify_password(password, user[1]):  # user[1]은 저장된 비밀번호 해시
            st.success(f"환영합니다, {user_id}님!")
            st.write(f"성별: {user[2]}")
            st.write(f"나이: {user[3]}")
            st.write(f"얼굴상: {user[4]}")
            st.write(f"DISC 검사 결과: {user[5]}")
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")

# 메인 앱
def main():
    init_db()
    menu = st.sidebar.selectbox("메뉴 선택", ["회원가입", "로그인"])

    if menu == "회원가입":
        register()
    elif menu == "로그인":
        login()

if __name__ == "__main__":
    main()
