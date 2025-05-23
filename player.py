import pafy
import vlc
import asyncio
import ctypes 
import platform
from prompt_toolkit import prompt



async def play_song(url):
    global player
    is_opening = False
    is_playing = False
    
    
    # Inicializar COM solo si es Windows
    if platform.system() == "Windows":
        ctypes.windll.ole32.CoInitializeEx(None, 0x2)
    
    video = pafy.new(url)
    best = video.streams[0]
    play_url = best.url
    
    
    instance = vlc.Instance('--no-video')
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    print(play_url)
    media.get_mrl()
    player.set_media(media)
    player.audio_set_volume(20)
    player.play()
    
    good_states = [
        "State.Playing",
        "State.NothingSpecial",
        "State.Opening"
    ]
    
    while str(player.get_state()) in good_states:
        await asyncio.sleep(0.5)
        if str(player.get_state()) == "State.Opening" and not is_opening:
            print("Status: Loading")
            is_opening = True
            
        if str(player.get_state()) == "State.Playing" and not is_playing:
            print("Status: Playing")
            is_playing = True
    
    print("Status: Finish")
    player.stop()
    
def stop_song():
    global player
    if player:
        player.stop()
        print("Song stopped")
        
