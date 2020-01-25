#alert process send a mail when a value goes higher than spected
import smtplib, ssl

"""def read_creds():
    user = passw = ""
    with open("configuration.txt", "r") as f:
        file = f.readlines()
        user = file[0].strip()
        passw = file[1].strip()

    return user, passw"""
#read credentials from confg file

def sendmail(qa):
    port = 465

    #sender, password = read_creds()
    sender = 'pylogger.by.roi@gmail.com'
    password = 'estaesunaclavemuysegura'
    recieve = 'pylogger.by.roi@gmail.com'

    while True:
        if not qa.empty():
            message = """\
            Subject: PYlogger Defense system

            WARNING! One of your sensors passed the limit\n 
            """+str(qa.get())+"""

            Contact information: +542616123311 -Roi
            """

            context = ssl.create_default_context()
            print('\n\n---------------------------------')
            print("\tSENDING ALERT")
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, recieve, message)

            print("\tALERT SENT!\n------------------------------")
