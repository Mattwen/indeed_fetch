import smtplib
import time
import urllib
import urllib2
from bs4 import BeautifulSoup

gmail_user = 'xxxx'
gmail_password = 'xxxx'

time = (time.strftime("%d/%m/%Y"))
job_type = 'System Administration'

sent_from = gmail_user
to = ['mattwen@uw.edu']
subject = 'OMG Super Important Message'
body = 'here is the info'

def get_indeed_request(url):

    # params for indeed GET request
    params = {
        'q': "Systems Administrator",   # Job title
        'l': "Seattle",                 # Location
        'explvl': "entry_level",        # Exp level
        'limit': '50',                  # Page limit
        'fromage': '7',                 # Post age
    }
    # Try a GET request
    try:
        # Encode the query paramaters
        query = urllib.urlencode(params)

        # Join the baseUrl with the query + params
        request = ''.join([url, query])

        # generate the reponse and read it
        response = urllib2.urlopen(request)
        the_page = response.read()
        # Returns html code
        return the_page

    # Could not resolve the url (404)
    except:
        print 'could not grab url'
# send_mail()
html = get_indeed_request('https://www.indeed.com/jobs?')

def get_soup(html):

    # Create soup with html
    soup = BeautifulSoup(html, 'html.parser')

    # Divide the soup html by Div row result happens to be the interesting class div
    mydivs = soup.findAll("div", {"class": "row result"})

    # Storage for data
    data = {}

    # Goes though every element in mydivs soup and get the a text
    for element in mydivs:
        data[element.a.get_text()] = {}
        # Also need the location as well as the url to the job
    return data

# get the soup data and pass in the html
data = get_soup(html)

# Format the data string for emailing
def get_formatted_str(data):
    job_string = ''

    # Simply goes trhough each list item and adds it to the string with a newline at the end.
    for job in data:
        job_string += job + '\n'
    return job_string

# New variable for the formatte string - pass in soup data
job_string = get_formatted_str(data)

# Send an email to myself
def send_mail():

    # Generate a message to send via email
    msg = "\r\n".join([
        "From: matt.wenger1024@gmail.com",
        "To: mattwen@uw.edu",
        # Inlude url and location later
        "Subject: {} jobs for Matt {}".format(job_type, time),
        "",
        "Here are your jobs: \n{}".format(job_string)
    ])
    try:
        # Attempt to send an email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        # login with credentials
        server.login(gmail_user, gmail_password)
        # sendmail requires from, to, and message content in that order
        server.sendmail(sent_from, to, msg)
        server.close()

        print 'Email sent!'
    except:
        print 'Something went wrong...'
# Send the mail
send_mail()