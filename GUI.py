# Dynamic GUI (mobile phone layout)

from SYM import *
from VM import *

import threading            # GUI must be separate thread
import wx                   # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class PageWindow(wx.Frame): # inherit GUI widget
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/5*4 ; W = H/4*3 ; Center = (SW/7,SH/11)
        # colors
        color = {'F':wx.GREEN,'B':wx.BLACK}#'F':'#000011','B':'#E0E0AA'}
        # console font
        font = wx.Font(H/24,
            wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        self.Show()
        self.Maximize()
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # tabbing
        tab = wx.Notebook(self) ; tab.SetFont(font)
        tab.SetBackgroundColour(color['B']);
        tab.SetForegroundColour(color['F']);
        # log
        log = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        log.SetValue('# log')
        log.SetBackgroundColour(color['B']);
        log.SetForegroundColour(color['F']);
        tab.AddPage(log,'log')
        # workpad
        workpad = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        workpad.SetValue('# workpad\n\n\twords')
        workpad.SetBackgroundColour(color['B']);
        workpad.SetForegroundColour(color['F']);
        tab.AddPage(workpad,'pad')
        # stack
        stack = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        stack.SetValue('# stack')
        stack.SetBackgroundColour(color['B']);
        stack.SetForegroundColour(color['F']);
        tab.AddPage(stack,'stack')
        # words
        words = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        words.SetValue('# words')
        words.SetBackgroundColour(color['B']);
        words.SetForegroundColour(color['F']);
        tab.AddPage(words,'words')
        # draw
        draw = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        draw.SetValue('# draw')
        draw.SetBackgroundColour(color['B']);
        draw.SetForegroundColour(color['F']);
        tab.AddPage(draw,'draw')
        # shell
        shell = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        shell.SetValue('# shell')
        shell.SetBackgroundColour(color['B']);
        shell.SetForegroundColour(color['F']);
        tab.AddPage(shell,'shell')
        # layout
        sizer = wx.BoxSizer()
        sizer.Add(tab,1,wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

class MainWindow(wx.Frame):    
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/5*4 ; W = H/4*3
        RightCorner = (SW-W,SH-H) ; Center = (SW/7,SH/11)
        LPW = 32 # lines per window
        # colors
        BG = '#000011' ; FG = '#E0E0AA'
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # show window
        self.Show()
        # console font
        self.font = wx.Font(H/LPW,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)

def GUI():
    global wxmain ; wxmain = PageWindow()
    wxapp.MainLoop()

thread_GUI = threading.Thread(None,GUI)
thread_GUI.start()

thread_GUI.join()    # wait until GUI stops
