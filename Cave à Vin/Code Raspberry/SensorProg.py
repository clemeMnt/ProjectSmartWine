import RPi.GPIO as GPIO;
from time import sleep,strftime, localtime,time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import Adafruit_DHT as DHT

# Use a service account
cred = credentials.Certificate('/home/pi/Desktop/smartwine.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def setup():
    #Configuration PI-PIN en input
    PIN_DHT21=4
    # Setup Raspberry input, ouptut
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_DHT21, GPIO.IN)

    return (PIN_DHT21)

    
def verification(doc_ref,i):
    index = doc_ref.collection(u'sensor').document(str(i)).get()
    if index.exists:
        return True
    else:
        return False
        
def to_infinity(find):
    index = find
    while True:
        yield index
        index += 1
        
def to_infini():
    index = 0
    while True:
        yield index
        index += 1

def find_index(doc_ref):
    for i in to_infini() :    
        index = doc_ref.collection(u'sensor').document(str(i)).get()
        if index.exists:
            i = i + 1
        else:
            return i
        
    
def write(db,PIN_DHT21):
    doc_ref = db.collection(u'Cave').document(str(1))
    find = find_index(doc_ref)
    
    for find in to_infinity(find):
        humid, temp = DHT.read_retry(DHT.DHT22, PIN_DHT21)
        today = strftime("%a, %d %b %Y %H:%M:%S ", localtime())
        doc_ref = db.collection(u'Cave').document(str(1))
        doc_ref = doc_ref .collection(u'sensor').document(str(find))
        doc_ref.set({
        u'temp': round(temp,3),
        u'humi': round(humid,2),
        u'date': today
        })
        
        sleep(50)

PIN_DHT21 = setup()
write(db,PIN_DHT21)

