"""The application starting point."""
import wx

from controller import Controller

app = wx.App()
controller = Controller()
app.MainLoop()
