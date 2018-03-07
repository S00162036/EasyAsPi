import RPi.GPIO as GPIO #imports library for pin control
import time #for time....
from CoinKNN1 import main as KnnDecideCoin #imports the knn from file in same dir

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

####-----setup IR Sensor-------
IRBreakSensorPin = 22#pin used for IR Sensor
GPIO.setup(IRBreakSensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
###---finished ir sensor setup

####------setup start button--------
StartButtonPin = 4#other end on ground
GPIO.setup(StartButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)#pull up ressistor
####----finish setup start button

####-----setup Vibrator-------
VibratorPin = 25#pin used for DC motor logic
GPIO.setup(VibratorPin, GPIO.OUT)
####----finish setup vibrator

###-----Stepper Setup---------
#stepper pins: a  b  c  d
stepperPins = [5,6,13,19]#pins used
#stepperPins = [27,17,23,24]#pins used(not used now)

#setup pins for stepper
for pin in stepperPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

#steps
seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1] ]

#set up vars
distPerStep = 0.052375 #mm/step
sleepTime = 0.001 #how long of breakes (normal = 0.001, fast = 0.0007)
####-----end of stepper setup-----

####------LoadCell Setup-------
#pins used for load cell
PinDT = 17
PinSCK = 27

#Vars
weightStartweightStartSample=0
WeightSum=0
WeightTemp=0
####------end of loadcell setup-----

####----functions to operate vibration unit----
def vibrateForASecond():#actually half a sec
    GPIO.output(VibratorPin, GPIO.HIGH)
    #print"motor on"
    time.sleep(.5)
    GPIO.output(VibratorPin, GPIO.LOW)
    #print"motor off"

###----end of vibration unit functions----

####----function to operate load gate------------------------
def MoveServoGateLoadcell():
    ####-----setup for load gate-----
    LoadGateStartPos = 5.3#startPosition for gate
    controlPinLoadGate = 23#pin used for laod gate servo
    GPIO.setup(controlPinLoadGate, GPIO.OUT)
    controlLoadGate = GPIO.PWM(controlPinLoadGate, 50)#fifty hertz
    controlLoadGate.start(LoadGateStartPos)#start
    ####---load gate setup finished----
    time.sleep(.2)#time to move
    LoadGateEndPos = 10
    #assume we are in starting position
    controlLoadGate.ChangeDutyCycle(LoadGateEndPos)#move to end position fast
    time.sleep(.5)#time to move

    #reset to start position
    controlLoadGate.ChangeDutyCycle(LoadGateStartPos)#move to end position fast
    time.sleep(.5)#time to move
    controlLoadGate.stop()#stops move

def MoveServoGateLoadcellToStart():
    LoadGateStartPos = 5.3#startPosition for gate
    controlPinLoadGate = 23#pin used for laod gate servo
    GPIO.setup(controlPinLoadGate, GPIO.OUT)
    controlLoadGate = GPIO.PWM(controlPinLoadGate, 50)#fifty hertz
    controlLoadGate.start(LoadGateStartPos)#start
    time.sleep(.2)#time to move
    controlLoadGate.stop()#stops move



#Stepper Functions----------------------------------------
def move(direction):#################moves one step
    #1 passed in for forward, -1 for back##

    stepsWanted = 1 * direction #works out which direction

    if int(stepsWanted) < 0: #minus no is entered
        seq.reverse()
        for i in range(-int(stepsWanted)):
            for halfStep in range(8):
                for pin in range(4):
                    GPIO.output(stepperPins[pin], seq[halfStep][pin])
                time.sleep(sleepTime)
        seq.reverse()


    else:#pos num entered
        for i in range(int(stepsWanted)):
            for halfStep in range(8):
                for pin in range(4):
                    GPIO.output(stepperPins[pin], seq[halfStep][pin])
                time.sleep(sleepTime)



#LoadCell Functions-----------------------------------------
#function to read data from HX711 chip
def readCount():
    i=0
    Count=0
    GPIO.setup(PinDT, GPIO.OUT)
    GPIO.output(PinDT,1)#set dt high
    GPIO.setup(PinSCK, GPIO.OUT)
    GPIO.output(PinSCK,0)
    GPIO.setup(PinDT, GPIO.IN)

    while GPIO.input(PinDT) == 1:
        i=0
    for i in range(24):#24 bits
        GPIO.output(PinSCK,1)
        Count=Count<<1#step through byte

        GPIO.output(PinSCK,0)
        #time.sleep(0.001)
        if GPIO.input(PinDT) == 0:
            Count=Count+1

    GPIO.output(PinSCK,1)
    Count=Count^0x800000
    GPIO.output(PinSCK, 0)
    return Count

#function to return a solid weight
def GetWeight():##not in use
    weightStartSample=0
    WeightSum=0
    WeightTemp=0

    keepChecking = 1
    while keepChecking:
        w=0
        WeightSum = 0
        for i in range(5):
            Count=readCount()
            w=(Count-weightStartSample)/800#ratio needed to get to one decimal place
            WeightSum=WeightSum+w
            time.sleep(0.05)
        WeightSum=(WeightSum/5)-1
            
        if WeightTemp == WeightSum:
            #print WeightSum,"dg"#decigram
            keepChecking = 0
            return WeightSum#-----
        time.sleep(0.1)
        WeightTemp = WeightSum


#wait until load detected
def WaitForLoad():
    load = 0
    #wait for coin
    load = readCount()/8000
    while load >= readCount()/8000:
        #load=load#waste time
        #print"waiting for load"
        pass  #this does nothing but allows us to have an empty loop
        

#Coin Functions-----------------------------------------
#figure out what coin by weight and height
def DecideCoin(height, weight):
    coin = 0.00
    #ignoring weight for now
    if height >= 19.9 and height <= 21.0 and weight >= 10100 and weight <= 10200:
        coin =2.0
    elif height >= 15.0 and height <= 16.0 and weight >= 10130 and weight <= 10160:
        coin =1.0
    #elif height >= 22.8 and height <= 23.1:#---------------need a 50 measuremnt
        #coin =0.50
    return (coin)


#measure height and weight
def GetCoinHeightWeight():
    distanceMoved = 0
    stepsCount = 0#total steps
    coinHeight1 = 0
    coinWeight1 = 0
    load1 = 0
    
    coinWeight1 = GetWeight() #stores weight of coin    

    #measure height
    load1 = readCount()/8000
    while load1 >= readCount()/8000:
        #move stepper
        move(7)
        #print"move stepper"
        stepsCount = stepsCount+7
    #movement stopped
    print ("Load Detected!!!")
    #record steps taken
    distanceMoved = stepsCount * distPerStep
    coinHeight1 = rackDistFromCell - distanceMoved
    #dicide coin
    #display
    #print stepsCount," steps"
    #print distanceMoved," dist"
    #print coinWeight1," weight1"
    #print coinHeight1," height1"
    #move stepper back x amount of steps
    move(-stepsCount)
    return coinHeight1, coinWeight1
####------end of load cell functions

####----functions to operate Hopper gate----
def MoveServoGateHopperEject():
    # setup
    HopperGateStartPos = 10#startPosition for gate
    HopperGateEndPos = 5.3
    controlPinHopperGate = 24#pin used for laod gate servo
    GPIO.setup(controlPinHopperGate, GPIO.OUT)
    controlHopperGate = GPIO.PWM(controlPinHopperGate, 50)#fifty hertz
    controlHopperGate.start(HopperGateStartPos)#start
    time.sleep(.2)#time to move
    # setup finished

    #assume we are in starting position
    controlHopperGate.ChangeDutyCycle(HopperGateEndPos)#move to end position fast
    time.sleep(.6)#time to move#-------------------------------------------------------------this is very important----get as small as posible!!

    #reset to start position-------------------decided to remove this
    #controlHopperGate.ChangeDutyCycle(HopperGateStartPos)#move to end position fast
    #time.sleep(.5)#time to move
    
    controlHopperGate.stop()#stops move

#function moves hopper gate to start pos
def MoveServoGateHopperToStart():
    # setup
    HopperGateStartPos = 10#startPosition for gate
    controlPinHopperGate = 24#pin used for laod gate servo
    GPIO.setup(controlPinHopperGate, GPIO.OUT)
    controlHopperGate = GPIO.PWM(controlPinHopperGate, 50)#fifty hertz
    controlHopperGate.start(HopperGateStartPos)#start
    time.sleep(.45)#time to move
    # setup finished

    controlHopperGate.stop()#stops move
###----end of hopper gate functions----



####----functions to operate distrobution Hopper servo----
#function to move servo to selected coin possition
def MoveServoDistro(CoinValue):
    #CoinValue is expected to be a float with one euro displayed as 1.0 etc..
    #positions
    #end one=2, end two=12, difference=10, coinstypes to count=7
    DistroServoCoinMisc = 12
    DistroServoCoinFiveCent = 10.75
    DistroServoCoinTenCent = 9
    DistroServoCoinTwentyCent = 7.25
    DistroServoCoinFiftyCent = 5.5
    DistroServoCoinOneEuro = 3.75
    DistroServoCoinTwoEuro = 2
    # setup
    controlPinDistroServo = 18#pin used for Distro Servo
    GPIO.setup(controlPinDistroServo, GPIO.OUT)#configure as output
    controlDistro = GPIO.PWM(controlPinDistroServo, 50)#fifty hertz
    # setup finished
    
    # determine where to move based on coin
    if(CoinValue == 0.05):#five cent
        controlDistro.start(DistroServoCoinFiveCent)#Move to five cent position
    elif(CoinValue == 0.1):#ten cent
        controlDistro.start(DistroServoCoinTenCent)#Move to ten cent position#
    elif(CoinValue == 0.2):#twenty cent
        controlDistro.start(DistroServoCoinTwentyCent)#Move to twenty cent position
    elif(CoinValue == 0.5):#etc...
        controlDistro.start(DistroServoCoinFiftyCent)
    elif(CoinValue == 1.0):#etc...
        controlDistro.start(DistroServoCoinOneEuro)
    elif(CoinValue == 2.0):#etc...
        controlDistro.start(DistroServoCoinTwoEuro)
    else:
        controlDistro.start(DistroServoCoinMisc)        
        
    time.sleep(2)#time to move
    controlDistro.stop()#stops servo
###----end of distrobution Hopper servo functions----




####------------------------------------------ actual code -----------------------------------------------------
#vars for feeding coins
NoCoinsCount = 0 #var to store trys to vibrate a coin into position
waitAmountForCoins = 6 #how many times we test for no coins

#vars for  coin measurning 
coinHeight = 0
coinWeight = 0
rackDistFromCell = 30.0 #mm #when set up like this
currentCoin = 0.0
weightStartSample = readCount() #measure at empty load cell
StartButtonState = GPIO.input(StartButtonPin)#sees if button is pressed


#get gates in start position
MoveServoGateHopperToStart()
MoveServoGateLoadcellToStart()

try:#exit on Crtl+C
    
    while True:#loop to take all the coins
        while StartButtonState == True:#start Button not pressed
            StartButtonState = GPIO.input(StartButtonPin)#sees if button is pressed
        #loop through waiting for a coin
        while (GPIO.input(IRBreakSensorPin) == 1 and NoCoinsCount <= waitAmountForCoins):
            #vibrate------------------------------------------
            vibrateForASecond()#vibrates--
            print"i am vibrating"#for testing
            #time.sleep(1)#for tesing--
            NoCoinsCount+=1

        if NoCoinsCount <= waitAmountForCoins:
            #coin found
            weightStartSample = readCount() #measure at empty load cell------------ 
            NoCoinsCount = 0 #reset count
            MoveServoGateHopperEject()
            
            WaitForLoad()
            time.sleep(0.1)

            coinHeight, coinWeight = GetCoinHeightWeight()
            
            #--------------------------------------------------machine learning code 
            #currentCoin = DecideCoin(coinHeight, coinWeight)#testing function
            currentCoin = float(KnnDecideCoin(coinHeight, coinWeight))#knn machine learing
            
        

            
            print coinHeight," height"
            print coinWeight," weight"
            print currentCoin," coin"

            MoveServoDistro(currentCoin)#move distroHopper to position
            
            MoveServoGateLoadcell()#eject coin from loadCellHolder
            MoveServoGateHopperToStart()#return hopper gate to start
            #---------------------------------------------------------------maybe take weight sample here?
            
        else:
            #no more coins
            print "no more coins"
            break # exits the all coin while loop

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nquit")
    
GPIO.cleanup()
