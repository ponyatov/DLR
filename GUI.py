import time

import threading
import wx					# import wxWidgets

wxapp = wx.App()		# create wx GUI application

# https://www.blog.pythonlibrary.org/2013/07/12/wxpython-how-to-minimize-to-system-tray/
class TaskBar(wx.TaskBarIcon):	# taskbar manager
	def __init__(self,frame):
		# init superclass
		wx.TaskBarIcon.__init__(self)
		# save frame we manage
		self.frame = frame
		# set taskbar icon
		self.icon = frame.icon
		self.SetIcon(self.icon,sys.argv[0])
		# bind open/focus on left click
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN,
			self.OnTaskBarLeftClick)
	def OnTaskBarActivate(self,event):
		pass
	def OnTaskBarClose(self,event):
		self.frame.Close()
	def OnTaskBarLeftClick(self,event):
		self.frame.Show()		# show frame
		self.frame.Restore()	# un(min|max)imize
		self.frame.Raise()		# make top level window
		self.frame.SetFocus()	# and set focus

class MainWindow(wx.Frame): # main GUI window in class
	def __init__(self):
		# tune size and position to look like messenger
		X,Y,W,H = wx.ClientDisplayRect()
		# create main frame
		wx.Frame.__init__(self,None,-1,sys.argv[0],
		size=(W/4,H/2),pos=(W-W/4,H-H/2))
		# style tune
		self.icon = wx.ArtProvider.GetIcon(wx.ART_ADD_BOOKMARK)
		self.SetIcon(self.icon)
		self.SetBackgroundColour(wx.BLACK)
		# set visible
		self.Show()
		# make GUI taskbared
		self.tbIcon = TaskBar(self)
	def onClose(self,event):
		# required to remove taskbar icon
		self.tbIcon.RemoveIcon()
		self.tbIcon.Destroy()
		# destroy main window itself
		self.Destroy()
	def shot(self,PNG='sshot.png'):	# do screen shot
		dc = wx.ScreenDC()
		X,Y,W,H = self.GetRect()
		bmp = wx.EmptyBitmap(W,H)
		mdc = wx.MemoryDC(bmp)
		mdc.Blit(0,0,W,H,dc,X,Y)
		bmp.SaveFile(PNG,wx.BITMAP_TYPE_PNG)

def startGUI():				# wrap thread in function
	global wxmain			# required for ScreenShot()
	wxmain = MainWindow()	# construct main window
	wxapp.MainLoop()		# start wx GUI main loop
thGUI = threading.Thread(None,startGUI)
thGUI.start()				# start GUI thread

# time.sleep(1) ; wxmain.shot()

thGUI.join()				# wait until GUI stops
