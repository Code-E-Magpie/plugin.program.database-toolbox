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
import fnmatch, glob, os, re, sqlite3, sys

# ============================================================
# Variables
# ============================================================

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id') # id in addons.xml
ADDON = xbmcaddon.Addon(ADDON_ID)
ADDON_DATA_PATH = 'special://userdata/addon_data'
ADDON_DEVELOPER = ADDON.getAddonInfo('author') # provider-name in addons.xml (developer)
ADDON_FANART = ADDON.getAddonInfo('fanart')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name') # name in addons.xml
ADDON_VERSION = ADDON.getAddonInfo('version') # version in addons.xml
ADDONS_PATH = 'special://home/addons'
DATABASE = xbmcvfs.translatePath('special://database/')
DATABASE_PATH = 'special://database/'
HOME = xbmcvfs.translatePath('special://home/')
HOME_PATH = 'special://home/'
NOTIFICATION_DURATION = ADDON.getSetting('NOTIFICATION_DURATION')
PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
SIZE_HIGHLIGHT = ADDON.getSetting('SIZE_HIGHLIGHT')
SPACER_ROW = ADDON.getSetting('SPACER_ROW')
TEXT_ADDON = ADDON.getSetting('TEXT_ADDON')
TEXT_DARK = ADDON.getSetting('TEXT_DARK')
TEXT_DIM = ADDON.getSetting('TEXT_DIM')
TEXT_GENERAL = ADDON.getSetting('TEXT_GENERAL')
TEXT_HIGHLIGHT = ADDON.getSetting('TEXT_HIGHLIGHT')
TEXT_ITEM = ADDON.getSetting('TEXT_ITEM')
TEXT_VALUE = ADDON.getSetting('TEXT_VALUE')
TOOLBOX = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', 'toolbox.png')
USERDATA_PATH = 'special://userdata/'

# ============================================================
# Addon_ID_Version / Addon_Title / Dialogue / Log_Title
# ============================================================

Addon_ID_Version = ('[COLOR %s]%s [/COLOR][COLOR %s] %s[/COLOR]' % (TEXT_ITEM, ADDON_ID, TEXT_VALUE, ADDON_VERSION))
Addon_Title = ('[COLOR %s]%s[/COLOR]' % (TEXT_ADDON, ' '.join((ADDON_NAME).strip(' '))))
Dialogue = xbmcgui.Dialog()
Log_Title = ('[COLOR %s]%s [/COLOR]' % (TEXT_ADDON, ADDON_NAME))

# ============================================================
# Addons / Clean / Db / Menu
# ============================================================

Addons = ('[COLOR %s]addons > [/COLOR]' % TEXT_GENERAL)
Clean = ('[COLOR %s]clean > [/COLOR]' % TEXT_GENERAL)
Db = ('[COLOR %s]db > [/COLOR]' % TEXT_GENERAL)
Menu = ('[COLOR %s]menu > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Log
# ============================================================

def Log(msg, level = xbmc.LOGDEBUG):
	xbmc.log(msg, level = level)

# ============================================================
# FUNCTION: Notification
# ============================================================

def Notification(title, message, times = NOTIFICATION_DURATION, icon = ADDON_ICON, sound = False):
	Dialogue.notification(title, message, icon, int(times), sound)

# ============================================================
# FUNCTION: Size_Convert
# ============================================================

def Size_Convert(num, suffix = 'B'):

	for unit in ['', 'K', 'M', 'G']:
		if abs(num) < 1024.0:
			return "%3.02f %s%s" % (num, unit, suffix)
		num /= 1024.0

	return "%.02f %s%s" % (num, 'G', suffix)

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
			close = '[COLOR %s]Close[/COLOR]' % TEXT_GENERAL
			self.getControl(self.title).setLabel(title)
			self.getControl(self.okbutton).setLabel(close)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

	textbox = TextBoxes("Textbox.xml", ADDON.getAddonInfo('path'), 'default')
	textbox.doModal()
	del textbox

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# Information
# ------------------------------------------------------------
# ============================================================

# ============================================================
# FUNCTION: Development_Information
# ============================================================

MAGPIE_TEXT = '%s[CR][CR]The official repository of %s add-ons.[CR]Distribution of the Magpie Repository is permitted.[CR][CR][COLOR silver]IMPORTANT:[CR]Distribution of %s add-ons are NOT permitted.[CR]%s add-ons are exclusively distributed via the Magpie Repository and / or %s on GitHub.[CR]The code and files of these add-ons are free for use, subject to crediting %s.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.magpie[CR][CR]To install Magpie Repository:[CR]Add the Kodi source https://Code-E-Magpie.github.io/repository.magpie/[CR]Use the \'Install from zip file\' method to install the Magpie Repository.[/COLOR]' % (' '.join('MAGPIE REPOSITORY'), ADDON_DEVELOPER, ADDON_DEVELOPER, ADDON_DEVELOPER, ADDON_DEVELOPER, ADDON_DEVELOPER, TEXT_DARK)

DATABASE_TEXT = '[CR][CR][CR]%s[CR][CR]Database Toolbox with easy to use database maintenance tools.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.database-toolbox[/COLOR]' % (' '.join('DATABASE TOOLBOX'), TEXT_DARK)

MAINTENANCE_TEXT = '[CR][CR][CR]%s[CR][CR]Maintenance Toolbox with easy to read Kodi information (system, add-ons, network and internet).[CR]Clear cache + folders, surplus add-ons, temp folder and thumbnails.[CR]View logs and errors (new and old).[CR]Check repositories, sources and internet speed (Speedtest by Ookla).[CR]Backup and restore favourites, sources, logs, userdata, add-ons, add-on data etc.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.maintenance-toolbox[/COLOR]' % (' '.join('MAINTENANCE TOOLBOX'), TEXT_DARK)

REORDER_TEXT = '[CR][CR][CR]%s[CR][CR]Easy to use reordering of favourites for Kodi.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.reorder-favourites[/COLOR]' % (' '.join('REORDER FAVOURITES'), TEXT_DARK)

LOG_TEXT = '[CR][CR][CR]%s[CR][CR]System Log Toolbox easy to use system log viewer.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.system-log-toolbox[/COLOR]' % (' '.join('SYSTEM LOG TOOLBOX'), TEXT_DARK)

SPECIAL_TEXT = '[CR][CR][CR]%s[CR][CR]Special Favourites: Kodi special paths and customised examples.[CR]Special Sources: Kodi special paths (files & folders) and customised examples.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/Code-E-Magpie[/COLOR]' % (' '.join('FAVOURITES & SOURCES'), TEXT_DARK)

TEMPLATE_TEXT = '[CR][CR][CR]%s[CR][CR]Created to illustrate a GitHub repository with a simple folder structure linked to a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.template[/COLOR][CR][CR]Alternatively a GitHub repository linked to a Kodi source, without using a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.simple[/COLOR]' % (' '.join('TEMPLATE REPOSITORY'), TEXT_DARK, TEXT_DARK)

Development_Text = '[CR][CR][CR][COLOR %s][B]%s[/B][CR][COLOR %s][LIGHT](Magpie Repository / Database Toolbox / Maintenance Toolbox / Reorder Favourites / System Log Toolbox / Favourites & Sources / Template Repository)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('Code-E-Magpie Development'), TEXT_VALUE, TEXT_GENERAL, (MAGPIE_TEXT + DATABASE_TEXT + MAINTENANCE_TEXT + REORDER_TEXT + LOG_TEXT + SPECIAL_TEXT + TEMPLATE_TEXT))

# ============================================================
# FUNCTION: User_Information
# ============================================================

INSTRUCTIONS_TEXT = '%s[CR][CR]Open the add-on to access the menu.[CR]Select one of the \'>\' menu items and follow the user information.[CR][CR]\'Database Toolbox Settings >\' user settings:[CR]• Size highlight above value set (default = 1048576 i.e. 1 MB)[CR]• Spacer row on / off[CR]• \'Clean Databases (folder)\' options set dialogue boxes on / off[CR]• \'Clean Databases (folder)\' options set notifications on / off[CR]• set notification duration[CR]• customise text colours with trillions of text colour combinations[CR][CR]\'Clean Addons Database\' has a \'Would you like to continue ?\' option to exit before processing begins (see \'%s\' below).[CR][CR]\'Clean Databases (folder)\' options exclude \'Thumbs.db\' files.[CR]\'Clean Databases (folder): home >\' includes all databases but excludes \'Thumbs.db\' files.[CR]\'Clean Databases (folder): userdata >\' includes all databases but excludes addons and \'Thumbs.db\' files.[CR][CR]\'Database Files (.db file list) >\' includes \'Thumbs.db\' files in the \'Database Count\' for completeness.[CR]There is a separate total for \'Thumbs.db files\' and a list of databases (full path and database size).[CR][CR]\'Exit Only >\' exits the add-on.' % (' '.join('INSTRUCTIONS'), ' '.join('NOTES'))

NOTES_TEXT = '[CR][CR][CR]%s[CR][CR]It is important to proceed carefully so changes can be reversed if necessary i.e. \'Clean Addons Database\' closes Kodi without cleanup at the end.[CR][CR]• Backup databases using Kodi file manager or a backup add-on.[CR]• Close other add-ons and save any changes.[CR]• Restart Kodi if required.[CR][CR]ln everyday use the Textures13.db can get corrupted and prevent Kodi starting. Deleting the Textures13.db database resolves this as it rebuilds on startup.[CR]Other databases such as the add-ons database do not rebuild and may require restoring from backup if startup fails.[CR][CR]Later versions of Android make restoring a backedup database difficult.[CR]Android prevents users accessing the Data folder containing data for all the installed apps including Kodi and its databases.[CR]Access is possible using a file explorer app from the Play Store such as Total Commander.[CR]The app needs to be used with the Shizuku app from the Play Store or if restricted from GitHub https://github.com/RikkaApps/Shizuku' % ' '.join('NOTES')

ENVIRONMENT_TEXT = '[CR][CR][CR]%s[CR][CR]Kodi v21.3 Omega apk (Android app) with Confluence skin as default (including default font).[CR]Tablet (1340 x 800 aspect ratio 5:3) running Android 14 using QuickEdit apk (TryItAndSee / LearnAsYouGo iterative development and testing).[CR]Chromecast HD (1280 x 720 aspect ratio 16:9) running Android TV OS version 14 (user testing).[CR]100%% tested and working on Android.[CR]Not tested on other platforms.[CR]Code debugged and reengineered using https://aipy.dev/tools where required.' % ' '.join('DEVELOPMENT ENVIRONMENT')

CHANGELOG_TEXT = '[CR][CR][CR]%s[LIGHT] (newest at the top)[/LIGHT][CR][CR]Version code x.y.z attributes[CR]x = major change / y = number of \'>\' menu items / z = minor change[CR][CR]version 2.10.2 (10 menu items)[CR]- Clean Addons Database futureproofing added to select Addons*.db[CR]- minor changes to menu formatting[CR][CR]version 2.10.1 (10 menu items)[CR]- added text colour customisation to text boxes and buttons[CR]- added pre clean database size to dialogue boxes (\'Clean Databases (folder)\' options)[CR]- database information formatting reworked and renamed \'Database Files (.db file list) >\'[CR]- added spacer row and size highlight above value set in settings[CR]- minor changes to improve consistency with other add-ons[CR][CR]version 2.10.0 (10 menu items)[CR]- code added from OpenWizard 2.0.7 by drinfernoo & slamious (plugin.program.openwizard)[CR]- Clean Databases created[CR]- Database Information created[CR]- variables and functions reworked[CR]- menu, multiselect dialogue boxes and logs reworked[CR]- user information updated including instructions and notes[CR]- added user settings for dialogue boxes, notifications, notification duration and trillions of text colour combinations[CR][CR]version 1.3.1 (3 menu items)[CR]- database variable added[CR]- dialogue boxes and logs reworked[CR]- user information updated including instructions and notes[CR][CR]version 1.3.0 (3 menu items)[CR]- initial code from Abacus Program 1.0.0 by %s (plugin.program.code-e-magpie)[CR]- code added from Truncate Tables 1.0.1 by The Cleaner (plugin.program.truncatetables)[CR]- Clean Addons Database created[CR]- icon.png changed and toolbox.png added[CR]- variables and functions reworked[CR]- menu, dialogue boxes and logs reworked[CR]- user information added (instructions, notes, development and changelog)' % (' '.join('CHANGELOG'), ADDON_DEVELOPER)

User_Information_Text = '[COLOR %s][B]%s[/B][CR][COLOR %s][LIGHT](Instructions / Notes / Development Environment / Changelog)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('USER INFORMATION'), TEXT_VALUE, TEXT_GENERAL, (INSTRUCTIONS_TEXT + NOTES_TEXT + ENVIRONMENT_TEXT + CHANGELOG_TEXT))

def User_Information():
	TextBox('[B]%s[/B][CR]%s' % (Addon_Title, Addon_ID_Version), User_Information_Text + Development_Text)

#####################################################################################

# ============================================================
# FUNCTION: Clean_Addons_Database
# ============================================================

def Clean_Addons_Database():

	pattern = re.compile(r'Addons(\d+)\.db$', re.IGNORECASE)
	matches = glob.glob(os.path.join(DATABASE, 'Addons*.db'))
	highest = 0

	for file in matches:
		basename = os.path.basename(file)
		file_match = pattern.search(basename)
		if file_match:
			try:
				number = int(file_match.group(1))
			except ValueError:
				continue
			if number > highest:
				highest = number

	addons_db = "Addons%s.db" % highest

	Log(Log_Title + Addons + '[COLOR %s][LIGHT]Started (addons database: special://database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
	success = False

	Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Close other add-ons and save any changes.[CR]Restart Kodi if required.[/LIGHT][/COLOR][CR]Backup %s database before proceeding.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, addons_db))

	addons_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Kodi will need to close without cleanup at the end.[/LIGHT][/COLOR][CR][CR]Would you like to continue ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Clean Database[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Cancel Clean[/COLOR]' % TEXT_HIGHLIGHT))

	if not addons_choice:
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Cancelled (addons database: special://database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		sys.exit()

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()
		cursor.execute('DELETE FROM addonlinkrepo;',)
		cursor.execute('DELETE FROM addons;',)
		cursor.execute('DELETE FROM package;',)
		cursor.execute('DELETE FROM repo;',)
		cursor.execute('DELETE FROM update_rules;',)
		cursor.execute('DELETE FROM version;',)
		connection.commit()
		success = True

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to clean addons database: [COLOR %s]%s[/COLOR][CR]See Kodi System Log for details.[/LIGHT][/COLOR][CR]The database may not exsist.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + 'database read error: %s may not exist[CR]%s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Addons + 'database connection error: %s[CR]%s' % (addons_db, str(e)), xbmc.LOGERROR)

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()
		cursor.execute('VACUUM;',)
		connection.commit()

	except sqlite3.Error as e:
		Log(Log_Title + Addons + 'database table error: %s[CR]%s' % (addons_db, str(e)), xbmc.LOGERROR)

	finally:
		try:
			if connection:
				connection.close()

		except sqlite3.Error:
			pass

	if success is True:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Cleaned addons database: [COLOR %s]%s[/COLOR][CR]Kodi will need to close without cleanup.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Finished (addons database: special://database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		os._exit(1)

# ============================================================
# FUNCTION: Clean_Databases
# ============================================================

def Clean_Databases(folder_path):

	Log(Log_Title + Clean + '[COLOR %s][LIGHT]Started (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

	database = []; database_paths = []

	for root, dirs, files in os.walk(xbmcvfs.translatePath(folder_path)):
		for file in fnmatch.filter(files, '*.db'):
			if file != 'Thumbs.db':
				database_path = os.path.join(root, file)
				database_bytes = os.path.getsize(database_path)
				database_size = Size_Convert(database_bytes)
				path = database_path.replace('\\', '/').split('/')
				database.append(database_path)
				database_paths.append('[COLOR %s]%s > [/COLOR]%s [COLOR %s]> [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, path[len(path)-2], path[len(path)-1], TEXT_DIM, (TEXT_VALUE if database_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size))
				database_paths.sort(key = lambda v: v.upper())

	choice = Dialogue.multiselect(Addon_Title + "[COLOR %s][LIGHT]   (select one or more from the list)[/LIGHT][/COLOR]" % TEXT_GENERAL, database_paths, 0, [], False)

	if choice == None:
		Log(Log_Title + Clean + '[COLOR %s][LIGHT]Cancelled (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

	elif len(choice) == 0:
		Log(Log_Title + Clean + '[COLOR %s][LIGHT]Cancelled (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

	else:
		for database_selected in choice:
			Database_Cleaner(database[database_selected])

		Log(Log_Title + Clean + '[COLOR %s][LIGHT]Finished (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Database_Cleaner
# ============================================================

def Database_Cleaner(database_selected):
	
	Log(Log_Title + Db + 'clean: %s' % database_selected, xbmc.LOGINFO)

	if os.path.exists(database_selected):
		database_size_before = Size_Convert(os.path.getsize(database_selected))
		try:
			textdb = sqlite3.connect(database_selected)
			textexe = textdb.cursor()

		except Exception as e:
			Log(Log_Title + Db + 'database connection error: %s[CR]%s' % (database_selected, str(e)), xbmc.LOGERROR)
			return False

	else:
		Log(Log_Title + Db + 'database not found: %s' % database_selected, xbmc.LOGERROR)
		return False

	textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	for table in textexe.fetchall():
		if table[0] == 'version':
			Log(Log_Title + Db + 'database table skipped: %s' % table[0], xbmc.LOGINFO)

		else:
			try:
				textexe.execute("DELETE FROM %s" % table[0])
				textdb.commit()
				Log(Log_Title + Db + 'database table data cleared: %s' % table[0], xbmc.LOGINFO)

			except Exception as e:
				Log(Log_Title + Db + 'database remove table error: %s[CR]%s' % (table[0], str(e)), xbmc.LOGERROR)

	database_path = database_selected.replace('\\', '/').split('/')
	database = ('[COLOR %s] > %s > [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, database_path[len(database_path)-2], TEXT_DARK, database_path[len(database_path)-1]))
	textexe.close()
	database_bytes = os.path.getsize(database_selected)
	database_size = Size_Convert(database_bytes)

	if ADDON.getSetting('NOTIFICATIONS') == 'true':
		Notification(Addon_Title, '[COLOR %s]Clean Databases: %s[/COLOR]' % (TEXT_GENERAL, database))
	if ADDON.getSetting('DIALOGUE_BOXES') == 'true':
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Databases: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]%s[/COLOR]%s[COLOR %s][LIGHT] (%s)[/LIGHT][/COLOR][CR]%s[/COLOR]' % (TEXT_GENERAL, (TEXT_VALUE if database_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size, database, TEXT_DARK, database_size_before, database_selected))
	Log(Log_Title + Db + 'clean: %s done' % database_selected, xbmc.LOGINFO)

# ============================================================
# FUNCTION: Database_Count
# ============================================================

def Database_Count():

	database_count = 0
	thumbs_count = 0

	for _, _, files in os.walk(HOME):
		database_count += sum(1 for file in files if file.endswith('.db'))
		thumbs_count += files.count('Thumbs.db')

	return database_count, thumbs_count

# ============================================================
# FUNCTION: Database_Files
# ============================================================

def Database_Files():

	database_paths = []

	for root, _, files in os.walk(HOME):
		for file in fnmatch.filter(files, '*.db'):
			database_path = os.path.join(root, file)
			database_bytes = os.path.getsize(database_path)
			database_size = Size_Convert(database_bytes)
			database_paths.append('[COLOR %s]%s[/COLOR][COLOR %s] > [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, database_path, TEXT_DIM, (TEXT_VALUE if database_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size))
			database_paths.sort(key = lambda v: v.upper())

	database = "\n\n".join(database_paths) if SPACER_ROW == 'true' else "\n".join(database_paths)

	database_count, thumbs_count = Database_Count()

	Database_Files_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Full Path / Database Size)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('DATABASE FILES'), TEXT_VALUE, TEXT_GENERAL, database)

	TextBox('[B]%s[/B][CR][COLOR %s]Databases: [/COLOR][COLOR %s]%s  [/COLOR][COLOR %s][LIGHT]Thumbs.db files: [/COLOR][COLOR %s]%s[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, database_count, TEXT_ITEM, TEXT_VALUE, thumbs_count), Database_Files_Text)

#####################################################################################

# ============================================================
# Menu Entry Point
# ============================================================

if '/Addon_Header' in PLUGIN_URL:
	ADDON.openSettings()

elif '/Clean_Addons_Database' in PLUGIN_URL:
	Clean_Addons_Database()

elif '/Databases_Addon_Data' in PLUGIN_URL:
	Clean_Databases(ADDON_DATA_PATH)

elif '/Databases_Addons' in PLUGIN_URL:
	Clean_Databases(ADDONS_PATH)

elif '/Databases_Database' in PLUGIN_URL:
	Clean_Databases(DATABASE_PATH)

elif '/Databases_Home' in PLUGIN_URL:
	Clean_Databases(HOME_PATH)

elif '/Databases_Userdata' in PLUGIN_URL:
	Clean_Databases(USERDATA_PATH)

elif '/Database_Files' in PLUGIN_URL:
	Database_Files()

elif '/Exit_Only' in PLUGIN_URL:
	xbmc.executebuiltin('Action(Back)')
	Log(Log_Title + Menu + '[COLOR %s][LIGHT]Finished (Exit Only)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

elif '/User_Information' in PLUGIN_URL:
	User_Information()

else:
	# Create the menu items.
	Log(Log_Title + Menu + '[COLOR %s][LIGHT]Started[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)
	xbmcplugin.setContent(PLUGIN_ID, 'files')
	
	Equals = xbmcgui.ListItem('[COLOR %s]==================================================[/COLOR]' % TEXT_DIM)
	Equals.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_FANART})

	Addon_Header = xbmcgui.ListItem('[B]%s[/B]%s' % (Addon_Title, ' '.join('  Settings >')))
	Addon_Header.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Clean_Addons_Database = xbmcgui.ListItem('Clean Addons Database  >')
	Clean_Addons_Database.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Databases_Addon_Data = xbmcgui.ListItem('[COLOR %s]Clean Databases (folder)[/COLOR]: addon_data  >' % TEXT_DARK)
	Databases_Addon_Data.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Databases_Addons = xbmcgui.ListItem('[COLOR %s]Clean Databases (folder)[/COLOR]: addons  >' % TEXT_DARK)
	Databases_Addons.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Databases_Database = xbmcgui.ListItem('[COLOR %s]Clean Databases (folder)[/COLOR]: database  >' % TEXT_DARK)
	Databases_Database.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Databases_Home = xbmcgui.ListItem('[COLOR %s]Clean Databases (folder)[/COLOR]: home [COLOR %s](all databases)[/COLOR]  >' % (TEXT_DARK, TEXT_DARK))
	Databases_Home.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Databases_Userdata = xbmcgui.ListItem('[COLOR %s]Clean Databases (folder)[/COLOR]: userdata [COLOR %s](all excluding addons)[/COLOR]  >' % (TEXT_DARK, TEXT_DARK))
	Databases_Userdata.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Database_Files = xbmcgui.ListItem('Database Files [COLOR %s](.db file list)[/COLOR]  >' % TEXT_DARK)
	Database_Files.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Exit_Only = xbmcgui.ListItem('Exit Only  >')
	Exit_Only.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	User_Information = xbmcgui.ListItem(' '.join('User Information >'))
	User_Information.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Addon_Developer = xbmcgui.ListItem('[COLOR %s]Developer: [/COLOR]%s' % (TEXT_DIM, ADDON_DEVELOPER))
	Addon_Developer.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Name = xbmcgui.ListItem('[COLOR %s]Name: %s[/COLOR]' % (TEXT_DIM, ADDON_NAME))
	Addon_Name.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Version = xbmcgui.ListItem('[COLOR %s]Version: %s[/COLOR]' % (TEXT_DIM, ADDON_VERSION))
	Addon_Version.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_ID = xbmcgui.ListItem('[COLOR %s]Add-on ID: %s[/COLOR]' % (TEXT_DIM, ADDON_ID))
	Addon_ID.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	# Append to PLUGIN_URL as it already ends with a slash.
	xbmcplugin.addDirectoryItems(
		PLUGIN_ID,
		(
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'Addon_Header', Addon_Header, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'Clean_Addons_Database', Clean_Addons_Database, False),
			(PLUGIN_URL + 'Databases_Addon_Data', Databases_Addon_Data, False),
			(PLUGIN_URL + 'Databases_Addons', Databases_Addons, False),
			(PLUGIN_URL + 'Databases_Database', Databases_Database, False),
			(PLUGIN_URL + 'Databases_Home', Databases_Home, False),
			(PLUGIN_URL + 'Databases_Userdata', Databases_Userdata, False),
			(PLUGIN_URL + 'Database_Files', Database_Files, False),
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