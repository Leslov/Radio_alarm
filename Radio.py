import vlc
from global_hotkeys import *

import time


def get_radio_stations():
    stations = {
        'Rawa': 'https://rawa.fm:8443/radio/8000/radio.mp3',
        'Rawa Kirtan': 'https://rawa.fm:8443/radio/8010/radio.mp3'
    }
    return stations


# Flag to indicate the program whether should continue running.
is_alive = True
is_playing = True
station_index = 0
current_station = ''

# VLC
vlc_instance = vlc.Instance()
player = vlc_instance.media_list_player_new()
media_list = vlc_instance.media_list_new(list(get_radio_stations().values()))
player.set_media_list(media_list)
volume = 50


def get_new_station(is_next):
    stations = get_radio_stations()
    count = len(stations)
    global station_index
    if is_next is None:
        pass
    elif is_next:
        station_index += 1
    elif not is_next:
        station_index -= 1

    if station_index >= count:
        station_index -= count
    elif station_index < 0:
        station_index += count
    keys = tuple(stations.keys())
    key = keys[station_index]
    return key


def set_station(key):
    global player
    print(f'Now playing {key}')
    station = get_radio_stations()[key]
    is_playing = True
    player.next()
    # init_player(station)


# Our keybinding event handlers.
def next():
    global player
    player.next()
    # key = get_new_station(True)
    # set_station(key)


def prev():
    global player
    player.previous()

    # key = get_new_station(False)
    # set_station(key)


def volume_up(volume, dif=10):
    volume = min(volume + dif, 100)
    set_volume(volume)


def volume_down(volume, dif=10):
    volume = max(volume - dif, 0)
    set_volume(volume)


def set_volume(volume):
    global player
    print(f'Current volume - {volume}')
    player.get_media_player().audio_set_volume(volume)


def pause():
    global is_playing
    is_playing = not is_playing
    if is_playing:
        print('Playing')
        player.play()
    else:
        print('Pause')
        player.stop()


def exit_application():
    global is_alive
    stop_checking_hotkeys()
    is_alive = False


def get_bindings():
    bindings = [
        [["control", "shift", "1"], None, prev],
        [["control", "shift", "2"], None, next],
        [["control", "shift", "multiply_key"], None, pause],
        [["control", "shift", "+"], None, lambda: set_volume(volume_up)],  # lambda volume: min(volume + 10, 100)
        [["control", "shift", "-"], None, lambda: set_volume(volume_down)],  # lambda volume: max(volume - 10, 0)],
        [["control", "shift", "9"], None, exit_application],
    ]
    return bindings


def get_commands():
    commands = []
    for bind in bindings:
        commands.append(bind[2])
    return tuple(commands)


def run_binding(bind_name):
    for command in commands:
        if command.__name__ == bind_name:
            command()


# Declare some key bindings.
# These take the format of [<key list>, <keydown handler callback>, <keyup handler callback>]

bindings = get_bindings()
commands = get_commands()
print([x.__name__ for x in commands])
# Register all of our keybindings
register_hotkeys(bindings)

# Finally, start listening for keypresses
start_checking_hotkeys()

# Keep waiting until the user presses the exit_application keybinding.
# Note that the hotkey listener will exit when the main thread does.
print(
    'Управление: Медиа кнопки для переключения станций. Ctrl+Shift+ -/+ управление звуком. Ctrl+Shift+9 для завершения программы')
key = get_new_station(None)
set_station(key)
while is_alive:
    # time.sleep(0.1)
    var = input()
    run_binding(var)
