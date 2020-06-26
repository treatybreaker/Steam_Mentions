# Steam_Mentions
Built to track mentions of steam 64s and steam profiles in the problem players discord channel in the OIH discord.

# Discord Token
You can get a discord token by following this guide: https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro

Once you have your token head over to config.json and place it into the discord token field, e.g. "discord token": "your token"

#Spreadsheet Path
The spreadsheet path is the location of where you want a LOCAL (saved on your computer/server/whatever) csv to be saved to by the program.

Set like so: "spreadsheet path": "C:\Users\yourname\Desktop\Steam_Mentions\player_reports.json"
#Google Token
You can get a google token by following this guide: https://pygsheets.readthedocs.io/en/stable/authorization.html#service-account

You'll want to follow the first four steps then skip down to: https://pygsheets.readthedocs.io/en/stable/authorization.html#service-account

Once you have the json file from google save it somewhere and in config.json set google token path to the path of your google json file, e.g: "google token path": "C:\Users\yourname\Desktop\Steam_Mentions\google_token.json"

#Google Spreadsheet Name
Just the name of the spreadsheet, if you haven't created a spreadsheet it will make one with the name provided there, otherwise it will overwrite the spreadsheet with each new update.

Set like so: "google spreadsheet name": "problem players"

#Share With
Provide a list of emails that you'd like the spreadsheet shared with.

Set like so: "share with": ["myemail@gmail.com", "anotheremail@genericcompany.com"]
