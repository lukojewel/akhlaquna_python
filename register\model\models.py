from datetime import datetime
from sqlalchemy import LargeBinary 
from sqlalchemy import create_engine, Column, Integer, SmallInteger, String, ForeignKey, Boolean, DateTime, Date, Table, or_, and_, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from config.config import *
from passlib import hash

# Create a DBAPI connection
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# Declare an instance of the Base class for mapping tables
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    fname = Column(String(100))
    mname = Column(String(100))
    lname = Column(String(100))
    qatar_id = Column(String(100))
    password = Column(String(50))
    active = Column(Boolean(), default=False)
    createdAt = Column(DateTime(), default=datetime.now)
    updatedAt = Column(DateTime(), default=datetime.now)
    mobile = Column(String(50))
    # profile_desc = Column(String(1000))
    # school = Column(String(100))
    # profile_pic_url = Column(String(250))
    # contact_details = Column(String(500))
    # # what_you_do = Column(String(100))
    # where_you_do = Column(String(150))
    # modified = Column(DateTime())
    # current_city = Column(String(100))
    # hometown = Column(String(100))
    # main_skill = Column(String(100))
    # about = Column(String(1200))
    # website = Column(String(50))
    # address = Column(String(250))
    # cover_photo_url = Column(String(100))
    # mongo_id=Column(String(30))
    # bio = Column(String(150))
    # social_fb_link = Column(String(100))
    # social_twitter_link = Column(String(100))
    # social_linkedin_link = Column(String(100))
    # social_yt_link = Column(String(100))
    # social_behance_link = Column(String(100))
    # one_signal_id = Column(String(100))


    def __init__(self, email, first_name, middle_name, last_name, qf_id, active, mobile):
        print ('Inside user __init__')
        self.fname = first_name
        self.mname = middle_name
        self.lname = last_name
        self.mobile = mobile
        self.email = email
        self.qatar_id = qf_id
        self.createdAt = datetime.now()
        # self.password = hash.pbkdf2_sha512.encrypt(password)
        # self.gender = gender
        self.active = active
        # self.date_of_birth = date_of_birth
        # self.mongo_id = mongo_id
        # self.profile_pic_url = profile_pic_url
        # self.interests = interests
        # self.what_you_do = what_you_do
        # self.where_you_do = where_you_do
        # self.modified = modified
        # self.current_city = current_city
        # self.hometown = hometown
        # self.main_skill = main_skill
        # self.about = about
        # self.website = website
        # self.address = address
        # self.cover_photo_url = cover_photo_url

#OTP table
class Otp(Base):
    __tablename__ = 'otp'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    otp = Column(Integer)
    otp_type = Column(SmallInteger, default=0)
    attempt = Column(SmallInteger, default=0)
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime());
    send = Column(SmallInteger, default=0)

    user = relationship("User")

    def __init__(self, user_id,otp,otp_type):
        self.user_id = user_id
        self.otp = otp
        self.otp_type = otp_type


class TokenManager(Base):
    __tablename__ = "token_manager"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    created = Column(DateTime(), default=datetime.now)
    user_type = Column(SmallInteger, default=0)
    #user = relationship("User", back_populates="token_manager")
    
    def __init__(self, user_id,created,user_type):
        self.user_id = user_id
        self.created = created
        self.user_type = user_type
        
#Saltkey generator table 
class Saltkey(Base):
    __tablename__ = "saltkey"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    key = Column(LargeBinary)

    def __init__(self, user_id,key):
        self.user_id = user_id
        self.key = key

class Submission(Base):
    __tablename__ = "submission"
    id = Column(Integer,primary_key=True)
    short_description = Column(String(500))
    file_urls = Column(String(1500))
    no_of_votes = Column(Integer, default=0)
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime());
    candidate_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self,short_description, file_urls, candidate_id ):
        self.short_description = short_description
        self.file_urls = file_urls
        self.candidate_id = candidate_id

        
session.commit()
# Close the connection
engine.dispose()