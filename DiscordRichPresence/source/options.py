from mods_base import ButtonOption, HiddenOption
from ui_utils import OptionBox, OptionBoxButton
from .globals import *

def optTitle_ShowOptionBox(source):
    optTitle_OptionBox.show()

def optTitle_onButtonSelect(box, button):
    optTitle_Storage.value = button.name
    Globals.game_title = button.name
    Globals.RPC_updateQueued = True

optTitle_OptionBox = OptionBox(
    title = 'Change Game Title',
    message = "This changes the game's name on Discord and is entirely cosmetic.",
    on_select = optTitle_onButtonSelect,
    buttons = [
    OptionBoxButton('Borderlands'),
    OptionBoxButton('Borderlands Enhanced'),
    OptionBoxButton('Borderlands GOTY'),
    OptionBoxButton('Borderlands GOTY Enhanced')])

optTitle_OptionBoxOpener = ButtonOption(identifier = 'Change Game Title', on_press = optTitle_ShowOptionBox)

optTitle_Storage = HiddenOption(identifier = 'Game Title', value = 'Borderlands')