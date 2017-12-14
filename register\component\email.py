from component.mailer import sendSparkPostMail
from threading import Thread
from config.config import *
from datetime import datetime
import time


def send_email(template_name, email, subject, argument_dictionary,attachments=[{}]):
    start_time = time.time()
    if attachments == [{}]:
        response = sendSparkPostMail(template_name, email, subject, argument_dictionary)
    else:
        response = sendSparkPostMail(template_name, email, subject, argument_dictionary, attachments)

    print(response)
    return response
    overhead = time.time() - start_time
    #logger.info("Email sent time in second = {}".format(overhead))


