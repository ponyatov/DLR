# Virtual Machine/GUI

from SYM import *

import threading            # GUI must be separate thread
import wx                   # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class PageWindow(wx.Frame): # inherit GUI widget
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/5*4 ; W = H/4*3 ; Center = (SW/7,SH/11)
        # colors
        color = {'F':'#000011','B':'#E0E0AA'}
        # console font
        font = wx.Font(H/24,
            wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        self.Show()
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # tabbing
        tab = wx.Notebook(self) ; tab.SetFont(font)
        tab.SetBackgroundColour(color['F']);
        tab.SetForegroundColour(color['B']);
        # workpad
        workpad = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        workpad.SetValue('# workpad\n\n\twords')
        workpad.SetBackgroundColour(color['F']);
        workpad.SetForegroundColour(color['B']);
        tab.AddPage(workpad,'pad')
        # stack
        stack = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        stack.SetValue('# stack')
        stack.SetBackgroundColour(color['F']);
        stack.SetForegroundColour(color['B']);
        tab.AddPage(stack,'stack')
        # words
        words = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        words.SetValue('# words')
        words.SetBackgroundColour(color['F']);
        words.SetForegroundColour(color['B']);
        tab.AddPage(words,'words')
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
        # sizer
        self.Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Vsizer = wx.BoxSizer(wx.VERTICAL) 
        self.SetSizer(self.Hsizer)
        # workpad
        self.workpad = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.workpad.SetFont(self.font)
        self.workpad.SetValue('# workpad\n\n\twords')
        self.workpad.SetBackgroundColour(BG);
        self.workpad.SetForegroundColour(FG);
        # shell
        self.shell = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.shell.SetFont(self.font)
        self.shell.SetValue('# shell')
        self.shell.SetBackgroundColour(BG);
        self.shell.SetForegroundColour(FG);
        # words
        self.words = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.words.SetFont(self.font)
        self.words.SetValue('# words')
        self.words.SetBackgroundColour(BG);
        self.words.SetForegroundColour(FG);
        # stack
        self.stack = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.stack.SetFont(self.font)
        self.stack.SetValue('# stack')
        self.stack.SetBackgroundColour(BG);
        self.stack.SetForegroundColour(FG);
        # place
        self.Hsizer.Add(self.words,1,wx.EXPAND)
        self.Vsizer.Add(self.workpad,4,wx.EXPAND)
        self.Vsizer.Add(self.shell,1,wx.EXPAND)
        self.Hsizer.Add(self.Vsizer,4,wx.EXPAND)
        self.Hsizer.Add(self.stack,2,wx.EXPAND)
        self.Layout()

def GUI():
    global wxmain ; wxmain = PageWindow()
    wxapp.MainLoop()

thread_GUI = threading.Thread(None,GUI)
thread_GUI.start()

thread_GUI.join()    # wait until GUI stops
