import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="My Personal Assistant", layout="wide", page_icon="👤")

# --- DATA LOADING ---
def load_data():
    try:
        # Relative paths: Streamlit Cloud only sees files inside your GitHub repo
        routine = pd.read_csv('daily_routine.csv')
        vault = pd.read_csv('personal_vault.csv')
        return routine, vault
    except FileNotFoundError:
        # This error shows if the filenames on GitHub don't match exactly
        st.error("CSV files not found. Ensure filenames match exactly on GitHub.")
        return None, None

def main():
    st.title("👤 Personal Assistant")
    
    # Display current local time
    now_time = datetime.datetime.now().strftime("%H:%M")
    st.write(f"**Current Time:** {now_time}")

    routine, vault = load_data()

    if routine is not None and vault is not None:
        tab1, tab2, tab3 = st.tabs(["📅 Daily Routine", "🔑 Vault", "🔍 Search"])

        with tab1:
            st.header("My Every Day Tasks")
            
            # TIME SORTING LOGIC:
            # We convert the text time to a real time object so 8:00 comes before 10:15
            routine['Time_obj'] = pd.to_datetime(routine['Time'], format='%H:%M').dt.time
            routine_sorted = routine.sort_values(by='Time_obj').drop(columns=['Time_obj'])
            
            # Displaying the properly ordered table
            st.table(routine_sorted)

        with tab2:
            st.header("Personal Data Vault")
            st.table(vault)

        with tab3:
            st.header("Smart Search")
            query = st.text_input("Find anything in your vault...")
            if query:
                # Search across all columns in the vault
                results = vault[vault.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
                if not results.empty:
                    st.table(results)
                else:
                    st.warning("No matches found.")

if __name__ == "__main__":
    main()
