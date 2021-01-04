import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import RPi.GPIO as GPIO;
import threading
from time import sleep,strftime, localtime,time


def setup():
    #Configuration PI-PIN en input
    PIN_LED = [17, 27, 22, 10, 9, 11]
    PIN_SWITCH = [18, 23, 24, 25, 7, 8]

    # Setup Raspberry input, ouptut
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in range (6):
        GPIO.setup(PIN_LED[i], GPIO.OUT)
        GPIO.setup(PIN_SWITCH[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)  
    return (PIN_LED,PIN_SWITCH)

# Use a service account
cred = credentials.Certificate('/home/pi/Desktop/smartwine.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
callback_done = threading.Event()

def state(PIN_SWITCH):
    for i in range (1,7):
        statebutton =  GPIO.input(PIN_SWITCH[i-1])
        if statebutton == 1 :
            doc_ref = db.collection(u'Cave').document(str(1))
            doc_ref.collection(u'cellar').document(str(i)).update({u'buttonState': True})
        elif statebutton == 0 : 
            doc_ref = db.collection(u'Cave').document(str(1))
            doc_ref.collection(u'cellar').document(str(i)).update({u'buttonState': False})
            
            
def main(PIN_LED,PIN_SWITCH):
    statebutton = []
    detectbottle = []
    
    state(PIN_SWITCH)
    
    doc_ref = db.collection(u'Cave').document(str(1))
    doc_ref = doc_ref.collection(u'cellar').stream()       
        
    for doc in doc_ref:
        add_S = [doc.get("buttonState"), doc.id]
        add_B = [doc.get("detect"), doc.id]
        statebutton.append(add_S)
        detectbottle.append(add_B)

    for i in range (0, len(statebutton)):
        if statebutton[i][0] == True and detectbottle[i][0] == False : 
            GPIO.output(PIN_LED[i],GPIO.HIGH)
            
        elif statebutton[i][0] == True and detectbottle[i][0] == True :
            
            GPIO.output(PIN_LED[i],GPIO.LOW)
            sleep(0.5)
            GPIO.output(PIN_LED[i],GPIO.HIGH)
            sleep(0.5)
            state(PIN_SWITCH)
            
        elif statebutton[i][0] == False and detectbottle[i][0] == False :
             GPIO.output(PIN_LED[i],GPIO.LOW)
            
        elif statebutton[i][0] == False and detectbottle[i][0] == True :
            GPIO.output(PIN_LED[i],GPIO.LOW)
            doc_ref = db.collection(u'Cave').document(str(1))
            doc_ref.collection(u'cellar').document(str(i+1)).update({u'detect': False})
                     
        
(PIN_LED,PIN_SWITCH) = setup()
while True :
    main(PIN_LED,PIN_SWITCH)
        
