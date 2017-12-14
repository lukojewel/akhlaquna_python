import os
import json
import string
import re
from model.models import *
from component.otp import generate_otp
from config.config import WEBSITE_URL
from base64 import b64decode, b64encode
from component.email import send_email

json_data = json.loads(open(os.environ['req']).read())
email = json_data['email']
small_first_name = json_data['first_name']
first_name = string.capwords(small_first_name)
if 'middle_name' in json_data:
    small_middle_name = json_data['middle_name']
    middle_name = string.capwords(small_middle_name)
else:
    middle_name = ''
small_last_name = json_data['last_name']
last_name = string.capwords(small_last_name)
qatari_id = json_data['qatari_id']
mobile = json_data['mobile']
active = False

# already_registered = session.query(User).filter_by(email=email).first() or session.query(User).filter_by(mobile=mobile).first() or session.query(User).filter_by(qatar_id=qatari_id).first()
already_registered = False
print('already_registered-->',already_registered)
if(not already_registered):
    if re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):

        user = User(
            email=email, 
            first_name=first_name, 
            middle_name=middle_name, 
            last_name=last_name, 
            active=active, 
            mobile=mobile, 
            qf_id=qatari_id
            )
        try:
            session.add(user)
            session.commit()
            user = session.query(User).order_by(User.id.desc()).first()
            
            otp_type = 0
            otp = generate_otp(user.id, otp_type)
            session.commit()
            email = user.email
            encoded_data = email+':'+ str(otp) 
            encoded_data = b64encode(encoded_data.encode('utf-8'))
            encoded_data = str(encoded_data)
            encoded_data = encoded_data[2:-1]
            print(encoded_data)
            encoded_data = WEBSITE_URL + 'Login/'+encoded_data
            print(encoded_data)
            template_name = 'account-activation'
            subject = 'Account activation'
            argument_dictionary = {
                    'first_name': user.fname,
                    'last_name': user.lname,
                    'decode_data' : encoded_data
                }
            full_name = user.fname + ' ' + user.lname
            name_with_email = {'address': {'name': full_name, 'email': user.email}}
            mail_result = send_email(template_name, name_with_email, subject, argument_dictionary)
            print(mail_result)

            status = True
            message = 'You have been registered successfully. Activation Code has been sent to your registered email ID.'
        except Exception as e:
            print(str(e))
            session.rollback()
            status = False
            message = 'Something went wrong.'

            
        # res.status = falcon.HTTP_201
    else:
        status = False
        message = 'Invalid email address.'
else:
    status = False
    message = 'Already registered.'

body = json.dumps({'status': status, 'message': message})

response = open(os.environ['res'], 'w')
response.write(body)
response.close()