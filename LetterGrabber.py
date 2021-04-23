import utime
from servo import Servo
from machine import Pin, ADC

class Line(object):
    def __init__(self,sA,sB,eA,eB):
        self.sA = sA
        self.sB = sB
        self.eA = eA
        self.eB = eB

      
led=Pin(15,Pin.OUT)
s1 = Servo(14,1725,8200)      # initialize servo on GPIO pin 0
button = Pin(12, Pin.IN, Pin.PULL_DOWN)
pot =ADC(Pin(26))
oldAngle=0
readingLines=False
led.on()

lines=[]

while True:
    angle=round(pot.read_u16()*180/65535,1)
    
    #Try to filter potentiometer data by limiting angular changes to 1.5 degrees
    if abs(oldAngle-angle)>1.5:
        oldAngle=angle
        s1.gotoAngle(angle)
        utime.sleep_ms(10)
    
    #Read button status
    if button.value():
        #Determine button press time. Anything longer than 0.5s will stop the line read
        utime.sleep_ms(10)
        t1=utime.ticks_ms()
        while button.value():
            t2=utime.ticks_ms()
        deltaTime=t2-t1
        
        if deltaTime <= 500:
            if not readingLines:
                print("Start position: ", angle)
                utime.sleep_ms(10)
                bA=angle
                bB=angle
            else:
                print("End position: ", angle)
                utime.sleep_ms(10)
                eA=angle
                eB=angle
                lines.append(Line(bA,bB,eA,eB))
            readingLines=not readingLines
        else:
            for l in lines:
                print("Painting line: (", l.sA, ", ", l.sB, "), (", l.eA, ", ", l.eB, ")")
                #print(l.sA, l.sB, l.eA, l.eB)
                led.off()
                s1.gotoAngle(l.sA)
                utime.sleep_ms(100)
                led.on()
                s1.gotoAngle(l.eA)
                utime.sleep_ms(100)
                
