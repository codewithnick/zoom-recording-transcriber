from os import path
import os
from pydub import AudioSegment
import speech_recognition as sr
import moviepy.editor as mp
import time
import pydub

#pydub.AudioSegment.converter = os.getcwd()+ "\\ffmpeg.exe"                    
#pydub.AudioSegment.ffprobe   = os.getcwd()+ "\\ffprobe.exe"
#use this if files are not detected

def format_text(s):
    n=15
    '''returns a string where \\n is inserted between every n words'''
    a = s.split()
    ret = ''
    for i in range(0, len(a), n):
        ret += ' '.join(a[i:i+n]) + '\n'

    return ret


def file_exists(filename):
    if os.path.exists(filename):
        return filename
    return False

def transcribe(curr_dir=os.getcwd(),filename="sample",delete_after_completion=False):

    # files
    src = curr_dir+"\\"+filename+".mkv"
    dst = curr_dir+"\\"+filename+".mp3"
    AUDIO_FILE =curr_dir+"\\"+filename+".wav"
    TEXT_FILE=curr_dir+"\\"+filename+".txt"

    if file_exists(TEXT_FILE):
        print("transcribed file already present")
        return
    
    my_clip = mp.VideoFileClip(src)
    if not file_exists(dst):
        print("making .mp3 file for ",src)
        my_clip.audio.write_audiofile(dst)

    
    # convert mp3 to wav
    if not file_exists(AUDIO_FILE):
        print("making .wav file for ",dst)
        my_clip.audio.write_audiofile(dst)
        sound = AudioSegment.from_mp3(dst)
        sound.export(AUDIO_FILE, format="wav")
        
    
    # use the audio file as the audio source                                        
    r = sr.Recognizer()
    if not file_exists(TEXT_FILE):
        print("transcribing ",AUDIO_FILE)
        with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)  # read the entire audio file                  
                mytext=format_text(r.recognize_google(audio))
                with open(TEXT_FILE,"w") as f:
                    f.write(mytext)
                print("Transcription: " +mytext )
    if delete_after_completion:
        print("deleting files after completion")
        os.remove(dst)
        os.remove(AUDIO_FILE)

transcribe(curr_dir=os.getcwd(),filename="sample")
