from sparkpost import SparkPost
from config.config import  SPARK_POST_API_KEY, SENDGRID_API_KEY
from component.templating import render_template
from random import randint
import sendgrid

sparky = SparkPost(SPARK_POST_API_KEY)
html_files = {
                'account-activation': 'Activation.html',
            }

def sendSparkPostMail(template_name, email, subject, argument_dictionary,attachments=[{}]):
    file_location = 'view/mail/' + html_files[template_name]
    with open(file_location, 'r') as content_file:
        content = content_file.read()

    rendered_html_data = render_template(content, argument_dictionary)

    return send_mail_sendgrid(email, subject, rendered_html_data)
    return final_sparkpostmail(template_name, email, subject, rendered_html_data, attachments)

def final_sparkpostmail(template_name, email, subject, rendered_html_data,attachments=[{}]):
    response = sparky.transmissions.send(
        recipients=[email],
        #cc=[EVOQUE_EMAIL],
        html=rendered_html_data,
        # html=content,
        # text='Hello {{name}}',
        from_email='Akhlaquna Award<support@email.teamevoque.com>',
        subject=subject,
        campaign=template_name,
        track_opens=True,
        track_clicks=True,
        #use_sandbox=False
        # substitution_data=argument_dictionary
            )
    print("response", response)
    return response

def send_mail_sendgrid(email, subject, rendered_html_data):
    sg = sendgrid.SendGridClient(SENDGRID_API_KEY)
    print(email, subject)

    try:
        client = sendgrid.SendGridClient(SENDGRID_API_KEY)
        print('client-->', client)
        message = sendgrid.Mail()
        message.add_to(email['address']['email'])
        message.set_from("support@email.teamevoque.com")
        message.set_subject(subject)
        message.set_html(rendered_html_data)
        print(client.send(message))
        return True
    except Exception as e:
        print('ERROR IN First-->', str(e))