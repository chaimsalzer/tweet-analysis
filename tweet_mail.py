import smtplib
import datetime
today = str(datetime.date.today())


def tweet_mail():
    sender = "chaim@birkon.net"
    receivers = ["chaimsalzer@gmail.com"]
    message = """From: Chaim <chaim@birkon.net>
    To: Chaim <chaimsalzer@gmail.com>
    MIME-Version: 1.0
    Content-type: text/html
    Subject: Tweets collected for %s

    Tweets for %s successfully collected
    """ % (today, today)
    try:
        print("sending message: " + message)
        with smtplib.SMTP('birkon.ipage.com', 587) as session:
            session.login("chaim@birkon.net", "Hila6137")
            session.sendmail(sender, receivers, message)
        print("message sent")
    except smtplib.SMTPException:
        print("could not send mail")



