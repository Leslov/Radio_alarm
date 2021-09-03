import vlc
from radio import MyRadio


class RadioImpl(MyRadio):
    def __init__(self):
        stations = {
            'Rawa': 'https://rawa.fm:8443/radio/8000/radio.mp3',
            'Rawa Kirtan': 'https://rawa.fm:8443/radio/8010/radio.mp3'
        }
        self.set_stations(stations)

    print('Инициализация радио')
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_list_player_new()
    volume = 50

    def play(self):
        print('playing')
        self.player.play()

    def stop(self):
        print('playing')
        self.player.pause()

    def next_station(self):
        print('next')
        self.player.next()

    def prev_station(self):
        print('prev')
        self.player.previous()

    def set_stations(self, stations):
        media_list = self.vlc_instance.media_list_new(list(stations.values()))
        self.player.set_media_list(media_list)

    def volume_up(self, volume, dif=10):
        self.volume = min(volume + dif, 100)
        self.set_volume(volume)

    def volume_down(self, volume, dif=10):
        self.volume = max(volume - dif, 0)
        self.set_volume(volume)

    def set_volume(self, volume):
        print(f'Current volume - {volume}')
        self.player.get_media_player().audio_set_volume(volume)


if __name__ == '__main__':
    rad = RadioImpl()
    rad.play()
