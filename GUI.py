# Dynamic GUI (mobile phone layout)

from SYM import *
import VM

import threading            # GUI must be separate thread
import wx                   # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class PageWindow(wx.Frame): # inherit GUI widget
    def TabChanged(self,E):
        old = E.GetOldSelection() ; new = E.GetSelection()
        print old,new,self
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/5*4 ; W = H/4*3 ; Center = (SW/7,SH/11)
        # colors
        color = {'F':wx.GREEN,'B':wx.BLACK,'S':wx.CYAN}
        # console font
        font = wx.Font(H/32,
            wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        self.SetBackgroundColour(color['B']);
        self.Show()
#         self.Maximize()
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # tabbing
        tab = wx.Notebook(self) ; tab.SetFont(font)
        tab.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.TabChanged)
        tab.SetBackgroundColour(color['B']);
        tab.SetForegroundColour(color['F']);
        # log
        log = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        log.SetValue('# log')
        log.SetBackgroundColour(color['B']);
        log.SetForegroundColour(color['F']);
        tab.AddPage(log,'log')
        # pad
        pad = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        pad.SetValue('# pad\n\n\twords')
        pad.SetBackgroundColour(color['B']);
        pad.SetForegroundColour(color['F']);
        tab.AddPage(pad,'pad',select=True)
        # stack
        stack = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        stack.SetValue(VM.D.dump()[1:])
        stack.SetBackgroundColour(color['B']);
        stack.SetForegroundColour(color['F']);
        tab.AddPage(stack,VM.D.tag)
        # words
        words = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        words.SetValue(VM.W.dump()[1:])
        words.SetBackgroundColour(color['B']);
        words.SetForegroundColour(color['F']);
        tab.AddPage(words,VM.W.val)
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
        # files
        files = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        files.SetValue(Dir().dump()[1:])
        files.SetBackgroundColour(color['B']);
        files.SetForegroundColour(color['F']);
        tab.AddPage(files,'files')
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
