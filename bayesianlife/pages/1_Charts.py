import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import UserInput, Food, Detox, Physical, Mental, Medical, Checklist  # Import your database classes

# Create a Streamlit app
st.title("Bayesian Life App")

# Sidebar for user input and navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Select Page", ["Data Selection", "Graphs"])

# Connect to the database
engine = create_engine('sqlite:///bayesian_life.db')
Session = sessionmaker(bind=engine)
session = Session()

if page == "Data Selection":
    st.header("Data Selection Page")
    
    # User selects date range
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    # User selects columns or tables for plotting
    selected_columns = st.multiselect("Select Columns", [
        "food.broth", "food.coffee", "food.kavas", "food.kefir", "food.yogurt", 
        "food.sour_cream", "food.ferment_veg", "food.fish", "food.organ_meat", "food.kimchi", 
        "detox.bath", "detox.juice", "detox.ocean", "detox.sunshine", "detox.enema", 
        "physical.BJJ", "physical.stretching", "physical.walking", "physical.sex", "physical.myofascial", "physical.workout", 
        "mental.piano", "mental.breath", "mental.cold", "mental.gardening", 
        "medical.cannabis_oil", "medical.cannabis_vape", "medical.cannabis_flower", "medical.ashwagandha", 
        "medical.cbd_oil", "medical.cbd_vape", "medical.lions_mane", "medical.psilocybin", 
        "medical.liver", "medical.probiotics", "medical.stressmush", 
        "checklist.mood", "checklist.sleep", "checklist.stress", "checklist.inflammation", 
        "checklist.energy", "checklist.headache", "checklist.back_pain", "checklist.stool"
    ])  
    
    # Query the database based on user selections
    selected_data = session.query(
        UserInput.selected_date,
        Food.broth, Food.coffee, Food.kavas, Food.kefir, Food.yogurt, 
        Food.sour_cream, Food.ferment_veg, Food.fish, Food.organ_meat, Food.kimchi, 
        Detox.bath, Detox.juice, Detox.ocean, Detox.sunshine, Detox.enema, 
        Physical.BJJ, Physical.stretching, Physical.walking, Physical.sex, Physical.myofascial, Physical.workout, 
        Mental.piano, Mental.breath, Mental.cold, Mental.gardening, 
        Medical.cannabis_oil, Medical.cannabis_vape, Medical.cannabis_flower, Medical.ashwagandha, 
        Medical.cbd_oil, Medical.cbd_vape, Medical.lions_mane, Medical.psilocybin, 
        Medical.liver, Medical.probiotics, Medical.stressmush, 
        Checklist.mood, Checklist.sleep, Checklist.stress, Checklist.inflammation, 
        Checklist.energy, Checklist.headache, Checklist.back_pain, Checklist.stool
    ).join(
        Food, Detox, Physical, Mental, Medical, Checklist
    ).filter(
        UserInput.selected_date.between(start_date, end_date)
    ).all()
    
    # Process the selected data and prepare it for plotting
    data_dict = {}
    for column in selected_columns:
        data_dict[column] = [getattr(entry, column) for entry in selected_data]
    
    df = pd.DataFrame(data_dict)
    
    # Plot the data
    st.subheader("Data Preview")
    st.write(df)  # Display the data as a table
    
    if st.button("Plot Graph"):
        # Plot selected data
        fig, ax = plt.subplots()
        for column in selected_columns:
            ax.plot(df.index, df[column], label=column)
        
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.legend()
        
        st.pyplot(fig)

elif page == "Graphs":
    st.header("Graphs Page")
    
    # Add code to display graphs based on user selections or saved data

# Close the database session
session.close()






