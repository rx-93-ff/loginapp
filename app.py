import streamlit as st
import mysql.connector
from mysql.connector import Error
import bcrypt

# 데이터베이스 연결 설정
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",         # MySQL 서버 주소 (phpMyAdmin 로컬의 경우 localhost)
            user="root",              # MySQL 사용자 이름
            password="",   # MySQL 비밀번호
            database="streamlit_app"  # 데이터베이스 이름
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
    return None

# 비밀번호 암호화 함수
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# 회원가입 함수
def register_user(user_id, password, gender, age, face_type, disc_result):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            hashed_pw = hash_password(password)
            cursor.execute("""
                INSERT INTO user_info (user_id, password, gender, age, face_type, disc_result)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, hashed_pw, gender, age, face_type, disc_result))
            conn.commit()
            st.success("회원가입 완료!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# 사용자 정보 조회 함수
def get_user(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)  # 결과를 딕셔너리 형식으로 반환
        try:
            cursor.execute("SELECT * FROM user_info WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            return user
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    return None

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
            register_user(user_id, password, gender, age, face_type, disc_result)
        else:
            st.error("모든 필드를 입력하세요.")

# 로그인 페이지
def login():
    st.title("로그인 페이지")
    user_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        user = get_user(user_id)
        if user and verify_password(password, user["password"]):
            st.success(f"환영합니다, {user_id}님!")
            st.write(f"성별: {user['gender']}")
            st.write(f"나이: {user['age']}")
            st.write(f"얼굴상: {user['face_type']}")
            st.write(f"DISC 결과: {user['disc_result']}")
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")

# 메인 앱
def main():
    st.sidebar.title("메뉴")
    menu = st.sidebar.selectbox("옵션 선택", ["회원가입", "로그인"])

    if menu == "회원가입":
        register()
    elif menu == "로그인":
        login()

if __name__ == "__main__":
    main()
