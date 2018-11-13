from bs4 import BeautifulSoup
import urllib
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class NewCar:

    def __init__(self, heading, cost, location, link):
        self.__heading = heading
        self.__cost = cost
        self.__pickup = pickup
        self.__link = link

    def isCheap(self, car2):
        if self.__cost > car2.__cost:
            return True
            print "Cheaper car has been located, new comparison commencing."
        else:
            return False
            print "Car is not cheaper, new comparison commencing."

    def cheaperContentWriter(self):
        fileContents = open("emailContents.txt", "w+")
        fileContents.write ("%s\n%f\n%s\n%s" % (self.__heading, self.__cost, self.__pickup, self.__link))
        fileContents.close() 

    def email (self):
        #make sure all emails are gmail for this program
        fromaddr = "" #Put the email you want the program to send FROM here.
        toaddr = ""  #Put the email you want the program to send TO here.
        password = "" #Put the password for the fromaddr email here.
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Cheaper car found!"
        body = "A cheaper car has been found! Please see attached Car, Cost, Pickup Location, and link to original advertisement:\nNEW CAR INFORMATION:\nCar: %s\nOverall Cost: %s\nPickup: %s \nLink: %s" % (self.__heading, self.__cost, self.__pickup, self.__link)
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print "Email sent!"
   
def contentReader():
    try:
        fileContents = open ("emailContents.txt", "r+")
        holder = []
        for line in fileContents:
            holder.append(line.strip())
        content = NewCar(holder[0], float(holder[1]), holder[2], holder[3])
        fileContents.close()
        return content
    except:
        content = NewCar("dummy", 9999999,"Dummy","Dummy")        
        return content


checkerVar = True
while checkerVar == True:
    r = urllib.urlopen('https://ottawa.craigslist.ca/search/cta').read()
    soup = BeautifulSoup(r, "html.parser")
    info = soup.p.a       
    results = soup.find_all('p', {'class' : 'result-info'})

    for soupResult in results:
            #find link
            link = (soupResult.find('a', {'class' : 'result-title hdrlnk'})).get('href')
            #find heading
            heading = (soupResult.find('a', {'class' : 'result-title hdrlnk'})).contents[0]
            #find pickup
            try:
                pickup = (soupResult.find('span', {'class' : 'result-hood'})).contents[0]
                pickup = pickup.strip()
                pickup = pickup.encode('ascii', 'ignore')     
            except:
                pickup = "No pickup Location"
            #find cost
            try:
                cost = (soupResult.find('span', {'class' : 'result-price'})).contents[0]
                cost = cost.strip()
                cost = list(cost.encode('utf-8'))
                newCost = ""
                for costs in range(len(cost)):
                    if cost[costs] != "$":
                        newCost = newCost + cost[costs]
                cost = float(newCost)
            except:
                cost = "No cost? Weird. Check description"
            checkingListing = NewCar(heading, cost, pickup, link)
            content = contentReader()
            if content.isCheap(checkingListing) == True:
                content = checkingListing
                content.cheaperContentWriter()
                content.email()    
