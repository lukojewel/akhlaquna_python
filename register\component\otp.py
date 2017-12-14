from model.models import *
from random import randint

def generate_otp(user_id, otp_type):
    otp = randint(100000, 999999)
    # Remove all old otp request data by user and then add it
    session.query(Otp).filter(and_(Otp.user_id == user_id, Otp.otp_type == otp_type)).delete()
    save_otp = Otp(user_id, otp, otp_type)
    session.add(save_otp)
    session.commit()
    return otp