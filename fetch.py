import smtplib
import time
import urllib
import urllib2
from bs4 import BeautifulSoup

# fill in with your gmail credentials
gmail_user = 'xxxx'
gmail_password = 'xxxx'

# Who is it addressed to
to = ['xxxx']

# dd/mm/yyyy
time = (time.strftime("%d/%m/%Y"))
# change to whatever
job_type = 'System Administration'

# Generates an Indeed GET
def get_indeed_request(url):

    # params for indeed GET request
    params = {
        'q': "Systems Administrator",   # Job title
        'l': "Seattle",                 # Location
        'explvl': "entry_level",        # Exp level
        'limit': '50',                  # Job limit
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
    mydivs = soup.findAll("div", {"class": "row"})

    # Storage for data
    data = {}


    # Goes though every element in mydivs soup and get the a text
    prefix = "indeed.com/"
    for element in mydivs:
        data[element.a.get_text(), prefix + mydivs[0].a["href"]] = {}
        # Also need the location as well as the url to the job
    return data

# get the soup data and pass in the html
data = get_soup(html)

def get_formatted_str(data):

    # Simply goes through each tuple list item and turns it into a single list
    return ["%s %s" % x for x in data]

# New variable for the formatted string - pass in soup data
job_string = get_formatted_str(data)

# Turns list into string and strips jobs that are irrelevant
def strip_garbage(data):
    my_val = []
    vars = job_type.split(" ")
    for i in data:
        if vars[0] in i:
            my_val.append(i)
    return my_val

# Format the data string for emailing
data = strip_garbage(job_string)
# Send an email to myself
def send_mail():
    myStr = '\n'.join(data)
    # Generate a message to send via email
    msg = "\r\n".join([
        "From: Fetch Bot",
        "To: mattwen@uw.edu",
        # Inlude url and location later
        "Subject: {} jobs for Matt {}".format(job_type, time),
        "",
        "Here are your jobs: \n{}".format(myStr)
    ])
    try:
        # Attempt to send an email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        # login with credentials
        server.login(gmail_user, gmail_password)
        # sendmail requires from, to, and message content in that order
        server.sendmail(gmail_user, to, msg)
        server.close()

        print 'Email sent!'
    except:
        print 'Something went wrong...'
# Send the mail
send_mail()
