from tkinter import *
import facebook
import time
from datetime import date
from datetime import datetime
import json
from imp import IndustryMarketplace
import pprint
import sys
token= 'EAAJxG8jnEtEBAI7kTjSQOyz5PMGNzPhvHe4DRQO4Q9dk397kVliL1smvaflOBgZBFJcfOKc0nmHsnd2kFw2v9moKDSAULfAjX4piMBZAwnBNhkHx64UoVQBbAaoZCnMK4KUfpwfhSsELY0zzllDpnOJmrYv9IZCiD64rIKJYTQsTJCKNUhke'
#graph = facebook.GraphAPI(access_token=token, version="3.1")
#events = graph.request('/search?q=Poetry&type=event&limit=10000')
#eventList = events['data']
eventid = ' '
status = ''
attenders_count=0
start_time=0
latitude=0
longitude=0
total_budget =0

#884445061979027
class ServiceRequester(IndustryMarketplace):
    name = 'Event Manager'
    service_provider = False
    fund_wallet = True
    gps_coords = '54.000, 4.000'

    endpoint = 'http://localhost:4000'
    
    def on_proposal(self, data, irdi, submodels):
        '''
        Accept only if the price is between 5 and 15
        '''
        self.log('on proposal called!')
        try:
            price = self.get_price(irdi, submodels)
            self.log('Received proposal for %si for irdi %s' % (price, irdi))
            if not price:
                self.log('Price not found, submodels: %s' % submodels)

            if price >0:
                self.log('Accepting proposal')
                self.accept_proposal(data)
            else:
                self.log('Rejecting proposal')
                self.reject_proposal(data)

                
        except Exception as e:
            self.log('Error on accepting: %s' % e)

    def on_inform_confirm(self, data, irdi, submodels):
        self.log('Offer confirmed, time to pay')
        self.inform_payment(data)


def addEvent():
    #get inputs
    #here we get event ID
    input_1=eventID.get()
    input_2=eventName.get()
    input_3=sendProposal.get()
    input_4=budgetPerson.get()
    #start the search for event based on eventid from result
    graph = facebook.GraphAPI(access_token=token, version="3.1")
    #use input_1 (eventID) to search event using Graph API Facebook
    event = graph.get_object(id=input_1,
    fields='start_time,attending_count,place')
    #Store the event objects from Graph API into the respective fields
    global attenders_count
    attenders_count = event['attending_count']
    start_time = event['start_time']
    global latitude
    latitude = event['place']['location']['latitude']
    global longitude
    longitude = event['place']['location']['longitude']
    #total iota budget for all attendees    
    global total_budget
    total_budget = attenders_count*int(input_4)
    #date of event
    start_time = start_time[:10]
    date_event = datetime.strptime(start_time,'%Y-%m-%d').date()
    #days before event to send proposal
    days_sendProposal = int(input_3)
    #comparison of dates to send the proposal
    difference = date_event - date.today()
    if(difference.days <= days_sendProposal):
        global status
        status = "PROPOSAL SENT"
    else:
        status = "PROPOSAL NOT SENT"

    """ This is our reference for the application
    "name": "Mobility as a service",
    "description": "A manned or autonomous vehicle is requested to transport a given number of persons from A to B",
    "id":"0173-1#01-AAI711#001"
    """
    display_name = Label(window, text=input_2 + " Event Details",width=40,anchor=W, justify=LEFT, pady=20)
    display_eventID= Label(window, text="Event ID: " + input_1,width =40,anchor=W, justify=LEFT)
    display_sendProposal= Label(window, text="Days before event to send proposal: " +input_3 +" days",width=40, anchor=W,justify=LEFT)
    display_eventDate = Label(window, text="Date of Event: " +start_time ,width=40, anchor=W,justify=LEFT)
    display_budgetPerson = Label(window, text="IOTA budget per person: "+input_4,width=40,anchor=W, justify=LEFT)
    display_personCount = Label(window, text="Total Attendees: "+str(attenders_count),width=40,anchor=W, justify=LEFT)
    display_totalBudget = Label(window, text="Total IOTA budget: "+str(total_budget),width=40,anchor=W, justify=LEFT)
    display_latitude = Label(window, text="Latitude: "+str(latitude),width=40,anchor=W, justify=LEFT)
    display_longitude = Label(window, text="Longitude: "+str(longitude),width=40,anchor=W, justify=LEFT)

    #status details of proposal
    display_status = Label(window, text=status,width=40,anchor=W, justify=LEFT)
    display_status.place(x=530, y=315)

    #display placement
    display_name.grid(column=0, row=4)
    display_eventID.grid(column=0, row=5)
    display_sendProposal.grid(column=0, row=6)
    display_eventDate.grid(column=0, row=7) 
    display_budgetPerson.grid(column=0, row=8)
    display_personCount.grid(column=0, row=9)
    display_totalBudget.grid(column=0, row = 10)
    display_latitude.grid(column=0, row = 11)
    display_longitude.grid(column=0, row = 12)


window = Tk()

window.title("Event Transport Logistics Manager")

window.geometry('800x500')


# Initial Fields User has to input, with the most important being the Event ID which Facebook Graph API uses
get_eventID = Label(window, text="Event ID:",width=40,anchor=W, justify=LEFT, pady=10)
get_eventName = Label(window, text="Event Name:",width =40,anchor=W, justify=LEFT, pady=10)
get_sendProposal= Label(window, text="Days before event to send proposal:",width=40, anchor=W,justify=LEFT, pady=10)
get_budgetPerson = Label(window, text="IOTA budget per person:",width=40,anchor=W, justify=LEFT, pady=10)

get_eventID.grid(column=0, row=0)
get_eventName.grid(column=0, row=1)
get_sendProposal.grid(column=0, row=2)
get_budgetPerson.grid(column=0, row=3)

eventID = Entry(window,width=20)
eventName = Entry(window,width=20)
sendProposal = Entry(window,width=20)
budgetPerson = Entry(window,width=20)

eventID.grid(column=1, row=0)
eventName.grid(column=1, row=1)
sendProposal.grid(column=1, row=2)
budgetPerson.grid(column=1, row=3)


addevent_button= Button(window, text="Add Event", command=addEvent)

addevent_button.grid(column=2, row=2, padx=60)

def iota_task():
    imp = ServiceRequester()
    global status
    if status == "PROPOSAL SENT":
        print("Sending request proposal...")
         # Get the eclass values from eclass.json
        values = {
            #starting point [lat, long] assume everyone is to be picked up at this point
            "0173-1#02-BAF163#002": '54.4321, 4.5210',

            #destination [lat, long]. get latitude and longitude from python app input
            "0173-1#02-AAO631#002": str(latitude) + ", " + str(longitude),

            #number of people to transport
            "0173-1#02-AAI711#001": attenders_count,

            #autonomous or not
            "0173-1#02-AAX711#001":True,

            #total price to transport the people. get total_budget from python app input
            "0173-1#02-AAB711#001": total_budget,

        }

        #here use the irdi for mobility as a service
        ret = imp.cfp(irdi='0173-1#01-AAI711#001', values=values, location='54.321, 4.123')
        pprint.pprint(ret)
        status = ""
    else:
        print("No proposals...")
    window.after(10000, iota_task) 


if __name__ == '__main__':
   
    window.after(10000, iota_task)
    window.mainloop()
        