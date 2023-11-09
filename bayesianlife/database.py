from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserInput(Base):
    __tablename__ = 'user_input'
    
    id = Column(Integer, primary_key=True)
    selected_date = Column(String, unique=True)
    submitted = Column(Boolean, default=False)

    food = relationship("Food", uselist=False, back_populates="user_input")
    detox = relationship("Detox", uselist=False, back_populates="user_input")
    physical = relationship("Physical", uselist=False, back_populates="user_input")
    mental = relationship("Mental", uselist=False, back_populates="user_input")
    medical = relationship("Medical", uselist=False, back_populates="user_input")
    checklist = relationship("Checklist", uselist=False, back_populates="user_input")

class Food(Base):
    __tablename__ = 'food'
    
    id = Column(Integer, primary_key=True)
    selected_date = Column(String, ForeignKey('user_input.selected_date'))
    broth = Column(Integer)
    kavas = Column(Boolean)
    coffee = Column(Integer)
    kefir = Column(Boolean)
    yogurt = Column(Boolean)
    sour_cream = Column(Boolean)
    ferment_veg = Column(Boolean)
    fish = Column(Boolean)
    organ_meat = Column(Boolean)
    kimchi = Column(Boolean)
    chocolate = Column(Boolean)
    nuts = Column(Boolean)
    cheese = Column(Boolean)
    pig_out = Column(Boolean)
    coconut = Column(Boolean)
    fruit = Column(Boolean)
    cheat = Column(Boolean)
    juice = Column(Boolean)
    fruit_juice = Column(Boolean)

    user_input = relationship("UserInput", back_populates="food")

class Detox(Base):
    __tablename__ = 'detox'
    
    id = Column(Integer, primary_key=True)
    selected_date = Column(String, ForeignKey('user_input.selected_date'))
    bath = Column(Boolean)
    juice = Column(Boolean)
    ocean = Column(Boolean)
    sunshine = Column(Boolean)
    enema = Column(Boolean)
    
    user_input = relationship("UserInput", back_populates="detox")

class Physical(Base):
    __tablename__ = 'physical'
    
    id = Column(Integer, primary_key=True)
    selected_date = Column(String, ForeignKey('user_input.selected_date'))
    BJJ = Column(Boolean)
    stretching = Column(Boolean)
    walking = Column(Boolean)
    sex = Column(Boolean)
    myofascial = Column(Boolean)
    workout = Column(Boolean)
    
    user_input = relationship("UserInput", back_populates="physical")

class Mental(Base):
    __tablename__ = 'mental'
    
    id = Column(Integer, primary_key=True)
    selected_date = Column(String, ForeignKey('user_input.selected_date'))
    piano = Column(Boolean)
    breath = Column(Boolean)
    cold = Column(Boolean)
    gardening = Column(Boolean)
    wank = Column(Boolean)  # Add a new column for "wank"
    
    user_input = relationship("UserInput", back_populates="mental")

class Medical(Base):
    __tablename__ = 'medical'
    
    id = Column(Integer, primary_key=True)
    selected_date = Column(String, ForeignKey('user_input.selected_date'))
    cannabis_oil = Column(Boolean)
    cannabis_vape = Column(Boolean)
    cannabis_flower = Column(Boolean)
    ashwagandha = Column(Boolean)
    cbd_oil = Column(Boolean)
    cbd_vape = Column(Boolean)
    lions_mane = Column(Boolean)
    psilocybin = Column(Boolean)
    liver = Column(Boolean)
    probiotics = Column(Boolean)
    stressmush = Column(Boolean)
    
    user_input = relationship("UserInput", back_populates="medical")

class Checklist(Base):
    __tablename__ = 'checklist'
    
    id = Column(Integer, primary_key=True)
    selected_date = Column(String, ForeignKey('user_input.selected_date'))
    
    mood = Column(Integer)          # Mood level as integer
    sleep = Column(Integer)         # Sleep quality/quantity as integer
    stress = Column(Integer)        # Stress level as integer
    inflammation = Column(Integer)  # Inflammation level as integer
    energy = Column(Integer)        # Energy level as integer
    headache = Column(Integer)      # Headache severity as integer
    stool = Column(Integer)         # Stool quality/quantity as integer
    back_pain = Column(Integer)     # Back pain severity as integer
    screen_time = Column(Integer)   # Screen time as integer

    
    user_input = relationship("UserInput", back_populates="checklist")

# Create the database engine
engine = create_engine('sqlite:///bayesian_life.db')
Base.metadata.create_all(engine)
