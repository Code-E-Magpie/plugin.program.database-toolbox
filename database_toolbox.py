# ============================================================
#################################
# database_toolbox.py by Code-E-Magpie
#################################
# ============================================================

# ============================================================
# File information
# ============================================================

# sourced from: plugin.program.code-e-magpie > abacus_program.py
# location: plugin.program.database-toolbox > database_toolbox.py
# type: system
# functionality: database toolbox

# ============================================================
# Import
# ============================================================

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
import os, sqlite3, sys

# ============================================================
# Variables
# ============================================================

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id') # id in addons.xml
ADDON = xbmcaddon.Addon(ADDON_ID)
ADDON_DEVELOPER = ADDON.getAddonInfo('author') # provider-name in addons.xml (developer)
ADDON_FANART = ADDON.getAddonInfo('fanart')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name') # name in addons.xml
ADDON_TITLE = (' '.join((ADDON_NAME).strip(' '))) # insert spaces between + remove leading & trailing
ADDON_VERSION = ADDON.getAddonInfo('version') # version in addons.xml
DATABASE = xbmcvfs.translatePath('special://database/')
DATABASE_ADDONS = os.path.join(DATABASE, 'Addons33.db')
PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
TEXT_ADDON = 'yellow' # default to "name" colour in addon.xml if quote marks are empty i.e. = ''
TEXT_DARK = 'darkgray'
TEXT_DIM = 'dimgray'
TEXT_GENERAL = 'silver'
TEXT_HIGHLIGHT = 'yellow'
TEXT_ITEM = 'blue'
TEXT_VALUE = 'orange'
TOOLBOX = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', 'toolbox.png')

# ============================================================
# Addon_ID_Version / Addon_Title / Addons / Dialogue / Log_Title
# ============================================================

Addon_ID_Version = ('[COLOR %s]%s [/COLOR][COLOR %s] %s[/COLOR]' % (TEXT_ITEM, ADDON_ID, TEXT_VALUE, ADDON_VERSION))
Addon_Title = ('[COLOR %s]%s[/COLOR]' % (TEXT_ADDON, ADDON_TITLE))
Addons = ('[COLOR %s]addons > [/COLOR]' % TEXT_GENERAL)
Dialogue = xbmcgui.Dialog()
Log_Title = ('[COLOR %s]%s [/COLOR]' % (TEXT_ADDON, ADDON_NAME))

# ============================================================
# FUNCTION: Log
# ============================================================

def Log(msg, level = xbmc.LOGDEBUG):
	xbmc.log(msg, level = level)

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# User Information
# ------------------------------------------------------------
# ============================================================

# ============================================================
# FUNCTION: TextBox
# ============================================================

ACTION_BACKSPACE = 110 # Backspace
ACTION_MOUSE_LEFT_CLICK = 100 # Mouse click
ACTION_MOUSE_LONG_CLICK = 108 # Mouse long click
ACTION_MOUSE_WHEEL_DOWN = 105 # Mouse wheel down
ACTION_MOUSE_WHEEL_UP = 104 # Mouse wheel up
ACTION_MOVE_DOWN = 4 # Down arrow key
ACTION_MOVE_LEFT = 1 # Left arrow key
ACTION_MOVE_MOUSE = 107 # Down arrow key
ACTION_MOVE_RIGHT = 2 # Right arrow key
ACTION_MOVE_UP = 3 # Up arrow key
ACTION_NAV_BACK = 92 # Backspace action
ACTION_PREVIOUS_MENU = 10 # ESC action
ACTION_SELECT_ITEM = 7 # Number Pad Enter

def TextBox(title, msg):
	class TextBoxes(xbmcgui.WindowXMLDialog):

		def onAction(self, action):
			if action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

		def onClick(self, controlId):
			if (controlId == self.okbutton):
				self.close()
			elif controlId != self.okbutton:
				self.noop = lambda: None

		def onInit(self): # group = 8000, background = 8100, noop = 8181
			self.title = 8200 # header
			self.msg = 8300 # textbox
			self.scrollbar = 8400 # scrollbar
			self.okbutton = 8500 # close button
			self.noop = lambda: None
			self.showDialog()

		def showDialog(self):
			self.getControl(self.title).setLabel(title)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

	textbox = TextBoxes("Textbox.xml", ADDON.getAddonInfo('path'), 'default')
	textbox.doModal()
	del textbox

# ============================================================
# FUNCTION: User_Information
# ============================================================

INSTRUCTIONS_TEXT = '[CR]I N S T R U C T I O N S[CR][CR]Open the add-on to access the menu.[CR]Select one of the \'>\' menu items and follow the user information.'

NOTES_TEXT = '[CR][CR][CR]N O T E S[CR][CR]Backup databases before proceeding.[CR]Close other add-ons and save any changes. Restart Kodi if required.[CR][CR]\'Clean Addons Database  >\' Kodi will need to close without cleanup at the end.[CR][CR]\'Exit Only >\' - exits the add-on.'

DEVELOPMENT_TEXT = '[CR][CR][CR]D E V E L O P M E N T[CR][CR]Kodi v21.3 Omega apk (Android app) with Confluence skin as default (including default font).[CR]Tablet (1340 x 800 aspect ratio 5:3) running Android 14 using QuickEdit apk (TryItAndSee / LearnAsYouGo iterative development and testing).[CR]Chromecast HD (1280 x 720 aspect ratio 16:9) running Android TV OS version 14 (user testing).[CR]100% tested and working on Android.[CR]Not tested on other platforms.[CR]Code debugged and reengineered where required using https://aipy.dev/tools'

CHANGELOG_TEXT = '[CR][CR][CR]C H A N G E L O G [LIGHT] (newest at the top)[/LIGHT][CR][CR]Version code x.y.z attributes[CR]x = major change / y = number of \'>\' menu items / z = minor change[CR][CR]version 1.3.0 (3 menu items)[CR]- initial code from Abacus Program 1.0.0 by C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e (plugin.program.code-e-magpie)[CR]- code added from Truncate Tables 1.0.1 by The Cleaner (plugin.program.truncatetables)[CR]- icon.png changed and toolbox.png added[CR]- variables and functions reworked[CR]- menu, dialogue boxes and logs reworked[CR]- user information updated including instructions and changelog'

User_Information_Text = '[COLOR %s][B]U S E R   I N F O R M A T I O N[/B][CR][COLOR %s][LIGHT](Instructions / Notes / Development / Changelog)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, TEXT_VALUE, TEXT_GENERAL, (INSTRUCTIONS_TEXT + NOTES_TEXT + DEVELOPMENT_TEXT + CHANGELOG_TEXT))

def User_Information():
	TextBox('[B]%s[/B][CR]%s' % (Addon_Title, Addon_ID_Version), User_Information_Text)

#####################################################################################

# ============================================================
# FUNCTION: Addons_Database
# ============================================================

def Addons_Database():

	Log(Log_Title + Addons + '[COLOR %s][LIGHT]Started (addons database: special://database/Addons33.db)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)
	success = False

	Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]Backup the database before proceeding.[/COLOR][CR]Close other add-ons and save any changes.[CR]Restart Kodi if required.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

	addons_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]Backup the database before proceeding.[CR]Kodi will need to close without cleanup at the end.[/COLOR][CR]Would you like to continue ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Clean Database[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Cancel Clean[/COLOR]' % TEXT_HIGHLIGHT))

	if not addons_choice:
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Cancelled[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)
		sys.exit()

	try:
		con = sqlite3.connect(DATABASE_ADDONS)
		cursor = con.cursor()
		cursor.execute('DELETE FROM addonlinkrepo;',)
		cursor.execute('DELETE FROM addons;',)
		cursor.execute('DELETE FROM package;',)
		cursor.execute('DELETE FROM repo;',)
		cursor.execute('DELETE FROM update_rules;',)
		cursor.execute('DELETE FROM version;',)
		con.commit()

		success = True

	except sqlite3.Error as e:

		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]Unable to clean database.[/COLOR][CR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))
		Log(Log_Title + Addons + 'database read error[CR]%s' % str(e), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if con:
				con.close()

		except UnboundLocalError as e:
			Log(Log_Title + Addons + 'database connection error[CR]%s' % str(e), xbmc.LOGERROR)

	try:
		con = sqlite3.connect(DATABASE_ADDONS)
		cursor = con.cursor()
		cursor.execute('VACUUM;',)
		con.commit()

	except sqlite3.Error as e:
		Log(Log_Title + Addons + 'database table error[CR]%s' % str(e), xbmc.LOGERROR)

	finally:
		try:
			if con:
				con.close()
		except sqlite3.Error:
			pass

	if success is True:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]Database cleaned.[/COLOR][CR]Kodi will need to close without cleanup.[CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Finished (addons database: special://database/Addons33.db)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)
		os._exit(1)

#####################################################################################

# ============================================================
# Menu Entry Point
# ============================================================

if '/Addons_Database' in PLUGIN_URL:

	Addons_Database()


elif '/Exit_Only' in PLUGIN_URL:

	xbmc.executebuiltin('Action(Back)')

	Log(Log_Title + Addons + '[COLOR %s][LIGHT]Finished (Exit Only)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)	


elif '/User_Information' in PLUGIN_URL:

	User_Information()


else:
	# Create the menu items.
	xbmcplugin.setContent(PLUGIN_ID, 'files')

	Equals = xbmcgui.ListItem('[COLOR %s]==================================================[/COLOR]' % TEXT_DIM)
	Equals.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_FANART})

	Addon_Header = xbmcgui.ListItem('[B]%s[/B]' % Addon_Title)
	Addon_Header.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Addons_Database = xbmcgui.ListItem('[COLOR %s]Clean Addons Database  [/COLOR]>' % TEXT_GENERAL)
	Addons_Database.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Exit_Only = xbmcgui.ListItem('[COLOR %s]Exit Only  [/COLOR]>' % TEXT_GENERAL)
	Exit_Only.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	User_Information = xbmcgui.ListItem('[COLOR %s]U s e r   I n f o r m a t i o n  >[/COLOR]' % TEXT_DARK)
	User_Information.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Addon_Developer = xbmcgui.ListItem('[COLOR %s]Developer: [/COLOR]%s' % (TEXT_DIM, ADDON_DEVELOPER))
	Addon_Developer.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Name = xbmcgui.ListItem('[COLOR %s]Name: %s[/COLOR]' % (TEXT_DIM, ADDON_NAME))
	Addon_Name.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Version = xbmcgui.ListItem('[COLOR %s]Version: %s[/COLOR]' % (TEXT_DIM, ADDON_VERSION))
	Addon_Version.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_ID = xbmcgui.ListItem('[COLOR %s]Addon ID: %s[/COLOR]' % (TEXT_DIM, ADDON_ID))
	Addon_ID.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	# Append to PLUGIN_URL as it already ends with a slash.
	xbmcplugin.addDirectoryItems(
		PLUGIN_ID,
		(
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL, Addon_Header, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'Addons_Database', Addons_Database, False),
			(PLUGIN_URL + 'Exit_Only', Exit_Only, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'User_Information', User_Information, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL, Addon_Developer, False),
			(PLUGIN_URL, Addon_Name, False),
			(PLUGIN_URL, Addon_Version, False),
			(PLUGIN_URL, Addon_ID, False)
		)
	)
	xbmcplugin.endOfDirectory(PLUGIN_ID)