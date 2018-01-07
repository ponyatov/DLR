# Virtual Machine/GUI

from SYM import *

import threading            # GUI must be separate thread
import wx                   # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class MainWindow(wx.Frame):    # inherit GUI widget
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/5*4 ; W = H/4*3
        RightCorner = (SW-W,SH-H) ; Center = (SW/7,SH/7)
        LPW = 32 # lines per window
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # show window
        self.Show()
        # console font
        self.font = wx.Font(H/LPW,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # sizer
        self.Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Vsizer = wx.BoxSizer(wx.VERTICAL) 
        self.SetSizer(self.Hsizer)
        # workpad
        self.workpad = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.workpad.SetFont(self.font)
        self.workpad.SetValue('# workpad\n\n\twords')
        # shell
        self.shell = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.shell.SetFont(self.font)
        self.shell.SetValue('# shell')
        # words
        self.words = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.words.SetFont(self.font)
        self.words.SetValue('# words')
        # stack
        self.stack = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.stack.SetFont(self.font)
        self.stack.SetValue('# stack')
        # place
        self.Hsizer.Add(self.words,1,wx.EXPAND)
        self.Vsizer.Add(self.workpad,4,wx.EXPAND)
        self.Vsizer.Add(self.shell,1,wx.EXPAND)
        self.Hsizer.Add(self.Vsizer,4,wx.EXPAND)
        self.Hsizer.Add(self.stack,2,wx.EXPAND)
        self.Layout()

def GUI():
    global wxmain ; wxmain = MainWindow()
    wxapp.MainLoop()

thread_GUI = threading.Thread(None,GUI)
thread_GUI.start()

thread_GUI.join()    # wait until GUI stops
