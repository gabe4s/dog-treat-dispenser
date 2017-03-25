import sys
import imaplib
import getpass
import email
from datetime import datetime
import time

SECONDS_TO_CHECK_EMAILS = 60

def dispenseTreat():
    print("Dispensing...")
    # Dispense Treat Here

def getNewEmailCount(mailbox):
    rv, data = mailbox.search(None, "Unseen", '(SUBJECT "Treat")')
    if rv != 'OK':
        print("No Messages In Folder")
        return 0
    newEmailCount = len(data[0].split())
    if(newEmailCount > 0):
        mailbox.store(data[0].replace(' ',','),'+FLAGS','\Seen')
    return newEmailCount

def loopForNewEmails(mailbox):
    while(1):
        rv, data = mailbox.select("Inbox")
        if rv == 'OK':
            print("=====Checking New Emails=====")
            print("-----" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "-----")
            newEmailCount = getNewEmailCount(mailbox)
            if(newEmailCount > 0):
                print("New Emails: " + str(newEmailCount))
                dispenseTreat()
            else:
                print("No New Emails")
            print("=============================")
        else:
            print("Failed To Get Mail")
        print("\nWaiting " + str(SECONDS_TO_CHECK_EMAILS) + " Seconds...\n")
        time.sleep(SECONDS_TO_CHECK_EMAILS)

def login(username, password):
    print("\nAttempting To Log In...")
    mailbox = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mailbox.login(username, password)
        print("Authentication Succeeded\n")
        return mailbox
    except imaplib.IMAP4.error:
        print("Authentication Failed\n")
        sys.exit(1)

def main():
    argc = len(sys.argv)
    if(argc < 3):
        print("Not Enough Arguments. Must Provide Username and Password.")
        sys.exit(1)
    username = sys.argv[1]
    password = sys.argv[2]
    mailbox = login(username, password)
    rv, data = mailbox.select("Inbox")
    if rv == 'OK':
        loopForNewEmails(mailbox)
    else:
        print("Mailbox Selecion Failed")
        mailbox.logout()
        sys.exit(1)

if __name__== "__main__":
    main()
