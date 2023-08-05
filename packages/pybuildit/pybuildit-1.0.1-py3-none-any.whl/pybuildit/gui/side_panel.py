import sys,os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as Tk
from pybuildit.gui.util  import *
from tkinter import simpledialog
from pybuildit import *
from tkinter import messagebox
import logging

logger = logging.getLogger("pybuildit")

class FaultStatusFrame(Tk.Frame):

    def __init__(self, buildit, master=None):
        Tk.Frame.__init__(self, master)
        self.buildit = buildit

        self.logo_R = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'imgs', "LED-RED.gif"))
        self.logo_O = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'imgs', "LED-OFF.gif"))
        self.logo_G = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'imgs', "LED-GREEN.gif"))

        self.isConnected = False
        self.faults  = 0


        for i,(k,v) in enumerate(faultDict.items()):

            stat =Label(self, text=v, font=("Arial Bold", 8))
            stat.grid(column=2, row=i+1, sticky=N+S+W)

            led = Label(self, image=self.logo_O)
            led.grid(column=1, row=i+1, sticky=N+S+E)


    def lightOff(self):
        led = Label(self, image=self.logo_O)
        led.grid(column=1, row=1, sticky=N+S+E)
        for i,(k,v) in enumerate(faultDict.items()):
            led = Label(self, image=self.logo_O)
            led.grid(column=1, row=i+1, sticky=N+S+E)

    def lightOn(self):
        if self.faults == 0:
            led = Label(self, image=self.logo_G)
            led.grid(column=1, row=1, sticky=N+S+E)
            for i,(k,v) in enumerate(faultDict.items()):
                if i == 0: continue
                led = Label(self, image=self.logo_O)
                led.grid(column=1, row=i+1, sticky=N+S+E)
        else:
            for i,(k,v) in enumerate(faultDict.items()):
                if (k & self.faults) > 0:
                    led = Label(self, image=self.logo_R)
                    led.grid(column=1, row=i+1, sticky=N+S+E)
                else:
                    led = Label(self, image=self.logo_O)
                    led.grid(column=1, row=i+1, sticky=N+S+E)

    def onTick(self, servoStatus):
        if (self.isConnected):
            if (servoStatus is None):
                self.lightOff()
            elif (self.faults != servoStatus[5]):
                self.faults = servoStatus[5]
                self.lightOn()
        elif (servoStatus is not None):
            self.lightOn()

        self.isConnected = servoStatus is not None

class ModeControlFrame(Tk.Frame):
    
    def __init__(self, buildit, master=None):
        Tk.Frame.__init__(self, master)
        self.buildit = buildit
        self.currentState = "STATE_UNKNOWN"
        self.currentTemp = "?"

        self.isConnected = False

        self.clearButton= Tk.Button(self, text='ClearFault', width= "10", command=self.clear)
        self.clearButton.pack(pady=5)

        self.holdButton= Tk.Button(self, text='Hold', width= "10", command=self.hold)
        self.holdButton.pack(pady=5)

        self.freeButton= Tk.Button(self, text='Free', width= "10", command=self.free)
        self.freeButton.pack(pady=5)

        self.readyButton= Tk.Button(self, text='Ready', width= "10", command=self.ready)
        self.readyButton.pack(pady=5)

        self.modeSelector()

        self.refvalText = Tk.Entry(self, width=10)
        self.refvalText.insert(Tk.END,"0")
        self.refvalText.pack(pady=5)

        self.speedLimit = IntVar()
        self.speedLimit.set(60)


        self.button= Tk.Button(self,text='SetRef', width= "5", command=self.set_ref)
        self.button.pack(pady=5)

        self.stopButton= Tk.Button(self, text='Stop', width= "10", command=self.stop)
        self.stopButton.pack(pady=5)

        self.statText = StringVar()
        self.statText.set(self.currentState)
        self.stat = Label(self, textvariable=self.statText, font=("Arial Bold", 9))
        self.stat.pack(pady=5)

        self.tempText = StringVar()
        self.tempText.set((str(self.currentTemp) + "°C"))

        self.temp =Label(self, textvariable=self.tempText, font=("Arial Bold", 9), fg="black")
        self.temp.pack(pady=5)

    def hold(self):
        
        logger.info("Hold button clicked ")
        tryBuildit(lambda: self.buildit.hold(builditGuiInfo.targetDevId))

    def free(self):
        
        logger.info("Free button clicked ")
        tryBuildit(lambda: self.buildit.free(builditGuiInfo.targetDevId))
        logger.info("State free")
    
    def ready(self):
        
        logger.info("Ready button clicked ")
        tryBuildit(lambda: self.buildit.ready(builditGuiInfo.targetDevId))

    def clear(self):
        
        logger.info("Clear button clicked ")
        tryBuildit(lambda: self.buildit.clear_fault(builditGuiInfo.targetDevId))

    def stop(self):
        logger.info("Stop button clicked ")
        tryBuildit(lambda: self.buildit.stop(builditGuiInfo.targetDevId))

    def set_ref(self):
        if not self.buildit.is_open():
            messagebox.showerror('error', 'no connection   ')
            logger.error('Connection Error')
            return

        ret = None
        if self.mode.get() == 0:
            v = int(self.refvalText.get())
            ret = tryBuildit(lambda: self.buildit.set_ref_current(builditGuiInfo.targetDevId, v))
            logger.info("Current: %s" %v)
        elif self.mode.get() == 1:
            v = float(self.refvalText.get())
            ret = tryBuildit(lambda: self.buildit.set_ref_velocity(builditGuiInfo.targetDevId, from_rpm(v)))
            logger.info("velocity: %s" %v)
        elif self.mode.get() == 2:
            v = float(self.refvalText.get())
            ret = tryBuildit(lambda: self.buildit.set_ref_position(builditGuiInfo.targetDevId, from_deg(v)))
            logger.info("Position: %s" %v)

    def modeSelector(self):

        self.mode = IntVar()
        self.mode.set(2)

        self.radio_cur = ttk.Radiobutton(self, value = 0, variable = self.mode, text = "current", width= "15")
        self.radio_cur.pack(pady=2)
        self.radio_vel = ttk.Radiobutton(self, value = 1, variable = self.mode, text = "velocity[rpm]", width= "15")
        self.radio_vel.pack(pady=2)
        self.radio_pos = ttk.Radiobutton(self, value = 2, variable = self.mode, text = "position[deg]", width= "15")
        self.radio_pos.pack(pady=2)
        logger.info("Mode Selector")

    def updateStatus(self):
        self.statText.set(self.currentState)
        #logger.info("current servo status: %s" %self.currentState)

    def updateTemp(self):
        self.tempText.set(str(self.currentTemp) + "°C")

    def onTick(self, servoStatus):
        if servoStatus is not None:
            newState = self.buildit.last_mcp_status().str_state()
            #logger.info('Servo status: %s'%newState)

            if (servoStatus[4] != self.currentTemp):
                self.currentTemp = servoStatus[4]
                self.updateTemp()
                logger.info('CurrentTemp: %s'%self.currentTemp)

            if newState != self.currentState:
                self.currentState = newState
                self.updateStatus()
                #logger.info('Newstate-updatestatus %s'%self.updateStatus())

    def updateSpeedSlider(self, servoStatus):
        if (self.isConnected):
            if (servoStatus is None):
                pass

        self.isConnected = servoStatus is not None

class SidePanel(Tk.Frame):

    def __init__(self, buildit, master):
        Tk.Frame.__init__(self, master)

        global tickListener
        tickListener.append(self)

        self.modeControl = ModeControlFrame(buildit, self)
        self.modeControl.pack()
        self.faultsStatus = FaultStatusFrame(buildit, self)
        self.faultsStatus.pack()

    def onTick(self, servoStatus):
        self.modeControl.onTick(servoStatus)
        self.faultsStatus.onTick(servoStatus)
        self.modeControl.updateSpeedSlider(servoStatus)


