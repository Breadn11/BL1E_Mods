from mods_base import build_mod, hook, get_pc
from .pypresence import Presence
from .dictionary import MAP_NAMES, CHARACTER_CLASSES

RPC_NAME = 'Borderlands'
RPC_UPDATE_COOLDOWN_SEC = 15
RPC_PRESENCE_ID = '1536688491902148689'
RPC_IMAGE = 'borderlands_logo_512'

class Globals:
    stat_level = 'Unknown'
    stat_character = 'Unknown'
    stat_map = 'Unknown'
    RPC_timeSinceUpdate = 15
    RPC_updateQueued = False
    inMenuMap = True

RPC = Presence(RPC_PRESENCE_ID)

def RPC_enable():
    RPC.connect()

def RPC_disable():
    RPC.close()

@hook('WillowGame.WillowPlayerController:PlayerTick')
def hook_PlayerTick(obj, args, ret, func):
    Globals.RPC_timeSinceUpdate += args.DeltaTime
    if Globals.RPC_updateQueued == True and Globals.RPC_timeSinceUpdate >= RPC_UPDATE_COOLDOWN_SEC:
        Globals.RPC_updateQueued = False
        Globals.RPC_timeSinceUpdate = 0
        if Globals.inMenuMap == False:
            RPC.update(
                name = RPC_NAME,
                details = 'Level ' + Globals.stat_level + ' ' + Globals.stat_character,
                state = Globals.stat_map,
                large_image=RPC_IMAGE)
        else:
            RPC.update(
                name = RPC_NAME,
                details = 'Main Menu',
                large_image = RPC_IMAGE)

@hook('WillowGame.WillowGameInfo:PreCommitMapChange')
def hook_PreCommitMapChange(obj, args, ret, func):
    if args.NextMapName != 'FakeEntry':
        PC = get_pc()
        Globals.inMenuMap = False
        Globals.stat_map = MAP_NAMES.get(args.NextMapName.lower(), args.NextMapName)
        if PC.GetClassDefinition() != None:
            Globals.stat_character = CHARACTER_CLASSES.get(PC.GetClassDefinition()._path_name().lower(), 'Unknown')
        if PC.GetPlayerBodyPawn() != None:
            Globals.stat_level = str(PC.GetPlayerBodyPawn().GetExpLevel())
        Globals.RPC_updateQueued = True

@hook('WillowGame.WillowGFxMenuFrontend:Start')
def hook_FrontendStart(obj, args, ret, func):
    Globals.inMenuMap = True
    Globals.RPC_updateQueued = True

@hook('WillowGame.WillowPlayerController:ExpLevelUp')
def hook_ExpLevelUp(obj, args, ret, func):
    Globals.stat_level = str(get_pc().GetPlayerBodyPawn().GetExpLevel() + 1)
    Globals.RPC_updateQueued = True

build_mod(on_enable=RPC_enable, on_disable=RPC_disable)