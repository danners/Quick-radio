#!/usr/bin/env python

import gtk, gst, pynotify, pickle,os

class Sender:
	def __init__(self,name,address,cat):
		self.address=address
		self.name=name
		self.cat=cat


class Player:
	def __init__(self):
		self.senderliste= pickle.load(settings)
		self.player = gst.element_factory_make("playbin","player")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_message)
	
	def playradio(self,origin,sender):
		self.player.set_state(gst.STATE_NULL)
		self.player.set_property("uri",sender.address)
		self.player.set_state(gst.STATE_PLAYING)
		notify("Spiele "+sender.name)

	def stopradio(self,origin):
		self.player.set_state(gst.STATE_NULL)
	
	def on_message(self,bus,message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug

class RadioMenu(gtk.Menu):

	def __init__(self):
		gtk.Menu.__init__(self)
	       	self.radio = Player()	
		for sender in self.radio.senderliste:
				item = gtk.ImageMenuItem(sender.name)
				item.connect('activate', self.radio.playradio,sender)
				item.set_image(gtk.image_new_from_stock('gtk-media-play', gtk.ICON_SIZE_MENU))
				self.append(item)

	
		item = gtk.SeparatorMenuItem()
		self.append(item)
	
		
		item = gtk.ImageMenuItem('Pause')
		item.connect('activate', self.radio.stopradio)
		item.set_image(gtk.image_new_from_stock('gtk-media-stop',gtk.ICON_SIZE_MENU))
		self.append(item)
	
		
		item = gtk.ImageMenuItem('Beenden')
		item.connect('activate', gtk.main_quit)
		item.set_image(gtk.image_new_from_stock('gtk-quit',gtk.ICON_SIZE_MENU))
		self.append(item)
		

		

	def show_menu(self, widget, button, time):
			self.show_all()
			self.popup(None, None, gtk.status_icon_position_menu, button, time, icon)

	

def initCaps ():
	capabilities = {'actions':             False,
	'body':                False,
	'body-hyperlinks':     False,
	'body-images':         False,
	'body-markup':         False,
	'icon-multi':          False,
	'icon-static':         False,
	'sound':               False,
	'image/svg+xml':       False,
	'private-synchronous': False,
	'append':              False,
	'private-icon-only':   False}
	caps = pynotify.get_server_caps ()
	if caps is None:
        	print "Failed to receive server caps."
		gtk.main_quit()
	for cap in caps:
		capabilities[cap] = True

def notify(message):
		printmsg = pynotify.Notification(message,"","gnome-dev-wavelan")
		printmsg.show()

if __name__=="__main__":

	icon = gtk.status_icon_new_from_file('/usr/share/icons/gnome/24x24/devices/gnome-dev-wavelan.png')
	icon.set_tooltip('Radio switcher')
	settings = open(os.path.expanduser('~')+'/.radio','r')
	menu = RadioMenu()
	pynotify.init('icon-summary')
	initCaps()
	icon.connect("popup-menu",menu.show_menu)
	gtk.main()
