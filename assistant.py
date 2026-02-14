import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Personal Assistant", layout="wide", page_icon="👤")

# --- DATA LOADING ---
def load_data():
    try:
        # Relative paths for Streamlit Cloud deployment
        routine = pd.read_csv('daily_routine.csv')
        vault = pd.read_csv('personal_vault.csv')
        return routine, vault
    except FileNotFoundError:
        st.error("CSV files not found. Ensure filenames match exactly on GitHub.")
        return None, None

def main():
    st.title("Hey Saksham")
    
    now_time = datetime.datetime.now().strftime("%H:%M")
    st.write(f"**Current Time:** {now_time}")

    routine, vault = load_data()

    if routine is not None and vault is not None:
        tab1, tab2, tab3 = st.tabs([" Daily Routine", " Your Details", "🔍 "])

        with tab1:
            st.header("Here Are Your Daily Tasks")
            
            # IMPROVED TIME SORTING:
            # errors='coerce' handles cases where time format might be slightly off
            routine['Time_obj'] = pd.to_datetime(routine['Time'], format='%H:%M', errors='coerce').dt.time
            
            # Sort and clean up
            routine_sorted = routine.sort_values(by='Time_obj').drop(columns=['Time_obj'])
            
            # Display sorted table
            st.table(routine_sorted)

        with tab2:
            st.header("Personal Data Vault")
            st.table(vault)

        with tab3:
            st.header("Smart Search")
            query = st.text_input("Find anything in your vault...")
            if query:
                results = vault[vault.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
                if not results.empty:
                    st.table(results)
                else:
                    st.warning("No matches found.")

if __name__ == "__main__":
    main()
