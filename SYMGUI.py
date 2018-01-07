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
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=(SW-W,SH-H),size=(W,H))
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # show window
        self.Show()
        # console font
        self.font = wx.Font(H/32,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL) ; self.SetSizer(self.sizer)
        # console
        self.console = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.console.SetFont(self.font)
        self.console.SetValue('# console')
        # cmdline
        self.cmdline = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.cmdline.SetFont(self.font)
        self.cmdline.SetValue('# cmdline')
        # place
        self.sizer.Add(self.console,4,wx.EXPAND)
        self.sizer.Add(self.cmdline,1,wx.EXPAND)
        self.Layout()

def GUI():
    global wxmain ; wxmain = MainWindow()
    wxapp.MainLoop()

thread_GUI = threading.Thread(None,GUI)
thread_GUI.start()

thread_GUI.join()    # wait until GUI stops
