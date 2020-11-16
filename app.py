from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from script import *        # main script to fetch links

app = Flask(__name__)
fallbackMessage = '''Currently only supports stuffs Like:
-> cats
-> dogs
-> memes
-> animals
-> art
-> photos
-> wow
-> walls
---------------------------------
Use: gib <number> <stuff you want>             
Will send you 5 wallpapers
---------------------------------'''

@app.route('/')     # just to test if server up and running
def helloWorld():
    return 'Hello, World'

@app.route('/stuffs', methods=['POST'])     # thing that handles request
def stuffs():
    incomingMessage = request.values.get('Body', '').lower().split(' ')
    response = MessagingResponse()

    if incomingMessage[0] == 'help':
        response.message(fallbackMessage)
        
    elif len(incomingMessage) != 3 or incomingMessage[0] != 'gib':
        response.message('Are you out of your mind?\nUse: gib <number> <stuff you want>')

    else:
        try:    # checking if the 2nd argument is number or not
            count = int(incomingMessage[1])
            dankStuffsLinks = gibMeDankStuff(count, incomingMessage[2])
            if len(dankStuffsLinks) == 0:   # if no links returned by script means 404
                response.message(fallbackMessage)
            else:
                for i in range(0, count):   # adding each link(image) to the response
                    response.message().media(dankStuffsLinks[i])

        except ValueError:
            response.message('Are you out of your mind?\nUse: gib <number> <stuff you want>')
    return str(response)    # sending the response (images or text)

if __name__ == '__main__':
    app.run()
