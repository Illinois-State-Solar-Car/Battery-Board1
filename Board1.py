import board
import digitalio
import time
#from adafruit_mcp2515       import MCP2515 as CAN
#from adafruit_mcp2515.canio import RemoteTransmissionRequest, Message, Match, Timer
import busio
import struct



               
def shitfuck():
    
    while True:
        
        print("hey........")
        strobe.value = 1
        time.sleep(1)
        strobe.value = 0
        time.sleep(1)

spi = busio.SPI(board.GP2, board.GP3, board.GP4)


#can_cs = digitalio.DigitalInOut(board.GP9)
#can_cs.switch_to_output()
#mcp = CAN(spi, can_cs, baudrate = 500000, crystal_freq = 16000000, silent = False,loopback = False)


current = -1
lowTemp = 20
highTemp = 20
avgTemp = 20
#Mike's fancy led
#Everbody like's blinky lights
led = digitalio.DigitalInOut(board.GP18)
led.direction = digitalio.Direction.OUTPUT

#Define Relays
motor_relay      = digitalio.DigitalInOut(board.GP22)
ground_relay     = digitalio.DigitalInOut(board.GP23)
precharge_relay  = digitalio.DigitalInOut(board.GP24)
power_tracker    = digitalio.DigitalInOut(board.GP21)

strobe           = digitalio.DigitalInOut(board.GP25)
#Set Relays to be outputs
motor_relay.direction              = digitalio.Direction.OUTPUT
ground_relay.direction             = digitalio.Direction.OUTPUT
precharge_relay.direction          = digitalio.Direction.OUTPUT
power_tracker.direction            = digitalio.Direction.OUTPUT

strobe.direction                   = digitalio.Direction.OUTPUT
#Input data pins
#charge_enable       = digitalio.DigitalInOut(board.A3)
discharge_enable    = digitalio.DigitalInOut(board.GP20)
kill_car            = digitalio.DigitalInOut(board.GP19)
charge_car          = digitalio.DigitalInOut(board.GP10)

#Set input data pins to be 
#charge_enable.switch_to_input(      pull=digitalio.Pull.DOWN)
discharge_enable.switch_to_input(   pull=digitalio.Pull.DOWN)
kill_car.switch_to_input(           pull=digitalio.Pull.DOWN)
charge_car.switch_to_input(         pull=digitalio.Pull.DOWN)

#Why is this here? well idk but it's in the doccumentation  https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut.switch_to_input
#charge_enable.pull      = digitalio.Pull.DOWN
discharge_enable.pull   = digitalio.Pull.DOWN
kill_car.pull           = digitalio.Pull.DOWN
charge_car.pull         = digitalio.Pull.DOWN

#A silly function that is essentally a phat pause
#But it makes an led blink at 5Hz ;) 
def pause_but_blink(sleep_time:float):
    
    global led      
    sTime = time.time()
    while time.time() - sTime <= sleep_time:
        if (charge_car.value or  discharge_enable.value or kill_car.value or charge_car.value):
            
            
        
            ground_relay.value         = False
            precharge_relay.value      = False
            motor_relay.value          = False
            power_tracker.value        = False
            if (discharge_enable.value or kill_car.value):
                
                shitfuck()
                print("\nhelp\n")
                sleep_time = 100000000
            if (charge_car.value):
                while True:
                    print("ShitFuck 2: Eletric Boogaloo")
            
        led.value = not led.value
        time.sleep(0.2)

#Define a flag that is TRUE if the car has been started
started_car                = False

# make sure everything is initially off to start,
ground_relay.value         = False
precharge_relay.value      = False
motor_relay.value          = False
power_tracker.value        = False
 




'''
-----------------------------------------------------
-----------------------------------------------------
This is where the car actually runs!
'''
print(kill_car.value)
#print(charge_enable.value)
print(charge_car.value)



#If BMS say we are good to charge and we haven't started the car yet
while not started_car:
    
    
    print("discharge_en: ",discharge_enable.value)
    print("kill: ",kill_car.value)
    print("charge: ",charge_car.value)
    
    if (not discharge_enable.value and not kill_car.value and not charge_car.value) and not started_car:
        """
        print("hi")
        print(kill_car.value)
        print(charge_enable.value)
        print(charge_car.value)
        """
        #Turn on the precharge relays
        ground_relay.value      = True
        precharge_relay.value   = True
        power_tracker.value     = True
            
        #Wait 5sec for precharge
        pause_but_blink(5.0)
        motor_relay.value = True
                                                    
        #now turn on shane, i mean the relay <------<         # | 
                                                       # | 
        #wait again 1sec for saftey                  |   
        pause_but_blink(1.0)                       # |    
        #LOL-----------------------------------------^
        precharge_relay.value  = False
            
            
            
        #Set the bool to TRUE to show the car has been started 
        started_car = True
        
        pause_but_blink(.2)



    time.sleep(0.2)


while started_car:
     
    if((discharge_enable.value or kill_car.value or charge_car.value) !=0):

        ground_relay.value     = False
        power_tracker.value    = False
        motor_relay.value      = False
        precharge_relay.value  = False
        
        
        while True:
            pause_but_blink(.75)
            #strobe.toggle()
            print(discharge_enable.value," = discharge enable")
            print(kill_car.value, " = kill switch "  , charge_car.value, " = on/off  " )
    
    
    print("Power Trackers: "+str(power_tracker.value))
    pause_but_blink(.02)
    
