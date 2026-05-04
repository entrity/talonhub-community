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

def is_mode_command():
  return "command" in get_modes()

@mod.action_class
class Actions:
  def firm_toggle_talon():
    """Toggle between not active and dictation mode"""
    if is_microphone_none():
      _set_dictation_mode()
    else:
      _set_sleep_mode()

  def firm_toggle_command_mode():
    """Toggle between command mode and dictation mode"""
    if is_microphone_none():
      _set_command_mode()
    else:
      _set_sleep_mode()

  def toggle_command_vs_dictation_mode():
    """Toggle between command mode and dictation mode"""
    if not is_mode_command():
      _set_command_mode()
    else:
      _set_dictation_mode()

def toggle_on():
  actions.sound.set_microphone("System Default")
  actions.speech.enable()

def _set_command_mode():
  play_sound("/usr/share/sounds/freedesktop/stereo/message-new-instant.oga")
  if is_microphone_none():
    toggle_on()
  actions.mode.disable("sleep")
  actions.mode.disable("dictation")
  actions.mode.enable("command")

def _set_dictation_mode():
  play_sound("/usr/share/sounds/freedesktop/stereo/message.oga")
  if is_microphone_none():
    toggle_on()
  actions.mode.disable("sleep")
  actions.mode.disable("command")
  actions.mode.enable("dictation")

def _set_sleep_mode():
  play_sound("/usr/share/sounds/freedesktop/stereo/power-unplug.oga")
  if not is_microphone_none():
    actions.sound.set_microphone("None")
    actions.speech.disable()
  actions.mode.disable("command")
  actions.mode.disable("dictation")
  actions.mode.enable("sleep")

def play_sound(file_path: str):
  subprocess.Popen(["mplayer", "-volume", "66", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
