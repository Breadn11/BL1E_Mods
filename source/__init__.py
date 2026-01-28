from mods_base import build_mod, hook, BoolOption
from unrealsdk.hooks import Type, Block

@hook('WillowGame.CombatDialogLineDefinition:ResolveSoundCue', Type.PRE)
def onResolveSoundCue(obj, args, ret, func):
    if args.CharacterSoundEffects.Outer._path_name() == 'gd_DialogPlayer.Common':
        if args.SoundEffectType.Name == 'PlayerJump':
            if optMuteJump.value == True:
                return Block
        if args.SoundEffectType.Name == 'DialogType_Landed':
            if optMuteLand.value == True:
                return Block

optMuteJump = BoolOption(
    identifier = 'Mute Jumping Sound',
    value = True,
    true_text='True',
    false_text='False',
)

optMuteLand = BoolOption(
    identifier = 'Mute Landing Sound',
    value = True,
    true_text='True',
    false_text='False',
)

build_mod()