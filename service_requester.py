from imp import IndustryMarketplace
import pprint
import sys

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

            if price >10:
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


if __name__ == '__main__':

    imp = ServiceRequester()
    
    # Either run it as a listeing service
    if len(sys.argv) == 1:
        imp.listen()
    


    # Our application is a mobility as a service so get from operations.json is "id":"0173-1#01-AAI711#001"
    if len(sys.argv) == 2 and sys.argv[1] == 'request_transportvehicle':
        print("here")
    # Get the eclass values and set it accordingly from the event details (from firebase web-app)
        values = {
            #starting point [lat, long]
            "0173-1#02-BAF163#002": '54.4321, 4.5210',

            #destination [lat, long]
            "0173-1#02-AAO631#002": '54.4321, 4.5210',

            #number of people to transport
            "0173-1#02-AAI711#001": 34,

            "0173-1#02-AAX711#001":True,

            #total price to transport the people
            "0173-1#02-AAB711#001": 500,

        }

        #here use the irdi for mobility as a service
        ret = imp.cfp(irdi='0173-1#01-AAI711#001', values=values, location='54.321, 4.123')
    #pprint.pprint(ret)
  

    if len(sys.argv) == 2 and sys.argv[1] == 'request_drone':

        values = {
            #weight
            '0173-1#02-AAJ336#002': 10,
            #start lat and long
            '0173-1#02-BAF163#002': '54.1234, 4.3210',
            #destination lat and long
            '0173-1#02-AAO631#002': '54.4321, 4.5210',
        }

        ret = imp.cfp(irdi='0173-1#01-AAJ336#002', values=values, location='54.321, 4.123')
        #pprint.pprint(ret)
    
    if len(sys.argv) == 2 and sys.argv[1] == 'drone_inspection':

        values = {
            '0173-1#02-AAP788#001': 2,
            '0173-1#02-AAY979#001': 10,
            '0173-1#02-BAF163#002': '54.4321, 4.5210',
        }

        ret = imp.cfp(irdi='0173-1#01-AAP788#001', values=values, location='54.321, 4.123')
        pprint.pprint(ret)
