from mods_base import build_mod, hook, get_pc
from ui_utils import TrainingBox
from .pypresence import Presence
from .options import optTitle_Storage, optTitle_OptionBox, optTitle_OptionBoxOpener
from .dictionary import *
from .globals import *

RPC = Presence(RPC_PRESENCE_ID)

@hook('WillowGame.WillowPlayerController:PlayerTick')
def hook_PlayerTick(obj, args, ret, func):
    Globals.RPC_timeSinceUpdate += args.DeltaTime
    if Globals.RPC_updateQueued == True and Globals.RPC_timeSinceUpdate >= RPC_COOLDOWN_SEC:
        Globals.RPC_updateQueued = False
        Globals.RPC_timeSinceUpdate = 0
        RPC_update()

@hook('WillowGame.WillowGameInfo:PreCommitMapChange')
def hook_PreCommitMapChange(obj, args, ret, func):
    if args.NextMapName != 'FakeEntry':
        PC = get_pc()
        Globals.inMenuMap = False
        Globals.stat_map = MAP_NAMES.get(args.NextMapName.lower(), args.NextMapName)
        if PC.GetClassDefinition() != None:
            Globals.stat_character = CHARACTER_CLASSES.get(PC.GetClassDefinition().Name, 'Unknown')
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

def RPC_update():
    if Globals.inMenuMap == True:
        RPC.update(
            name = Globals.game_title,
            details = 'Main Menu',
            large_image = RPC_IMAGE)
    else:
        RPC.update(
            name = Globals.game_title,
            details = 'Level ' + Globals.stat_level + ' ' + Globals.stat_character,
            state = Globals.stat_map,
            large_image = RPC_IMAGE)

disableWarning = TrainingBox(
    title = 'WARNING',
    message = 'Please restart your game if you wish to re-enable the mod.',
    min_duration = 2
)

def onModEnable():
    RPC.connect()
    Globals.inMenuMap = True
    Globals.RPC_updateQueued = True

def onModDisable():
    RPC.close()
    disableWarning.show()

build_mod(
    on_enable = onModEnable, 
    on_disable = onModDisable
    )