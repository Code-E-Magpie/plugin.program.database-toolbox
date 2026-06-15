# Database Toolbox for Kodi

![icon](https://github.com/Code-E-Magpie/plugin.program.database-toolbox/blob/main/resources/media/icon.png)

Easy to use database toolbox to maintain Kodi database files in a small package.


# Instructions
Open the add-on to access the menu.

Select one of the '>' menu items and follow the user information.

A 'Would you like to continue ?' option is provided to exit the item before processing begins.

'Exit Only >' - exits the add-on.


# Notes
It is important to proceed carefully so changes can be reversed if necessary e.g. 'Clean Addons Database  >' closes Kodi without cleanup at the end.

• Backup databases using file manager or a backup add-on.

• Close other add-ons and save any changes.

• Restart Kodi if required.


ln everyday use the Textures13.db can get corrupted and prevent Kodi starting. Deleting the Textures13.db database resolves this as it rebuilds on startup.<br>Other databases such as the add-ons database do not rebuild and may require restoring from backup if startup fails.


Later versions of Android make restoring a backedup database difficult.
Android prevents users accessing the Data folder containing data for all the installed apps including Kodi and its databases.

Access is possible using a file explorer app from the Play Store such as Total Commander.<br>The app needs to be used with the Shizuku app from the Play Store or if restricted from GitHub https://github.com/RikkaApps/Shizuku


# Development
Kodi v21.3 Omega apk (Android app) with Confluence skin as default (including default font).

Tablet (1340 x 800 aspect ratio 5:3) running Android 14 using QuickEdit apk (TryItAndSee / LearnAsYouGo iterative development and testing).

Chromecast HD (1280 x 720 aspect ratio 16:9) running Android TV OS version 14 (user testing).

100% tested and working on Android.<br/>Not tested on other platforms.

Code debugged and reengineered where required using https://aipy.dev/tools


# Future development
Database Toolbox functionality is simple and easy to use and will remain so.

Further development of Database Toolbox is planned.

Database Toolbox will be maintained for new releases of Kodi and changes to Python where possible.


# IMPORTANT
Distribution of this add-on is NOT permitted.
This add-on is exclusively distributed via the Magpie Repository and / or Code-E-Magpie on GitHub.

The code and files of this add-on are free for use, subject to crediting Code-E-Magpie
