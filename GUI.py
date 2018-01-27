# Dynamic GUI (mobile phone layout)

TESTCODE = '''#pad
        words?zz
1 2.3 4e5 ? #. ?'''

from SYM import *
import VM

import threading            # GUI must be separate thread
import wx                   # import wxWidgets
wxapp = wx.App()            # create wx GUI application

class MainWindow(wx.Frame): # inherit GUI widget
    def KeyDown(self,E):
        key = E.GetKeyCode()
        ctrl = E.CmdDown() ; alt = E.AltDown() ; shift = E.ShiftDown()
        print
        print self,E
        print ctrl,alt,shift,key
        if alt and key == wx.WXK_F4: self.Close()
        elif ctrl and key == wx.WXK_RETURN:
            VM.PAD_Q.put(self.pad.GetStringSelection())
        elif shift and key == wx.WXK_RETURN:
            self.edit.WriteText(self.pad.GetStringSelection())
        elif key == wx.WXK_F12:
            VM.PAD_Q.put(self.pad.GetValue())
        elif ctrl and key == wx.WXK_PAGEDOWN:
            pos = self.tab.GetSelection()+1
            if pos < self.tab.GetPageCount(): self.tab.SetSelection(pos)
            else: self.tab.SetSelection(0)
        elif ctrl and key == wx.WXK_PAGEUP:
            pos = self.tab.GetSelection()-1
            if pos >= 0: self.tab.SetSelection(pos)
            else: self.tab.SetSelection(self.tab.GetPageCount()-1)
        else:
            E.Skip()
    def Update(self,E):
        self.stack.SetValue(VM.D.dump()[1:])
        while not VM.log.empty(): self.log.AppendText(VM.log.get())
    def onClose(self,E):
        self.timer.Stop()
        self.Destroy()
    def __init__(self):
        # align on screen
        SW,SH = wx.GetDisplaySize()
        H = SH/5*4 ; W = H/5*3 ; Center = (SW/7,SH/11)
        # console font
        font = wx.Font(H/48,
            wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        # initialize superclass
        wx.Frame.__init__(self,None,title='SYM',pos=Center,size=(W,H))
        self.Bind(wx.EVT_CLOSE,self.onClose)
        self.Show()
        # set window icon
        self.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION))
        # tabbing
        self.tab = tab = wx.Notebook(self) ; tab.SetFont(font)
        # log
        self.log = log = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        log.SetValue('# log')
        tab.AddPage(log,'log')
        log.Bind(wx.EVT_CHAR,self.KeyDown)
        # edit
        self.edit = edit = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        edit.SetValue(TESTCODE)
        tab.AddPage(edit,'edit',select=True)
        edit.Bind(wx.EVT_CHAR,self.KeyDown)
        # stack
        self.stack = stack = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        self.stack.SetValue(VM.D.dump()[1:])
        tab.AddPage(stack,VM.D.tag)
        stack.Bind(wx.EVT_CHAR,self.KeyDown)
        # words
        words = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        words.SetValue(VM.W.dump()[1:])
        tab.AddPage(words,VM.W.val)
        words.Bind(wx.EVT_CHAR,self.KeyDown)
        # draw
        draw = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        draw.SetValue('# draw')
        tab.AddPage(draw,'draw')
        draw.Bind(wx.EVT_CHAR,self.KeyDown)
        # shell
        shell = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        shell.SetValue('# shell')
        tab.AddPage(shell,'shell')
        shell.Bind(wx.EVT_CHAR,self.KeyDown)
        # files
        files = wx.TextCtrl(tab,style=wx.TE_MULTILINE)
        files.SetValue(Dir().dump()[1:])
        tab.AddPage(files,'files')
        files.Bind(wx.EVT_CHAR,self.KeyDown)
        # pad
        pad = self.pad = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.pad.SetValue(TESTCODE)
        pad.SetFont(font)
        pad.Bind(wx.EVT_CHAR,self.KeyDown)
        # layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tab,4,wx.EXPAND)
        sizer.Add(pad,1,wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        # start-up update timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.Update,self.timer)
        self.timer.Start(0x111)#ms

global wxmain ; wxmain = MainWindow()

thread_VM = threading.Thread(None,VM.PAD_runner) ; thread_VM.start()

wxapp.MainLoop() 

# thread_VM.join()    # wait until VM stops
