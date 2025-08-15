from talon import Module, actions, scope, actions
import subprocess

mod = Module()

MICROPHONE_DEVICE_LIST = ["None", "System Default"]

def get_modes():
    return scope.get("mode")

def get_microphone_name():
    return actions.sound.active_microphone() # => str ["None", "System Default"]

def is_microphone_none():
    return get_microphone_name() == "None"

def is_mode_sleep():
    return "sleep" in get_modes()

def is_mode_dictation():
    return "dictation" in get_modes()

@mod.action_class
class Actions:
    def firm_toggle_talon():
        """Toggle between None and System Default microphone"""
        if is_microphone_none():
            # Toggle on
            subprocess.run(["mplayer", "/usr/share/sounds/freedesktop/stereo/message.oga"], check=True)
            actions.sound.set_microphone("System Default")
            actions.speech.enable()
            actions.mode.disable("sleep")
            actions.mode.disable("command")
            actions.mode.enable("dictation")
        else:
            # Toggle off
            subprocess.run(["mplayer", "/usr/share/sounds/freedesktop/stereo/power-unplug.oga"], check=True)
            actions.sound.set_microphone("None")
            actions.speech.disable()
            actions.mode.disable("command")
            actions.mode.disable("dictation")
            actions.mode.enable("sleep")
