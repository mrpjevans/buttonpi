import os
from time import sleep

from gpiozero import Button, LED
import pygame
import config
from audio_mapping import audio_mapping

button = Button(4, pull_up = False)
led = LED(22)
track = config.AUDIO_TRACK

pygame.mixer.pre_init(buffer=4096)
pygame.mixer.init()

def announce():
    global track, led
    play_and_block("./assets/audio_track.wav")
    play_and_block("./assets/" + str(track) + ".wav")
    play_and_block("./assets/ready.wav")
    led.on()

def play(file):
    pygame.mixer.music.unload()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def play_and_block(file):
    play(file)
    while pygame.mixer.music.get_busy():
        continue
    
def enter_setup_mode():
    global in_setup
    if not in_setup:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        in_setup = True
        setup()

def setup():
    global in_setup, button, track
    play_and_block("./assets/enter_setup.wav")
    play_and_block("./assets/" + str(track) + ".wav")
    timer = 0
    while True:

        if button.is_pressed:
            track += 1
            if track == 9:
                track = 0
            if track == 0:
                play_and_block("./assets/shutdown.wav")
            else:
                play_and_block("./assets/" + str(track) + ".wav")
            button.wait_for_release()
            timer = 0

        sleep(0.1)
        timer += 0.1
        
        if timer >= 5:
            if track == 0:
                play_and_block("./assets/shutting_down.wav")
                os.system("sudo poweroff")
                while True:
                    sleep(1)
            else:
                play_and_block("./assets/leave_setup.wav")
                in_setup = False
                with open("./config.py", 'w') as file:
                    file.write("AUDIO_TRACK = " + str(track))
                announce()
            break

button.hold_time = 5
button.when_held = enter_setup_mode
in_setup = False

announce()

while True:
    if button.is_pressed:
        if in_setup:
            pass
        elif pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            led.on()
        else:
            led.off()
            play("./audio/" + audio_mapping[track - 1])
        button.wait_for_release()

    sleep(0.1)

# while True:
#     button.wait_for_press()
#     button.wait_for_release()
#     if not in_setup:
#         led.off()
#         play_and_block("./audio/" + audio_mapping[track - 1])
#         led.on()

            
