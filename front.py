import streamlit as st
import psycopg2
import time
import hashlib
st.title("CWL Bełchatów")



if "stage" not in st.session_state:
    st.session_state["stage"] = 0

def checkLogin(username, password):
    con = psycopg2.connect(
        host="central",
        database="cwl1",
        user="postgres",
        password="cwlbełchatów"
    )
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    con.close()

    if result is None:
        return False
    
    stored_password = result[0]
    passwordHash = hashlib.sha256(password.encode()).hexdigest()
    return stored_password == passwordHash


def registerWithHash(username, password):
    con = psycopg2.connect(
        host="central",
        database="cwl1",
        user="postgres",
        password="cwlbełchatów"
    )
    cur = con.cursor()
    passwordHash = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, passwordHash))
    con.commit()
    con.close()

    

if st.session_state['stage'] == 0:
    with st.form("dd"):
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło", type='password')
        if st.form_submit_button("Zaloguj"):
            if checkLogin(username, password):
                st.success("Zalogowano")
                st.session_state['stage'] = 1
                time.sleep(1)
                st.rerun()
            else:
                st.error("Niepoprawne dane logowania")

if st.session_state['stage'] == 1:
    st.title("CWL Bełchatów - Panel")
    st.success("Zalogowano", icon="🔒")
    con = psycopg2.connect(
        host="central",
        database="cwl1",
        user="postgres",
        password="cwlbełchatów"
    )
    cur = con.cursor()
    cur.execute("SELECT id, name, race, color, photo, number, illnesses FROM dogs")
    rows = cur.fetchall()
    con.close()

    for row in rows:
        st.write(f"ID: {row[0]}")
        st.write(f"Nazwa: {row[1]}")
        st.write(f"Rasa: {row[2]}")
        st.write(f"Kolor: {row[3]}")
        st.write(f"Numer: {row[5]}")
        st.write(f"Choroby: {row[6]}")
        st.write("---")
    

    with st.form("registeruser"):
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło", type='password')
        if st.form_submit_button("Zarejestruj"):
            registerWithHash(username, password)
            st.success("Zarejestrowano")
            time.sleep(1)
            st.rerun()

