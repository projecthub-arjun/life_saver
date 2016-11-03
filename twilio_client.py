# Twilio is the 3rd party service used to make
# phone calls and send messages
from twilio.rest import TwilioRestClient

# Library used for handling dates
from datetime import datetime

# Library for using delay
import time

# Class to handle accident detection and notification
class Twilio:
    def __init__(self):
        # Twilio account details
        self.account_sid = "AC179d47f10d3fef703f8641c25c531949"
        self.auth_token  = "1fb6b1ae73df64220f9817c882a18df1"
        self.account_phone_number =  "+15108170384"
        self.call_pickup_url = "http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient"
        self.call_ring_timeout_s = 20
        self.failed_recipient_list = list()
        self.recipient_list = list()
        self.total_recipients = 10
        self.utc_start_time = datetime.utcnow()

        # Create the twilio client that will communicate
        # with the twilio server
        self.twilio_client = TwilioRestClient(self.account_sid, self.auth_token)
        self.get_broadcast_list()

    # Get the list of registered phone numbers from the server
    def get_broadcast_list(self):
        caller_ids = self.twilio_client.caller_ids.list()

        for caller_id in self.twilio_client.caller_ids.iter():
            phone_number = '+' + str(caller_id.friendly_name)
            if phone_number not in self.recipient_list:
                self.recipient_list.append(phone_number)

        self.total_recipients = len(self.recipient_list)

        return self.recipient_list

    def broadcast_emergency_message(self, message):
        for phone_number in self.recipient_list:
            print 'Sending SMS ', phone_number
            self.twilio_client.messages.create(to = phone_number, from_ = self.account_phone_number, body = message)
            time.sleep(1)

    def broadcast_emergency_call(self):
        self.utc_start_time = datetime.utcnow()
        self.call_status = dict()
        for phone_number in self.recipient_list:
            print 'Calling ', phone_number
            self.twilio_client.calls.create(to = phone_number, from_= self.account_phone_number, url= self.call_pickup_url, timeout = self.call_ring_timeout_s)
            time.sleep(2)
            self.call_status[phone_number] = "queued"

        return self.call_status

    def update_call_status(self):
        del self.failed_recipient_list[:]
        for call_log in self.twilio_client.calls.list(started_after = self.utc_start_time, PageSize = self.total_recipients):
            if(self.utc_start_time < datetime.strptime(call_log.start_time.split(" +")[0], "%a, %d %b %Y %H:%M:%S")):
                if(call_log.to_formatted in self.call_status):
                    self.call_status[call_log.to_formatted] = str(call_log.status)
                if((call_log.status != "completed") and (call_log.to_formatted not in self.failed_recipient_list)):
                    self.failed_recipient_list.append(call_log.to_formatted)
                print(" To: " + call_log.to_formatted + " Status: " + call_log.status + " Start Time: " + call_log.start_time.split(" +")[0])
        return self.failed_recipient_list

# Function to broadcast emergency calls and message,
# this will try to broadcast the calls until it is
# picked up by the user
def broadcast_emergency(twilio_client, message):
    twilio_client.broadcast_emergency_message(message)
    twilio_client.broadcast_emergency_call()
    retry_failed_calls = True
    while(retry_failed_calls):
        time.sleep(30)
        failed_recipient_list = twilio_client.update_call_status()
        if failed_recipient_list:
            print 'Retrying Calls', failed_recipient_list
            twilio_client.broadcast_emergency_call()
        else:
            break;

def main():
    twilio_client = Twilio()
    broadcast_emergency(twilio_client, "Test")

# Start of execution
if __name__ == '__main__':
    main()
