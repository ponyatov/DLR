# Dynamic GUI (mobile phone layout)

from SYM import *
import VM

import threading            # GUI must be separate thread
import wx                   # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class MainWindow(wx.Frame): # inherit GUI widget
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/5*4 ; W = H/4*3 ; Center = (SW/7,SH/11)
        # console font
        font = wx.Font(H/48,
            wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        self.Show()
#         self.Maximize()
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # tabbing
        tab = wx.Notebook(self) ; tab.SetFont(font)
        # log
        log = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        log.SetValue('# log')
        tab.AddPage(log,'log')
        # pad
        pad = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        pad.SetValue('# pad\n\n\twords')
        tab.AddPage(pad,'pad',select=True)
        # stack
        stack = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        stack.SetValue(VM.D.dump()[1:])
        tab.AddPage(stack,VM.D.tag)
        # words
        words = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        words.SetValue(VM.W.dump()[1:])
        tab.AddPage(words,VM.W.val)
        # draw
        draw = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        draw.SetValue('# draw')
        tab.AddPage(draw,'draw')
        # shell
        shell = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        shell.SetValue('# shell')
        tab.AddPage(shell,'shell')
        # files
        files = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        files.SetValue(Dir().dump()[1:])
        tab.AddPage(files,'files')
        # layout
        sizer = wx.BoxSizer()
        sizer.Add(tab,1,wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

def GUI():
    global wxmain ; wxmain = MainWindow()
    wxapp.MainLoop()

thread_GUI = threading.Thread(None,GUI)
thread_GUI.start()

thread_GUI.join()    # wait until GUI stops
