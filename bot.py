import discord, csv, os, logging, pygsheets, json
from discord.ext import commands
from steam.steamid import SteamID, steam64_from_url

client = commands.Bot(command_prefix='!')
permitted_channels = [721361526287499329]  # MUST HAVE A CHANNEL HERE OTHERWISE NOTHING WILL BE RECORDED

# -------- LOGGING --------
logFormatter = logging.Formatter('[%(asctime)s][%(name)s][%(lineno)d][%(levelname)s] %(message)s')
logger = logging.getLogger()
fileHandler = logging.FileHandler("bot.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logging.getLogger('Discord')

logger.setLevel('INFO')


# -------- LOGGING --------


def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)


config = read_json('config.json')

google_sheets = pygsheets.authorize(service_file=config['google token path'])
try:
    sheet = google_sheets.open(config['google spreadsheet name'])
except pygsheets.exceptions.SpreadsheetNotFound:
    sheet = google_sheets.create(config['google spreadsheet name'])

known_users = [user['emailAddress'] for user in sheet.permissions]
[sheet.share(email, role='writer') if email not in known_users else '' for email in config['share with']]


@client.event
async def on_ready():
    logger.info("Bot is online")
    await client.change_presence(activity=discord.Game(name="Watching Clouds."))


async def get_steam_profile(steam64):
    try:
        steam64 = int(steam64)
    except ValueError:
        return None
    steam64 = SteamID(steam64)
    return steam64.community_url


async def get_steam64(profile):
    return steam64_from_url(str(profile))


def read_csv(file: str):
    try:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            players = {}
            next(reader, None)
            for row in reader:
                players[int(row[0])] = {"Steam Profile": row[1], "Reported": int(row[2])}
            return players
    except FileNotFoundError:
        logger.warning(f"Cannot Find {config['spreadsheet path']}, using an empty dictionary!")
        return {}


def csv_write(file: str, players: dict):
    try:
        os.replace(file, f'{file}.bak')
    except FileNotFoundError:
        pass
    with open(file, 'w+', newline='') as f:
        write = csv.writer(f)
        write.writerow(['Steam64', 'Steam Profile', 'Times Reported'])
        rows = []
        for key, value in players.items():
            rows.append([str(key), value['Steam Profile'], value["Reported"]])
        write.writerows(rows)
    sheet.sheet1.update_values(crange='A1', values=rows)


@client.event
async def on_message(message: discord.Message):
    if message.channel.id in permitted_channels:
        logger.info(f"Searching message from {message.author} in permitted channels for steam64s and profiles...")
        for word in message.content.split():
            if steam64 := await get_steam64(word):
                logger.info(f"Found steam info: {steam64, word}.")
                await add_report(int(steam64), word)
            else:
                try:
                    if profile := await get_steam_profile(int(word)):
                        logger.info(f"Found steam info: {int(word), profile}.")
                        await add_report(int(word), profile)
                except ValueError:
                    pass


problem_players = read_csv(config['spreadsheet path'])


async def add_report(steam64: int, profile: str):
    logger.info(f"Adding report for {profile}")
    if steam64 in problem_players.keys():
        problem_players[steam64]["Reported"] += 1
        problem_players[steam64]['Steam Profile'] = profile
    else:
        problem_players[steam64] = {"Steam Profile": profile, "Reported": 1}
    csv_write(config['spreadsheet path'], problem_players)


try:
    client.run(config['discord token'])  # MUST HAVE A VALID DISCORD BOT TOKEN
except discord.errors.LoginFailure:
    logger.error("Could not login to discord, check your discord token!")
except discord.errors.HTTPException:
    logger.error("Invalid discord token provided, please check your token and try again!")
