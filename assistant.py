import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="My Personal Assistant", layout="wide", page_icon="👤")

# --- DATA LOADING ---
def load_data():
    try:
        # Relative paths for Streamlit Cloud (no /content/drive/)
        routine = pd.read_csv('dailyroutine.csv')
        vault = pd.read_csv('personal details.csv')
        return routine, vault
    except FileNotFoundError:
        st.error("CSV files not found. Ensure they are uploaded to the same GitHub folder.")
        return None, None

def main():
    st.title("👤 Personal Assistant")
    
    now = datetime.datetime.now().strftime("%H:%M")
    st.write(f"**Current Time:** {now}")

    routine, vault = load_data()

    if routine is not None and vault is not None:
        tab1, tab2, tab3 = st.tabs(["📅 Daily Routine", "🔑 Vault", "🔍 Search"])

        with tab1:
            st.header("My Every Day Tasks")
            
            # FIXING THE TIME SORTING:
            # Convert 'Time' to datetime objects so 8:00 comes before 10:15
            routine['Time_obj'] = pd.to_datetime(routine['Time'], format='%H:%M').dt.time
            routine_sorted = routine.sort_values(by='Time_obj').drop(columns=['Time_obj'])
            
            # Display sorted table
            st.table(routine_sorted)

        with tab2:
            st.header("Personal Data Vault")
            st.table(vault)

        with tab3:
            st.header("Smart Search")
            query = st.text_input("Find anything...")
            if query:
                results = vault[vault.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
                st.table(results)

if __name__ == "__main__":
    main()
