import streamlit as st
import psycopg2
import time
import hashlib
from streamlit_option_menu import option_menu
import pandas
import toml

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
    with st.sidebar:
        selected = option_menu("CWLB", ["Lista zwierząt", 'Dodaj zwierzę', 'Usuń zwierzę', 'Dodaj użytkownika', 'Zmień dizajn'], 
        icons=['card-list', 'plus-lg', 'x-lg', 'person-plus'], menu_icon="cast", default_index=0)
    if selected == "Lista zwierząt":
        
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

        df = pandas.DataFrame(rows, columns=["ID", "Imię", "Rasa", "Kolor", "Zdjęcie", "Numer", "Choroby"])
        df['Zdjęcie'] = df['Zdjęcie'].apply(lambda x: f'<img src="{x}" width="100">' if x != 'brak' else 'brak')
        #convert df to html
        print(df.to_html(escape=False, index=False))
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    elif selected == "Dodaj użytkownika":


        with st.form("registeruser"):
            username = st.text_input("Nazwa użytkownika")
            password = st.text_input("Hasło", type='password')
            if st.form_submit_button("Zarejestruj"):
                registerWithHash(username, password)
                st.success("Zarejestrowano")
                time.sleep(1)
                st.rerun()
    elif selected == "Zmień dizajn":
        #get long text from user and put it in ./.streamlit/config.toml
        
        #if long text is empty, show colour pickers for primaryColor, backgroundColor, secondaryBackgroundColor, textColor
        st.write("Wybierz kolory")
        col1, col2 = st.columns(2)
        # Load existing config if available
        try:
            with open("./.streamlit/config.toml", "r") as f:
                config_data = toml.load(f)
                primaryColor = config_data["theme"].get("primaryColor", "#ff0000")
                backgroundColor = config_data["theme"].get("backgroundColor", "#ffffff")
                secondaryBackgroundColor = config_data["theme"].get("secondaryBackgroundColor", "#f0f0f0")
                textColor = config_data["theme"].get("textColor", "#000000")
        except FileNotFoundError:
            primaryColor = "#ff0000"
            backgroundColor = "#ffffff"
            secondaryBackgroundColor = "#f0f0f0"
            textColor = "#000000"

        with col1:
            primaryColor = st.color_picker("Kolor główny", primaryColor)
            backgroundColor = st.color_picker("Kolor tła", backgroundColor)
        with col2:
            secondaryBackgroundColor = st.color_picker("Kolor tła drugoplanowego", secondaryBackgroundColor)
            textColor = st.color_picker("Kolor tekstu", textColor)
        # compile the colors into a string like this:
#         """
#         [theme]
# primaryColor="#575366"
# backgroundColor="#6e7dab"
# secondaryBackgroundColor="#929226"
# textColor="#32292f"""
#and put it in ./.streamlit/config.toml
        config = f"""
[theme]
primaryColor="{primaryColor}"
backgroundColor="{backgroundColor}"
secondaryBackgroundColor="{secondaryBackgroundColor}"
textColor="{textColor}"
        """
        if st.button("Zapisz"):
            with open("./.streamlit/config.toml", "w") as f:
                f.write(config)
            st.success("Zapisano")
            time.sleep(1)
            st.rerun()

        if st.button("Pobierz lokalny plik"):
            st.download_button("Pobierz plik", config, "config.toml", "toml")
    
        

