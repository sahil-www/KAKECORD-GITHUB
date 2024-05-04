



import os
# import urllib.parse as up

########################################## SHOULD NOT BE CHANGED ###################################################

# Heroku Postgres
H_URL = "postgres://wdrbezikasxxax:751b08a6946ce7706125e75ca62eba14d42fb7e33e1d364798e1df0f471ad98d@ec2-54-243-92-68.compute-1.amazonaws.com:5432/d1fs5aigr4tun4"
H_DATABASE = "d1fs5aigr4tun4"
H_USER = "wdrbezikasxxax"
H_PASS = "751b08a6946ce7706125e75ca62eba14d42fb7e33e1d364798e1df0f471ad98d"

# BOT
BOT_TOKEN = "YOUR TOKEN HERE"
BOT_PFP = "https://cdn.discordapp.com/attachments/850320052757594113/850320234120478731/Kakecord_PFP_01.png"
BOT_INVITE = "https://discord.com/oauth2/authorize?client_id=848798390136471572&scope=bot&permissions=2147875921"
BOT_SERVER = "https://discord.gg/xNgY7JhWsr"
BOT_PATREON = ""

# DIRS
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

####################################################################################################################

BOT_VERSION = "1.0.1"


# Emojis
# Currency
E_KAKECHIPS = "<:s_kakechips:854648905836134432>"
E_OWOCHIPS = "<:s_owo_chips:854195003283079178>"

# Card suits
E_SPADES = "<:s_spades:848810071060250672>"
E_HEARTS = "<:s_hearts:848810071554523137>"
E_DIAMONDS = "<:s_diamonds:848810071810899998>"
E_CLUBS = "<:s_clubs:848810073114279987>"
E_ALL_SUITES = "<:s_all_suites:848810074528940063>"

# RPS
E_ROCK = "<:s_rock:849904238733688832>"
E_PAPER = "<:s_paper:849907075307274240>"
E_SCISSORS = "<:s_scissors:849904239009726514>"

# TTT
E_A = "🇦"
E_B = "🇧"
E_C = "🇨"
E_D = "🇩"
E_E = "🇪"
E_F = "🇫"
E_G = "🇬"
E_H = "🇭"
E_I = "🇮"
E_X = ":x:"
E_O = ":o:"

# CF
E_COINFLIP = "<a:a_coinflip:856438213597200434>"
E_HEADS = "<:s_heads:856431572902084608>"
E_TAILS = "<:s_tails:856431688489238539>"

# RR
E_REVOLVER = "<:revolver:860159968253575177>"
E_BULLET = "<:bullet:860159794437423125>"

# Others
E_CHECK = "✅"
E_CROSS = "❎"
E_VS = "<:s_vs:850256973144391700>"
E_INFO = "<:s_info:857924428020842506>"
E_CHIPS = "<:su_chips:848809533350477835>"
E_GAMBLING = "<:s_gambling:857929387310841897>"
E_SUPPORT = "👍"
E_QUESTION = ":question:"

# Images
# RPS
I_RPS = "https://cdn.discordapp.com/attachments/850293649916559362/854294270876975114/PicsArt_06-15-03.10.17.png"
I_ROCK = "https://cdn.discordapp.com/attachments/850293649916559362/850293740253347911/rock.png"
I_PAPER = "https://cdn.discordapp.com/attachments/850293649916559362/850293763439329310/paper.png"
I_SCISSORS = "https://cdn.discordapp.com/attachments/850293649916559362/850293789369040906/scissors.png"

# TTT
I_TTT = "https://cdn.discordapp.com/attachments/850293649916559362/853924712605679616/PicsArt_06-14-02.41.49.png"
I_X = "https://cdn.discordapp.com/attachments/850293649916559362/853923198159683614/PicsArt_06-14-02.35.41.png"
I_O = "https://cdn.discordapp.com/attachments/850293649916559362/853924065257455636/PicsArt_06-14-02.39.14.png"

# CF
I_COINFLIP = "https://cdn.discordapp.com/attachments/850293649916559362/856422058291625984/coinflip.gif"
I_HEADS = "https://cdn.discordapp.com/attachments/850293649916559362/856432036306223104/heads.png"
I_TAILS= "https://cdn.discordapp.com/attachments/850293649916559362/856432051540328468/tails.png"

# BJ
I_BJ = "https://cdn.discordapp.com/attachments/850293649916559362/860167988787413072/blackjack.png"

# RR
I_REVOLVER = "https://cdn.discordapp.com/attachments/850293649916559362/860159902588207104/revolver.png"
I_BULLET = "https://cdn.discordapp.com/attachments/850293649916559362/860159920955064320/bullet.png"