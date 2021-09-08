import requests, pyaudio, wave, threading, itertools
from os import mkdir, system
from os.path import isdir
from base64 import b64encode
from colorama import Fore, init
from time import sleep
from sys import stdout

init()

## AUDIO CONFIG ##

FREQUENCY = 44100
DURATION = 4 # Seconds

## END AUDIO CONFIG ##

## API CONFIG ##

API_KEY = "2d9cfb1cfamsh05cacf514cdc739p169f72jsn87e38a61452d"

## END API CONFIG ##

def main():
    system("clear")
    print(Fore.CYAN + """\n ,ggggggggggg,                                          ,ggggggggggg,                    \ndP\"\"\"88\"\"\"\"\"\"Y8,              ,dPYb, ,dPYb, ,dPYb,     dP\"\"\"88\"\"\"\"\"\"Y8,             I8   \nYb,  88      `8b              IP\'`Yb IP\'`Yb IP\'`Yb     Yb,  88      `8b             I8   \n `\"  88      ,8P              I8  8I I8  8I I8  8I      `\"  88      ,8P          88888888\n     88aaaad8P\"               I8  8\' I8  8\' I8  8\'          88aaaad8P\"              I8   \n     88\"\"\"\"Yb,      ,gggg,gg  I8 dP  I8 dP  I8 dP   ,ggg,   88\"\"\"\"Y8ba    ,ggggg,   I8   \n     88     \"8b    dP\"  \"Y8I  I8dP   I8dP   I8dP   i8\" \"8i  88      `8b  dP\"  \"Y8gggI8   \n     88      `8i  i8\'    ,8I  I8P    I8P    I8P    I8, ,8I  88      ,8P i8\'    ,8I ,I8,  \n     88       Yb,,d8,   ,d8b,,d8b,_ ,d8b,_ ,d8b,_  `YbadP\'  88_____,d8\',d8,   ,d8\',d88b, \n     88        Y8P\"Y8888P\"`Y8PI8\"888PI8\"8888P\'\"Y88888P\"Y88888888888P\"  P\"Y8888P\"  8P\"\"Y8 \n                              I8 `8, I8 `8,                                              \n                              I8  `8,I8  `8,                                             \n                              I8   8II8   8I     """ + Fore.BLUE + """Free raffle tickets, and to joke with my teacher :)""" + Fore.CYAN + """                                        \n                              I8   8II8   8I                                             \n                              I8, ,8\'I8, ,8\'                                             \n                               \"Y8P\'  \"Y8P\'                                              \n""" + Fore.RESET)

    if not isdir("music"):
        print("\n[*] Music folder not detected, creating...")
        mkdir("music")
    else:
        print("\n[*] Music folder detected")

    print("[*] Starting [" + str(DURATION) + "] second recording...\n")
    
    global doneRecording

    doneRecording = False

    t = threading.Thread(target = recordingAnimation)
    t.start()

    record()
    
    doneRecording = True

    print("\n\n[*] Finished recording")
    print("[*] Saved recording at 16 bit, Mono PCM WAV")
    print("[*] Reading binary data from saved audio file...")
    
    with open("music/recording.wav", 'rb') as music:
        print("\n[!] Starting identification")
        identify(music.read())

def identify(song):
    songB64 = b64encode(song)

    print("[-] Song successfully encoded in base64")

    url = "https://shazam.p.rapidapi.com/songs/v2/detect"
    headers = { "content-type": "text/plain", "x-rapidapi-host": "shazam.p.rapidapi.com", "x-rapidapi-key": API_KEY }
    query = { "timezone": "America/Chicago", "locale": "en-US" }

    r = requests.post(url, headers = headers, params = query, data = songB64)
    
    print("\n[Status Code: " + str(r.status_code) + "] Made POST request to API, recieved response")

    if r.status_code == 200:
        print("\n[-] Successful call, parsing...")
    else:
        print("\n[-] Call returned unsuccessfull reponse. Exiting...")
        exit()

    rJSON = r.json()

    if len(rJSON["matches"]) > 0:
        print("\n[!] Match found!\n")

        try:
            print("Title: " + rJSON["track"]["title"]) 
        except:
            print("Title: N/A (Unable to find correct index)")
        try:
            print("Artist/Subtitle: " + rJSON["track"]["subtitle"])
        except:
            print("Artist/Subtitle: N/A (Unable to find correct index)")
        try:
            print("Artist Alt. : " + rJSON["track"]["sections"][2]["name"])
        except:
            pass
        try:
            print("Album: " + rJSON["track"]["sections"][0]["metadata"][0]["text"])
        except:
            print("Album: N/A (Unable to find correct index)")
        try:
            print("\nShazam link: " + rJSON["track"]["url"])
        except:
            print("Shazam link: N/A (Unable to find correct index)")
        try:
            print("Apple Music link: " + rJSON["track"]["myshazam"]["apple"]["actions"][0]["uri"])
        except:
            print("Apple Music link: N/A (Unable to find correct index)")
    else:
        print("\n[!] No matches found :(")

def record():
    p = pyaudio.PyAudio()

    recording = p.open(format = pyaudio.paInt16, channels = 1, rate = FREQUENCY, frames_per_buffer = 1024, input = True, input_device_index = 0)

    chunks = []

    for i in range(int(FREQUENCY / 1024 * DURATION)):
        data = recording.read(1024)
        chunks.append(data)

    recording.stop_stream()
    recording.close()
    p.terminate()

    f = wave.open("music/recording.wav", 'wb')
    f.setnchannels(1)
    f.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    f.setframerate(FREQUENCY)
    f.writeframes(b''.join(chunks))
    f.close()

def recordingAnimation():
    for i in itertools.cycle(['|', '/', '-', '\\']):
        if doneRecording:
            break
        stdout.write('\r[...] Recording audio ' + i)
        stdout.flush()
        sleep(0.1)

main()
