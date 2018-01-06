# Virtual Machine/GUI

from SYM import *

import threading            # GUI must be separate thread
import wx                    # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class MainWindow(wx.Frame):    # inherit GUI widget
    def __init__(self):
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM')
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # show window
        self.Show()
        # align on screen
        W,H = wx.GetDisplaySize()
        

def GUI():
    global wxmain ; wxmain = MainWindow()
    wxapp.MainLoop()

thread_GUI = threading.Thread(None,GUI)
thread_GUI.start()

thread_GUI.join()    # wait until GUI stops
