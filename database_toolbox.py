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
ADDON_DATA = xbmcvfs.translatePath('special://userdata/addon_data')
ADDON_DEVELOPER = ADDON.getAddonInfo('author') # provider-name in addons.xml (developer)
ADDON_FANART = ADDON.getAddonInfo('fanart')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name') # name in addons.xml
ADDON_VERSION = ADDON.getAddonInfo('version') # version in addons.xml
ADDONS = xbmcvfs.translatePath('special://home/addons')
DATABASE = xbmcvfs.translatePath('special://database/')
HOME = xbmcvfs.translatePath('special://home/')
NOTIFICATION_DURATION = ADDON.getSetting('notification_duration')
PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
SIZE_HIGHLIGHT = ADDON.getSetting('size_highlight')
TEXT_ADDON = ADDON.getSetting('text_addon')
TEXT_DARK = ADDON.getSetting('text_dark')
TEXT_DIM = ADDON.getSetting('text_dim')
TEXT_GENERAL = ADDON.getSetting('text_general')
TEXT_HIGHLIGHT = ADDON.getSetting('text_highlight')
TEXT_ITEM = ADDON.getSetting('text_item')
TEXT_VALUE = ADDON.getSetting('text_value')
TOOLBOX = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', 'toolbox.png')
USERDATA = xbmcvfs.translatePath('special://userdata/')

# ============================================================
# Addon_ID_Version / Addon_Title / Dialogue / Log_Title
# ============================================================

Addon_ID_Version = ('[COLOR %s]%s [/COLOR][COLOR %s] %s[/COLOR]' % (TEXT_ITEM, ADDON_ID, TEXT_VALUE, ADDON_VERSION))
Addon_Title = ('[COLOR %s]%s[/COLOR]' % (TEXT_ADDON, ' '.join((ADDON_NAME).strip(' '))))
Dialogue = xbmcgui.Dialog()
Log_Title = ('[COLOR %s]%s [/COLOR]' % (TEXT_ADDON, ADDON_NAME))

# ============================================================
# Addons / Arrow / Clean_db / Delete_db / Menu
# ============================================================

Addons = ('[COLOR %s]addons > [/COLOR]' % TEXT_GENERAL)
Arrow = '[COLOR %s] > [/COLOR]' % TEXT_DIM
Clean_db = ('[COLOR %s]clean db > [/COLOR]' % TEXT_GENERAL)
Delete_db = ('[COLOR %s]delete db > [/COLOR]' % TEXT_GENERAL)
Menu = ('[COLOR %s]menu > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: DialogueSelect
# ============================================================

def DialogueSelect(list, title = Addon_Title):
	return Dialogue.select(title, list)

# ============================================================
# FUNCTION: Log
# ============================================================

def Log(message, level = xbmc.LOGDEBUG):
	xbmc.log(message, level = level)

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

def TextBox(title, text):
	class TextBoxes(xbmcgui.WindowXMLDialog):

		def onAction(self, action):
			if action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

		def onClick(self, controlId):
			if (controlId == self.close_button):
				self.close()
			elif controlId != self.close_button:
				self.noop = lambda: None

		def onInit(self): # group = 8000, background = 8100, noop = 8181
			self.title = 8200
			self.text = 8300
			self.scrollbar = 8400
			self.close_button = 8500
			self.noop = lambda: None
			self.showDialog()

		def showDialog(self):
			close = '[COLOR %s]Close[/COLOR]' % TEXT_GENERAL
			self.getControl(self.title).setLabel(title)
			self.getControl(self.close_button).setLabel(close)
			self.getControl(self.text).setText(text)
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

INSTRUCTIONS_TEXT = '%s[CR][CR]Open the add-on to access the menu.[CR]Click on \'User Interface >\' to open the user interface.[CR][CR]\'Addons*.db: Clean Addons Database\' has a \'Would you like to continue ?\' option to exit before processing begins (see \'%s\' below).[CR]\'Addons*.db: View Raw Tables\' displays content of Addons*.db table selected for analysis.[CR]\'Addon data: Clean Database [LIGHT]//userdata/addon_data/[/LIGHT]\' select one or more to clean.[CR]\'Addon data: Delete Database [LIGHT]//userdata/addon_data/[/LIGHT]\' select one or more to delete.[CR]\'Database: Clean Database [LIGHT]//database/[/LIGHT]\' select one or more to clean.[CR]\'Userdata: Clean Database [LIGHT]//userdata/[/LIGHT]\' select one or more to clean. Includes all databases in addon_data and database[CR]\'Database Files [LIGHT] (.db file list)[/LIGHT]\' list of databases (full path and database size) includes all Kodi databases and a separate total for Thumbs.db files.[CR]\'Database Toolbox: User Information\'[CR][CR]\'Exit Menu >\' exits the add-on.' % (' '.join('INSTRUCTIONS'), ' '.join('NOTES'))

NOTES_TEXT = '[CR][CR][CR]%s[CR][CR]It is important to proceed carefully so changes can be reversed if necessary i.e. \'Clean Addons Database\' closes Kodi without cleanup at the end.[CR][CR]• Backup databases using Kodi file manager or a backup add-on.[CR]• Close other add-ons and save any changes.[CR]• Restart Kodi if required.[CR][CR]ln everyday use the Textures13.db can get corrupted and prevent Kodi starting. Deleting the Textures13.db database resolves this as it rebuilds on startup.[CR]Other databases such as the add-ons database do not rebuild and may require restoring from backup if startup fails.[CR][CR]Later versions of Android make restoring a backedup database difficult.[CR]Android prevents users accessing the Data folder containing data for all the installed apps including Kodi and its databases.[CR]Access is possible using a file explorer app from the Play Store such as Total Commander.[CR]The app needs to be used with the Shizuku app from the Play Store or if restricted from GitHub https://github.com/RikkaApps/Shizuku[CR]Alternative Android apps that work from time to time (depending on version of app and Android OS / device) include FV File Explorer and X-plore apps.' % ' '.join('NOTES')

SETTINGS_TEXT = '[CR][CR][CR]%s[CR][CR]Press the OK button in settings to save any changes made and after resetting a category to default.[CR]Some changes may require restarting the add-on.[CR][CR]Clean Database / Delete Database set dialogue boxes on / off[CR]Clean Databases / Delete Database set notifications on / off[CR]Notification Duration[CR]Size Highlight above value set (default = 1048576 i.e. 1 MB)[CR][CR]Customise text colours with billions of text colour combinations[CR][CR]Choose from 140 colours for each one (there is also a none option):[CR]Text Add-on Colour: header (menu, notifications, logs and text boxes)[CR]Text Dark Colour: logs and text boxes[CR]Text Dim Colour: menu[CR]Text General Colour: main text (notifications, logs, text boxes and close button)[CR]Text Highlight Colour: values on menu requiring attention and logs[CR]Text Item Colour: items on menu and text boxes[CR]Text Value Colour: values on menu and text boxes' % ' '.join('SETTINGS')

ENVIRONMENT_TEXT = '[CR][CR][CR]%s[CR][CR]Kodi v21.3 Omega apk (Android app) with Confluence skin as default (including default font).[CR]Tablet (1340 x 800 aspect ratio 5:3) running Android 14 using QuickEdit apk (TryItAndSee / LearnAsYouGo iterative development and testing).[CR]Chromecast HD (1280 x 720 aspect ratio 16:9) running Android TV OS version 14 (user testing).[CR]100%% tested and working on Android.[CR]Not tested on other platforms.[CR]Code debugged and reengineered using https://aipy.dev/tools where required (pre 2.10.0).[CR]Code debugged and reengineered using https://stackoverflow.com/ai-assist (2.10.0 onwards).' % ' '.join('DEVELOPMENT ENVIRONMENT')

CHANGELOG_TEXT = '[CR][CR][CR]%s[LIGHT] (newest at the top)[/LIGHT][CR][CR]Version code x.y.z attributes[CR]x = major change / y = number of \'>\' menu items / z = minor change[CR][CR]version 3.4.0 (4 menu items)[CR]- menu simplified (based on Reorder Favourites 2.4.0)[CR]- options consolidated with improved code (developed for Maintenance Toolbox 2.4.0 initial release)[CR]- added Addons*.db View Raw Tables and Delete Database from //userdata/addon_data/[CR][CR]version 2.10.3 (10 menu items)[CR]- settings reworked to avoid clashes (different names to variables etc.)[CR]- minor changes to TextBox.xml to improve performance and consistency with other add-ons[CR]- minor changes to Log and TextBox functions to improve consistency with other add-ons[CR][CR]version 2.10.2 (10 menu items)[CR]- Clean Addons Database futureproofing added to select Addons*.db[CR]- minor changes to menu formatting[CR][CR]version 2.10.1 (10 menu items)[CR]- added text colour customisation to text boxes and buttons[CR]- added pre clean database size to dialogue boxes (\'Clean Databases (folder)\' options)[CR]- database information formatting reworked and renamed \'Database Files (.db file list) >\'[CR]- added size highlight above value set in settings[CR]- minor changes to improve consistency with other add-ons[CR][CR]version 2.10.0 (10 menu items)[CR]- code added from OpenWizard 2.0.7 by drinfernoo & slamious (plugin.program.openwizard)[CR]- Clean Databases created[CR]- Database Information created[CR]- variables and functions reworked[CR]- menu, multiselect dialogue boxes and logs reworked[CR]- user information updated including instructions and notes[CR]- added user settings for dialogue boxes, notifications, notification duration and trillions of text colour combinations[CR][CR]version 1.3.1 (3 menu items)[CR]- database variable added[CR]- dialogue boxes and logs reworked[CR]- user information updated including instructions and notes[CR][CR]version 1.3.0 (3 menu items)[CR]- initial code from Abacus Program 1.0.0 by %s (plugin.program.code-e-magpie)[CR]- code added from Truncate Tables 1.0.1 by The Cleaner (plugin.program.truncatetables)[CR]- Clean Addons Database created[CR]- icon.png changed and toolbox.png added[CR]- variables and functions reworked[CR]- menu, dialogue boxes and logs reworked[CR]- user information added (instructions, notes, development and changelog)' % (' '.join('CHANGELOG'), ADDON_DEVELOPER)

User_Information_Text = '[COLOR %s][B]%s[/B][CR][COLOR %s][LIGHT](Instructions / Notes / Settings / Development Environment / Changelog)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('USER INFORMATION'), TEXT_VALUE, TEXT_GENERAL, (INSTRUCTIONS_TEXT + NOTES_TEXT + SETTINGS_TEXT + ENVIRONMENT_TEXT + CHANGELOG_TEXT))

def User_Information():
	TextBox('[B]%s[/B][CR]%s' % (Addon_Title, Addon_ID_Version), User_Information_Text + Development_Text)

#####################################################################################

# ============================================================
# FUNCTION: Add_Blank
# ============================================================

def Add_Blank():

	choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Common Function: [LIGHT](Add Blank)[CR][COLOR %s] > Add Blank row between each new line.[CR] > No Blank row between each new line.[/LIGHT][/COLOR][CR]Add a blank row between each new line ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]No Blank[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Add Blank[/COLOR]' % TEXT_HIGHLIGHT))

	if choice == 0:
		blank = 'true'
	else:
		blank = 'false'

	return blank

# ============================================================
# FUNCTION: Addon_Files
# ============================================================

def Addon_Files(file_type):

	files_mapping = {"cache": HOME, "database": HOME, "fanart": ADDONS, "icon": ADDONS, "thumbs": HOME}
	files_mapping_type = {"cache": '*cache*.db', "database": '*.db', "fanart": 'fanart.jpg', "icon": 'icon.png'}
	files_type = {"cache": 'CACHE DATABASES', "database": 'DATABASE FILES', "fanart": 'FANART FILES', "icon": 'ICON FILES'}

	try:
		path = files_mapping[file_type]
		pattern = files_mapping_type[file_type]
		title = files_type[file_type]

	except KeyError:
		Log(Log_Title + Footer + 'add-on files name error: %s' % file_type, xbmc.LOGERROR)
		return

	database_count, thumbs_count = Database_Count()
	file_paths = []

	for root, _, files in os.walk(path):
		for fname in fnmatch.filter(files, pattern):
			file_path = os.path.join(root, fname)
			file_bytes = os.path.getsize(file_path)
			file_size = Size_Convert(file_bytes)
			file_paths.append('[COLOR %s]%s[/COLOR]%s[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, file_path, Arrow, (TEXT_VALUE if file_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), file_size))

	file_count = len(file_paths)
	file_paths.sort(key = lambda v: v.upper())

	blank = Add_Blank()
	column_text = '[COLOR %s]Path %s Size[/COLOR]' % (TEXT_GENERAL, Arrow)
	column = column_text + "\n\n" if blank == 'true' else column_text + "\n"
	file = "\n\n".join(file_paths) if blank == 'true' else "\n".join(file_paths)

	Files_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: /%s)[/LIGHT][/COLOR][CR][CR]%s[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join(title), TEXT_VALUE, path, '' if file_count == 0 else column, TEXT_GENERAL, ('None found.' if file_count == 0 else file))
	TextBox('[B]%s[/B][CR][COLOR %s]%s: [/COLOR][COLOR %s]%s  [/COLOR]' % (Addon_Title, TEXT_ITEM, title.title(), TEXT_VALUE, file_count) + ('[COLOR %s][LIGHT]Thumbs.db files: [/COLOR][COLOR %s]%s[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_VALUE, thumbs_count) if file_type == 'database' else ''), Files_Text)

# ============================================================
# FUNCTION: Addons_Db
# ============================================================

def Addons_Db():
	
	pattern = re.compile(r'Addons(\d+)\.db$', re.IGNORECASE)
	database_matches = glob.glob(os.path.join(DATABASE, 'Addons*.db'))
	highest = 0

	for database in database_matches:
		basename = os.path.basename(database)
		database_match = pattern.search(basename)
		if database_match:
			try:
				number = int(database_match.group(1))
			except ValueError:
				continue
			if number > highest:
				highest = number

	addons_db = "Addons%s.db" % highest
	return addons_db

# ============================================================
# FUNCTION: Addons_Tables
# ============================================================

def Addons_Tables(table_name):

	table_addonlinkrepo = "SELECT * FROM addonlinkrepo ORDER BY idRepo ASC, idAddon ASC"
	table_addons = "SELECT id, addonID, version FROM addons ORDER BY LOWER(addonID) ASC, id ASC"
	table_installed = "SELECT * FROM installed ORDER BY LOWER(addonID) ASC"
	table_package = "SELECT * FROM package ORDER BY LOWER(addonID) ASC, LOWER(filename) DESC"
	table_repo = "SELECT * FROM repo ORDER BY LOWER(addonID) ASC"
	table_update_rules = "SELECT * FROM update_rules ORDER BY LOWER(addonID) ASC"
	table_version = "SELECT * FROM version ORDER BY LOWER(idVersion) ASC"

	addons_db = Addons_Db()
	table_mapping = {"addonlinkrepo": table_addonlinkrepo, "addons": table_addons, "installed": table_installed, "package": table_package, "repo": table_repo, "update_rules": table_update_rules, "version": table_version}

	try:
		table = table_mapping[table_name]

	except KeyError:
		Log(Log_Title + Footer + 'table name error: %s' % table_name, xbmc.LOGERROR)

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		table_count = "SELECT COUNT (*) FROM %s" % table_name
		cursor.execute(table_count)
		table_count = cursor.fetchall()
		table_count = int(str(table_count)[2: -3])

		cursor.execute("PRAGMA table_info(%s);" % table_name)
		columns_info = cursor.fetchall()

		cursor.execute(table)
		table = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if cursor:
				cursor.close()
		except Exception:
			pass
		try:
			if connection:
				connection.close()
		except Exception:
			pass

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	column_text = [column[1] for column in columns_info]
	column = str(column_text).replace("['", "").replace("']", ("\n\n" if blank == 'true' else "\n")).replace("', '", (" " + Arrow + " "))
	column_addons_text =  '[COLOR %s]id %s addonID %s version[/COLOR]' % (TEXT_GENERAL, Arrow, Arrow)
	column_addons = column_addons_text + "\n\n" if blank == 'true' else column_addons_text + "\n"
	table = str(table).replace("[('","").replace("[(","").replace("')]","").replace(")]","").replace("'), (",("\n\n" if blank == 'true' else "\n")).replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("), ('",("\n\n" if blank == 'true' else "\n")).replace("), (",("\n\n" if blank == 'true' else "\n")).replace("', '", Arrow).replace("', ", Arrow).replace(", '", Arrow).replace(", ", Arrow)

	Tables_Text = '[COLOR %s][B]%s[/B][/COLOR][COLOR %s][LIGHT][CR](Data Source: /%s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s%s[/COLOR]' % (TEXT_ITEM, ' '.join(table_name).upper(), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, column if table_name != 'addons' else column_addons, table if table_count != 0 else 'No lines in %s table.' % table_name)
	TextBox('[B]%s[/B][CR][COLOR %s]%s table: [/COLOR][COLOR %s]%s[LIGHT] lines[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, table_name, TEXT_VALUE, table_count), Tables_Text)

# ============================================================
# FUNCTION: Clean_Addons_Database
# ============================================================

def Clean_Addons_Database():

	addons_db = Addons_Db()
	success = False

	Log(Log_Title + Addons + '[COLOR %s][LIGHT]Started (addons database: //database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)

	Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Close other add-ons and save any changes.[CR]Restart Kodi if required.[/LIGHT][/COLOR][CR]Backup %s database before proceeding.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, addons_db))

	addons_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]%s clean (empty) tables except installed and version.[CR]Kodi will need to close without cleanup at the end.[/LIGHT][/COLOR][CR]Would you like to continue ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, addons_db), yeslabel = ('[COLOR %s]Clean Database[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Cancel Clean[/COLOR]' % TEXT_HIGHLIGHT))

	if not addons_choice:
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Cancelled (addons database: //database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		return False # replaced sys.exit()

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		cursor.execute('DELETE FROM addonlinkrepo;')
		cursor.execute('DELETE FROM addons;')
		cursor.execute('DELETE FROM package;')
		cursor.execute('DELETE FROM repo;')
		cursor.execute('DELETE FROM update_rules;')

		connection.commit()
		success = True

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to clean addons database: [COLOR %s]%s[/COLOR][CR]The database is locked or may not exist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + '%s read error %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return False

	finally:
		try:
			if cursor is not None:
				try:
					cursor.close()
				except Exception as e:
					Log(Log_Title + Addons + '%s cursor close error %s' % (addons_db, str(e)), xbmc.LOGERROR)
		finally:
			try:
				if connection is not None:
					try:
						connection.close()
					except Exception as e:
						Log(Log_Title + Addons + '%s connection close error %s' % (addons_db, str(e)), xbmc.LOGERROR)
			except Exception:
				pass

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		cursor.execute('VACUUM;')

		connection.commit()
		Log(Log_Title + Addons + 'Clean Addons Database: vacuumed [LIGHT] (%s)[/LIGHT]' % addons_db, xbmc.LOGINFO)

	except sqlite3.Error as e:
		Log(Log_Title + Addons + '%s vacuum error %s' % (addons_db, str(e)), xbmc.LOGERROR)

	finally:
		if cursor is not None:
			try:
				cursor.close()
			except Exception:
				pass
		if connection is not None:
			try:
				connection.close()
			except Exception:
				pass

	if success:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Cleaned addons database: [COLOR %s]%s[/COLOR][CR]Kodi will need to close without cleanup.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Finished (addons database: //database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		xbmc.executebuiltin('Quit')
#	replaced os._exit(1) with xbmc.executebuiltin('Quit') could use return True
	return False

# ============================================================
# FUNCTION: Clean_Database
# ============================================================

def Clean_Database(database_selected):

	Log(Log_Title + Clean_db + '[COLOR %s][LIGHT]Started (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)

	if not os.path.exists(database_selected):
		Log(Log_Title + Clean_db + '%s not found' % database_selected, xbmc.LOGERROR)
		return False

	database_path = database_selected.replace('\\', '/').split('/')
	database_name = database_path[-1]
	database_text = ('[COLOR %s] > %s > [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, database_path[-2] if len(database_path) >= 2 else '', TEXT_DARK, database_name))

	database_bytes = os.path.getsize(database_selected)
	database_size = Size_Convert(database_bytes)

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(database_selected)
		cursor = connection.cursor()

		cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
		tables = [row[0] for row in cursor.fetchall()]

		if not tables:
			Log(Log_Title + Clean_db + '%s no user tables found' % database_selected, xbmc.LOGINFO)
			return True

		for table in tables:
			if table == 'version':
				Log(Log_Title + Clean_db + '%s table skipped' % table, xbmc.LOGINFO)
				continue

			if not table.replace('_', '').isalnum():
				Log(Log_Title + Clean_db + '%s invalid table name skipped' % table, xbmc.LOGERROR)
				continue

			try:
				safe_table = table.replace('"', '""')
				sql = 'DELETE FROM "{}"'.format(safe_table)
				cursor.execute(sql)
				Log(Log_Title + Clean_db + '%s table cleaned [LIGHT](emptied)[/LIGHT]' % table, xbmc.LOGINFO)

			except Exception as e:
				Log(Log_Title + Clean_db + '%s remove table error %s' % (table, str(e)), xbmc.LOGERROR)

		connection.commit()

	except sqlite3.Error as e:
		Log(Log_Title + Clean_db + '%s connection error %s' % (database_selected, str(e)), xbmc.LOGERROR)
		return False

	finally:
		if cursor is not None:
			try:
				cursor.close()
			except Exception as e:
				Log(Log_Title + Clean_db + '%s cursor close error %s' % (database_selected, str(e)), xbmc.LOGERROR)
		if connection is not None:
			try:
				connection.close()
			except Exception as e:
				Log(Log_Title + Clean_db + '%s connection close error %s' % (database_selected, str(e)), xbmc.LOGERROR)

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(database_selected)
		cursor = connection.cursor()

		cursor.execute("VACUUM;")

		connection.commit()

		Log(Log_Title + Clean_db + 'vacuumed %s' % database_name, xbmc.LOGINFO)

	except sqlite3.Error as e:
		Log(Log_Title + Clean_db + '%s vacuum error %s' % (database_selected, str(e)), xbmc.LOGERROR)

	finally:
		try:
			if cursor is not None:
				cursor.close()
		except Exception:
			pass
		try:
			if connection is not None:
				connection.close()
		except Exception:
			pass

	database_bytes_after = os.path.getsize(database_selected)
	database_size_after = Size_Convert(database_bytes_after)

	Log(Log_Title + Clean_db + 'vacuumed reduction %s [LIGHT](start %s  finish %s)[/LIGHT]' % (Size_Convert(database_bytes - database_bytes_after), database_size, database_size_after), xbmc.LOGINFO)

	if ADDON.getSetting('notifications') == 'true':
		Notification(Addon_Title, '[COLOR %s]Clean Database: %s[/COLOR]' % (TEXT_GENERAL, database_text))
	if ADDON.getSetting('dialogue_boxes') == 'true':
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]%s[/COLOR]%s[COLOR %s][LIGHT] (%s)[/LIGHT][/COLOR][CR]%s[/COLOR]' % (TEXT_GENERAL, (TEXT_VALUE if database_bytes_after < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size_after, database_text, TEXT_DARK, database_size, database_selected))

	Log(Log_Title + Clean_db + '[COLOR %s][LIGHT]Finished (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)
	return True

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
# FUNCTION: Delete_Database
# ============================================================

def Delete_Database(database_selected):

	Log(Log_Title + Delete_db + '[COLOR %s][LIGHT]Started (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)

	database_path = database_selected.replace('\\', '/').split('/')
	database_name = database_path[-1]
	database_text = ('[COLOR %s] > %s > [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, database_path[-2] if len(database_path) >= 2 else '', TEXT_DARK, database_name))

	database_bytes = os.path.getsize(database_selected)
	database_size = Size_Convert(database_bytes)

	if not os.path.exists(database_selected):
		Log(Log_Title + Delete_db + '%s not found' % database_selected, xbmc.LOGERROR)
		return False

	try:
		os.remove(database_selected)

		Log(Log_Title + Delete_db + '//%s deleted' % database_selected, xbmc.LOGINFO)

		if ADDON.getSetting('notifications') == 'true':
			Notification(Addon_Title, '[COLOR %s]Delete Database: %s[/COLOR]' % (TEXT_GENERAL, database_text))
		if ADDON.getSetting('dialogue_boxes') == 'true':
			Dialogue.ok(Addon_Title, '[COLOR %s]Delete Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]0.00 B[/COLOR]%s[COLOR %s][LIGHT] (%s)[/LIGHT][/COLOR][CR]%s[/COLOR]' % (TEXT_GENERAL, TEXT_VALUE, database_text, TEXT_DARK, database_size, database_selected))

	except OSError as e:
		Log(Log_Title + Delete_db + 'Delete Database: error %s %s' % (database_name, str(e)), xbmc.LOGINFO)

	Log(Log_Title + Delete_db + '[COLOR %s][LIGHT]Finished (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)
	return True

# ============================================================
# FUNCTION: Select_Database
# ============================================================

def Select_Database(folder_path, mode):

	databases = []

	for root, dirs, files in os.walk(xbmcvfs.translatePath(folder_path)):
		for file in fnmatch.filter(files, '*.db'):
			if file == 'Thumbs.db':
				continue

			database_path = os.path.join(root, file)
			database_bytes = os.path.getsize(database_path)
			database_size = Size_Convert(database_bytes)
			path = database_path.replace('\\', '/').split('/')
			display = '[COLOR %s]%s > [/COLOR]%s [COLOR %s]> [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, path[-2], path[-1], TEXT_DIM, (TEXT_VALUE if database_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size)
			databases.append((display, database_path))

	databases.sort(key = lambda t: t[0].upper())
	database_paths = [t[0] for t in databases]
	database_files = [t[1] for t in databases]

	choice = Dialogue.multiselect(Addon_Title + "[COLOR %s][LIGHT]   (select one or more from the list)[/LIGHT][/COLOR]" % TEXT_GENERAL, database_paths, 0, [], False)

	if not choice:
		return

	for database_selected in choice:
		if mode == 'clean_database':
			Clean_Database(database_files[database_selected])
		elif mode == 'delete_database':
			Delete_Database(database_files[database_selected])

# ============================================================
# FUNCTION: The_Menu
# ============================================================

def The_Menu():

	database_menu = ['[COLOR %s]%s:[/COLOR] Clean Addons Database' % (TEXT_DARK, Addons_Db()), '[COLOR %s]%s:[/COLOR] View Raw Tables [COLOR %s][LIGHT] (for analysis)[/LIGHT][/COLOR]' % (TEXT_DARK, Addons_Db(), TEXT_DIM), '[COLOR %s]Addon data:[/COLOR] Clean Database [LIGHT]//userdata/addon_data/[/LIGHT]' % TEXT_DARK, '[COLOR %s]Addon data:[/COLOR] Delete Database [LIGHT]//userdata/addon_data/[/LIGHT]' % TEXT_DARK, '[COLOR %s]Database:[/COLOR] Clean Database [LIGHT]//database/[/LIGHT]' % TEXT_DARK, '[COLOR %s]Userdata:[/COLOR] Clean Database [LIGHT]//userdata/[/LIGHT]' % TEXT_DARK, 'Database Files [COLOR %s][LIGHT] (.db file list)[/LIGHT][/COLOR]' % TEXT_DIM, '[COLOR %s]Database Toolbox: [/COLOR]User Information' % TEXT_DARK]

	table_menu = ['< < <  [COLOR %s][LIGHT]back to menu[/LIGHT][/COLOR]' % TEXT_DIM, 'addonlinkrepo [COLOR %s][LIGHT] (sort idRepo asc > idAddon asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'addons [COLOR %s][LIGHT] (only 3 columns sort addonID asc > id asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'installed [COLOR %s][LIGHT] (sort addonID asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'package [COLOR %s][LIGHT] (sort addonID asc > filename desc)[/LIGHT][/COLOR]' % TEXT_DIM, 'repo [COLOR %s][LIGHT] (sort addonID asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'update_rules [COLOR %s][LIGHT] (sort addonID asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'version [COLOR %s][LIGHT] (sort idVersion asc)[/LIGHT][/COLOR]' % TEXT_DIM] 

	database = DialogueSelect(database_menu)
	if database == 0: Clean_Addons_Database()
	elif database == 1: # Addons#.db Tables
		table = DialogueSelect(table_menu)
		if table == 0: The_Menu() # < < <  back to menu
		elif table == 1: Addons_Tables('addonlinkrepo')
		elif table == 2: Addons_Tables('addons')
		elif table == 3: Addons_Tables('installed')
		elif table == 4: Addons_Tables('package')
		elif table == 5: Addons_Tables('repo')
		elif table == 6: Addons_Tables('update_rules')
		elif table == 7: Addons_Tables('version')
	elif database == 2: Select_Database(ADDON_DATA, 'clean_database')
	elif database == 3: Select_Database(ADDON_DATA, 'delete_database')
	elif database == 4: Select_Database(DATABASE, 'clean_database')
	elif database == 5: Select_Database(USERDATA, 'clean_database')
	elif database == 6: Addon_Files('database')
	elif database == 7: User_Information()

#####################################################################################

# ============================================================
# Menu Entry Point
# ============================================================

if '/Addon_Header' in PLUGIN_URL:
	ADDON.openSettings()

elif '/User_Interface' in PLUGIN_URL:
	The_Menu()

elif '/Exit_Menu' in PLUGIN_URL:
	xbmc.executebuiltin('Action(Back)')

elif '/User_Information' in PLUGIN_URL:
	User_Information()

else:
	xbmcplugin.setContent(PLUGIN_ID, 'files')
	
	Equals = xbmcgui.ListItem('[COLOR %s]==================================================[/COLOR]' % TEXT_DIM)
	Equals.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_FANART})

	Addon_Header = xbmcgui.ListItem('[B]%s[/B]%s' % (Addon_Title, ' '.join('  Settings >')))
	Addon_Header.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	User_Interface = xbmcgui.ListItem('[B]%s[/B]' % ' '.join('User Interface >'))
	User_Interface.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Exit_Menu = xbmcgui.ListItem(' '.join('Exit Menu >'))
	Exit_Menu.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

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

	# Append to PLUGIN_URL as it already ends with a slash
	xbmcplugin.addDirectoryItems(
		PLUGIN_ID,
		(
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'Addon_Header', Addon_Header, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'User_Interface', User_Interface, False),
			(PLUGIN_URL + 'Exit_Menu', Exit_Menu, False),
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