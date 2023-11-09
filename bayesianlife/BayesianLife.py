from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from database import UserInput, Food, Detox, Physical, Mental, Medical, Checklist  # Import your database classes

engine = create_engine('sqlite:///bayesian_life.db')
Session = sessionmaker(bind=engine)
session = Session()

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

import streamlit as st
from datetime import date
from sqlalchemy import func
import hashlib
import streamlit_authenticator as stauth

class BayesianLifeApp:

    def __init__(self):
        st.set_page_config(
        page_title="BayesianLife",
        page_icon="👋",
        ) 
        # Check if user is logged in
        self.stored_hashed_pw = "14fb8077481fa48aa86d2cb7c2f948eae410dda5a322ef7d38f5911efd5a6707"
    
        # Load your configuration file
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        # Create an authentication object
        self.authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )
        
        # Check if the user is logged in
        if self.is_authenticated():
            # User is authenticated, display the main app
            self.display_main_app()

    def is_authenticated(self):
        self.name, self.authentication_status, self.username = self.authenticator.login('Login', 'main')
        return self.authentication_status
    
    def display_login_page(self):
        # Display the login page with a unique key
        self.authenticator.login('Login', 'main')

    def display_main_app(self):
        if self.is_authenticated():
            st.sidebar.success("Select a demo above.")
            self.authenticator.logout('Logout', 'main')
            st.write(f'Welcome *{self.name}*')
            st.title("Bayesian Life")
            
            selected_date = st.date_input("Select Date", value=date.today())
            
            if self.date_submitted(selected_date):
                st.write(f"Data for {selected_date} has already been submitted!")

            # Get default values for Food and Detox
            default_broth = self.get_most_common_value(Food.broth)
            default_coffee = self.get_most_common_value(Food.coffee)
            default_kavas = self.get_most_common_value(Food.kavas)
            default_kefir = self.get_most_common_value(Food.kefir)
            default_yogurt = self.get_most_common_value(Food.yogurt)
            default_sour_cream = self.get_most_common_value(Food.sour_cream)
            default_ferment_veg = self.get_most_common_value(Food.ferment_veg)
            default_fish = self.get_most_common_value(Food.fish)
            default_organ_meat = self.get_most_common_value(Food.organ_meat)
            default_kimchi = self.get_most_common_value(Food.kimchi)
            default_chocolate = self.get_most_common_value(Food.chocolate)  # Added chocolate
            default_nuts = self.get_most_common_value(Food.nuts)  # Added nuts
            default_cheese = self.get_most_common_value(Food.cheese)  # Added cheese
            default_pig_out = self.get_most_common_value(Food.pig_out)  # Added pig_out
            default_coconut = self.get_most_common_value(Food.coconut)  # Added coconut
            default_bath = self.get_most_common_value(Detox.bath)
            default_juice = self.get_most_common_value(Food.juice)
            default_ocean = self.get_most_common_value(Detox.ocean)
            default_sunshine = self.get_most_common_value(Detox.sunshine)
            default_enema = self.get_most_common_value(Detox.enema)
            default_fruit = self.get_most_common_value(Food.fruit)
            default_cheat = self.get_most_common_value(Food.cheat)
            default_fruit_juice = self.get_most_common_value(Food.fruit_juice)

            #
        
            # Get default values for Physical
            default_BJJ = self.get_most_common_value(Physical.BJJ)
            default_stretching = self.get_most_common_value(Physical.stretching)
            default_walking = self.get_most_common_value(Physical.walking)
            default_sex = self.get_most_common_value(Physical.sex)
            default_myofascial = self.get_most_common_value(Physical.myofascial)
            default_workout = self.get_most_common_value(Physical.workout)

            # Get default values for Mental
            default_piano = self.get_most_common_value(Mental.piano)
            default_breath = self.get_most_common_value(Mental.breath)
            default_cold = self.get_most_common_value(Mental.cold)
            default_gardening = self.get_most_common_value(Mental.gardening)
            default_wank = self.get_most_common_value(Mental.wank)  # Added wank

            # Get default values for Medical
            default_cannabis_oil = self.get_most_common_value(Medical.cannabis_oil)
            default_cannabis_vape = self.get_most_common_value(Medical.cannabis_vape)
            default_cannabis_flower = self.get_most_common_value(Medical.cannabis_flower)
            default_ashwagandha = self.get_most_common_value(Medical.ashwagandha)
            default_cbd_oil = self.get_most_common_value(Medical.cbd_oil)
            default_cbd_vape = self.get_most_common_value(Medical.cbd_vape)
            default_lions_mane = self.get_most_common_value(Medical.lions_mane)
            default_psilocybin = self.get_most_common_value(Medical.psilocybin)
            default_liver = self.get_most_common_value(Medical.liver)
            default_probiotics = self.get_most_common_value(Medical.probiotics)
            default_stressmush = self.get_most_common_value(Medical.stressmush)

            default_mood = self.get_most_common_value(Checklist.mood)
            default_sleep = self.get_most_common_value(Checklist.sleep)
            default_stress = self.get_most_common_value(Checklist.stress)
            default_inflammation = self.get_most_common_value(Checklist.inflammation)
            default_energy = self.get_most_common_value(Checklist.energy)
            default_headache = self.get_most_common_value(Checklist.headache)
            default_back_pain = self.get_most_common_value(Checklist.back_pain)
            default_stool = self.get_most_common_value(Checklist.stool)
            default_screen_time = self.get_most_common_value(Checklist.screen_time)

            # Tabs for each category
            tab_food, tab_detox, tab_physical, tab_mental, tab_medical, tab_checklist = st.tabs(
                ["Food", "Detox", "Physical", "Mental", "Medical", "Checklist"]
            )

            # Food tab
            with tab_food:
                broth = st.selectbox("Broth Intake", [0, 1, 2, 3, 4, 5], index=default_broth or 2)
                coffee = st.selectbox("Coffee Intake", [0, 1, 2, 3, 4, 5], index=default_coffee or 2)
                kavas = st.checkbox("Kavas", default_kavas or False)
                kefir = st.checkbox("Kefir", default_kefir or False)
                yogurt = st.checkbox("Yogurt", default_yogurt or False)
                sour_cream = st.checkbox("Sour Cream", default_sour_cream or False)
                ferment_veg = st.checkbox("Fermented Vegetables", default_ferment_veg or False)
                fish = st.checkbox("Fish", default_fish or False)
                organ_meat = st.checkbox("Organ Meat", default_organ_meat or False)
                kimchi = st.checkbox("Kimchi", default_kimchi or False)
                chocolate = st.checkbox("Chocolate", default_chocolate or False)  # Added chocolate
                nuts = st.checkbox("Nuts", default_nuts or False)  # Added Nuts
                cheese = st.checkbox("Cheese", default_cheese or False)  # Added Cheese
                pig_out = st.checkbox("Pig Out", default_pig_out or False)  # Added Pig Out
                coconut = st.checkbox("Coconut", default_coconut or False)  # Added Coconut
                fruit = st.checkbox("Fruit", default_fruit or False)  # Added Fruit
                cheat = st.checkbox("Cheat", default_cheat or False)
                fruit_juice = st.checkbox("Fruit Juice", default_fruit_juice or False)




            # Detox tab
            with tab_detox:
                bath = st.checkbox("Bath", default_bath or False)
                juice = st.checkbox("Juice", default_juice or False)
                ocean = st.checkbox("Ocean", default_ocean or False)
                sunshine = st.checkbox("Sunshine", default_sunshine or False)
                enema = st.checkbox("Enema", default_enema or False)

            # Physical tab
            with tab_physical:
                BJJ = st.checkbox("BJJ", default_BJJ or False)
                stretching = st.checkbox("Stretching", default_stretching or False)
                walking = st.checkbox("Walking", default_walking or False)
                sex = st.checkbox("Sex", default_sex or False)
                myofascial = st.checkbox("Myofascial", default_myofascial or False)
                workout = st.checkbox("Workout", default_workout or False)

            # Mental tab
            with tab_mental:
                piano = st.checkbox("Piano", default_piano or False)
                breath = st.checkbox("Breath", default_breath or False)
                cold = st.checkbox("Cold", default_cold or False)
                gardening = st.checkbox("Gardening", default_gardening or False)
                wank = st.checkbox("Wank", default_wank or False)  # Added wank

            # Medical tab
            with tab_medical:
                cannabis_oil = st.checkbox("Cannabis Oil", default_cannabis_oil or False)
                cannabis_vape = st.checkbox("Cannabis Vape", default_cannabis_vape or False)
                cannabis_flower = st.checkbox("Cannabis Flower", default_cannabis_flower or False)
                ashwagandha = st.checkbox("Ashwagandha", default_ashwagandha or False)
                cbd_oil = st.checkbox("CBD Oil", default_cbd_oil or False)
                cbd_vape = st.checkbox("CBD Vape", default_cbd_vape or False)
                lions_mane = st.checkbox("Lion's Mane", default_lions_mane or False)
                psilocybin = st.checkbox("Psilocybin", default_psilocybin or False)
                liver = st.checkbox("Liver", default_liver or False)
                probiotics = st.checkbox("Probiotics", default_probiotics or False)
                stressmush = st.checkbox("StressMush", default_stressmush or False)

            # Checklist tab
            with tab_checklist:
                mood = st.slider("Mood Level", 0, 5, default_mood or 2)
                sleep = st.slider("Sleep Quality/Quantity", 0, 5, default_sleep or 2)
                stress = st.slider("Stress Level", 0, 5, default_stress or 2)
                inflammation = st.slider("Inflammation Level", 0, 5, default_inflammation or 2)
                energy = st.slider("Energy Level", 0, 5, default_energy or 2)
                headache = st.slider("Headache Severity", 0, 5, default_headache or 2)
                back_pain = st.slider("Back Pain Severity", 0, 5, default_back_pain or 2)
                stool = st.slider("Stool Quality/Quantity", 1, 7, default_stool or 4 )
                screen_time = st.slider("Screen Time", 0, 5, default_screen_time or 2)

            resubmit = st.checkbox("Resubmit")

            if self.is_authenticated():
                if st.button("Submit"):
                    result = self.bayesian_life(
                        selected_date, broth, kavas, coffee, kefir, yogurt, sour_cream, ferment_veg, fish, organ_meat, kimchi, 
                        chocolate, nuts, cheese, pig_out, coconut, fruit, cheat, fruit_juice,  # Added chocolate
                        bath, juice, ocean, sunshine, enema, BJJ, stretching, walking, sex, myofascial, workout, 
                        piano, breath, cold, gardening, wank,  # Added wank
                        cannabis_oil, cannabis_vape, cannabis_flower, ashwagandha, cbd_oil, cbd_vape, lions_mane, 
                        psilocybin, liver, probiotics, stressmush,
                        mood, sleep, stress, inflammation, energy, headache, stool, back_pain, screen_time,
                        resubmit
                    )
                    st.text(result)

                
                


    def bayesian_life(self, selected_date, broth, kavas, coffee, kefir, yogurt, sour_cream, ferment_veg, fish, organ_meat, kimchi, 
                  chocolate,  # Added chocolate
                  nuts,  # Added nuts
                  cheese,  # Added cheese
                  pig_out,  # Added pig_out
                  coconut,
                  fruit, cheat, fruit_juice,
                  bath, juice, ocean, sunshine, enema, BJJ, stretching, walking, sex, myofascial, workout, 
                  piano, breath, cold, gardening, wank,  # Added wank
                  cannabis_oil, cannabis_vape, cannabis_flower, ashwagandha, cbd_oil, cbd_vape, lions_mane, 
                  psilocybin, liver, probiotics, stressmush, mood, sleep, stress, inflammation, energy, headache, stool, back_pain, screen_time, resubmit=False):

        session = Session()
        existing_entry = session.query(UserInput).filter_by(selected_date=selected_date).first()

        if existing_entry and existing_entry.submitted and not resubmit:
            session.close()
            return "Already submitted for this date. Would you like to resubmit?"

        if existing_entry and resubmit:
            # Update Food
            existing_entry.food.broth = broth
            existing_entry.food.coffee = coffee
            existing_entry.food.kavas = kavas
            existing_entry.food.kefir = kefir
            existing_entry.food.yogurt = yogurt
            existing_entry.food.sour_cream = sour_cream
            existing_entry.food.ferment_veg = ferment_veg
            existing_entry.food.fish = fish
            existing_entry.food.organ_meat = organ_meat
            existing_entry.food.kimchi = kimchi
            existing_entry.food.chocolate = chocolate  # Added chocolate
            existing_entry.food.nuts = nuts  # Added nuts
            existing_entry.food.cheese = cheese  # Added cheese
            existing_entry.food.pig_out = pig_out  # Added pig_out
            existing_entry.food.coconut = coconut  # Added coconut
            existing_entry.food.fruit = fruit  # Added fruit
            existing_entry.food.cheat = cheat
            existing_entry.food.fruit_juice = fruit_juice



            # Update Detox
            existing_entry.detox.bath = bath
            existing_entry.detox.juice = juice
            existing_entry.detox.ocean = ocean
            existing_entry.detox.sunshine = sunshine
            existing_entry.detox.enema = enema

            # Update Physical
            existing_entry.physical.BJJ = BJJ
            existing_entry.physical.stretching = stretching
            existing_entry.physical.walking = walking
            existing_entry.physical.sex = sex
            existing_entry.physical.myofascial = myofascial
            existing_entry.physical.workout = workout

            # Update Mental
            existing_entry.mental.piano = piano
            existing_entry.mental.breath = breath
            existing_entry.mental.cold = cold
            existing_entry.mental.gardening = gardening
            existing_entry.mental.wank = wank  # Added wank

            # Update Medical
            existing_entry.medical.cannabis_oil = cannabis_oil
            existing_entry.medical.cannabis_vape = cannabis_vape
            existing_entry.medical.cannabis_flower = cannabis_flower
            existing_entry.medical.ashwagandha = ashwagandha
            existing_entry.medical.cbd_oil = cbd_oil
            existing_entry.medical.cbd_vape = cbd_vape
            existing_entry.medical.lions_mane = lions_mane
            existing_entry.medical.psilocybin = psilocybin
            existing_entry.medical.liver = liver
            existing_entry.medical.probiotics = probiotics
            existing_entry.medical.stressmush = stressmush

            # Update Checklist
            existing_entry.checklist.mood = mood
            existing_entry.checklist.sleep = sleep
            existing_entry.checklist.stress = stress
            existing_entry.checklist.inflammation = inflammation
            existing_entry.checklist.energy = energy
            existing_entry.checklist.headache = headache
            existing_entry.checklist.stool = stool
            existing_entry.checklist.back_pain = back_pain
            existing_entry.checklist.screen_time = screen_time

        else:
            # New entries for UserInput, Food, Detox, Physical, Mental, and Medical
            new_input = UserInput(selected_date=selected_date.strftime("%Y-%m-%d"), submitted=True)
            session.add(new_input)

            new_food = Food(selected_date=selected_date.strftime("%Y-%m-%d"), broth=broth, coffee=coffee, kavas=kavas, 
                        kefir=kefir, yogurt=yogurt, sour_cream=sour_cream, ferment_veg=ferment_veg, 
                        fish=fish, organ_meat=organ_meat, kimchi=kimchi, chocolate=chocolate, nuts=nuts,
                        cheese=cheese, pig_out=pig_out, coconut=coconut, fruit=fruit, cheat=cheat, fruit_juice=fruit_juice)  # Added chocolate, nuts, cheese, pig_out, coconut
            session.add(new_food)

            new_detox = Detox(selected_date=selected_date.strftime("%Y-%m-%d"), bath=bath, juice=juice, ocean=ocean, 
                        sunshine=sunshine, enema=enema)
            session.add(new_detox)

            new_physical = Physical(selected_date=selected_date.strftime("%Y-%m-%d"), BJJ=BJJ, stretching=stretching,
                                walking=walking, sex=sex, myofascial=myofascial, workout=workout)
            session.add(new_physical)

            new_mental = Mental(selected_date=selected_date.strftime("%Y-%m-%d"), piano=piano, breath=breath, cold=cold, 
                            gardening=gardening, wank=wank)  # Added wank
            session.add(new_mental)

            new_medical = Medical(selected_date=selected_date.strftime("%Y-%m-%d"), cannabis_oil=cannabis_oil, cannabis_vape=cannabis_vape,
                        cannabis_flower=cannabis_flower, ashwagandha=ashwagandha, cbd_oil=cbd_oil, cbd_vape=cbd_vape,
                        lions_mane=lions_mane, psilocybin=psilocybin, liver=liver, probiotics=probiotics, 
                        stressmush=stressmush)
            session.add(new_medical)

            # New entry for Checklist
            new_checklist = Checklist(selected_date=selected_date.strftime("%Y-%m-%d"), mood=mood, sleep=sleep, stress=stress,
                              inflammation=inflammation, energy=energy, headache=headache, stool=stool, 
                              back_pain=back_pain, screen_time=screen_time)
            session.add(new_checklist)

        session.commit()
        session.close()
        return "Your data has been submitted successfully!"


        


    def get_most_common_value(self, column):
        session = Session()
        most_common = session.query(column).group_by(column).order_by(func.count(column).desc()).first()
        session.close()
        return most_common[0] if most_common else None

    def date_submitted(self, selected_date):
        session = Session()
        existing_entry = session.query(UserInput).filter_by(selected_date=selected_date).first()
        session.close()
        return existing_entry is not None

    

if __name__ == "__main__":
    app = BayesianLifeApp()


