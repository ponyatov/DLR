# Virtual Machine/GUI

from SYM import *

import threading            # GUI must be separate thread
import wx                    # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class MainWindow(wx.Frame):    # inherit GUI widget
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/2 ; W = H/4*3
        RightCorner = (SW-W,SH-H) ; Center = (SW/5,SH/4)
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # show window
        self.Show()
        # console font
        self.font = wx.Font(H/32,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # sizer
        self.Hsizer = wx.BoxSizer(wx.VERTICAL)
        self.Vsizer = wx.BoxSizer(wx.VERTICAL) 
        self.SetSizer(self.Vsizer)
        # workpad
        self.workpad = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.workpad.SetFont(self.font)
        self.workpad.SetValue('# workpad\n\n\twords')
        # shell
        self.shell = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.shell.SetFont(self.font)
        self.shell.SetValue('# shell')
        # place
        self.Vsizer.Add(self.workpad,4,wx.EXPAND)
        self.Vsizer.Add(self.shell,1,wx.EXPAND)
        self.Layout()

def GUI():
    global wxmain ; wxmain = MainWindow()
    wxapp.MainLoop()

thread_GUI = threading.Thread(None,GUI)
thread_GUI.start()

thread_GUI.join()    # wait until GUI stops
