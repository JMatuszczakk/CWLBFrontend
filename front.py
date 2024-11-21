import streamlit as st
import psycopg2
st.title("CWL Bełchatów")

if "stage" not in st.session_state:
    st.session_state["stage"] = 0

def checkLogin(username, password):
    #TODO
    #create a connection to postgresql to check the username and password hash to login to dashboard
    con = psycopg2.connect(
        host="cwlb.matuszczak.org",
        database="cwl1",
        user="postgres",
        password="cwlbełchatów"
    )
    #fetch all usernames and crosscheck the password hash and username
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    con.close()
    
    if result is None:
        return False
    print(result)
    stored_password = result[0]
    print(stored_password)
    return stored_password == password

    return True

if st.session_state['stage'] == 0:
    with st.form("dd"):
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło", type='password')
        if st.form_submit_button("Zaloguj"):
            print(checkLogin(username, password))


