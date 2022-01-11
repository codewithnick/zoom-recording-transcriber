import shutil
from os import path
import os
from pydub import AudioSegment
import speech_recognition as sr
import moviepy.editor as mp
import time
import pydub
from make_chunk import silence_based_conversion
from pydub.silence import split_on_silence

#pydub.AudioSegment.converter = os.getcwd()+ "\\ffmpeg.exe"                    
#pydub.AudioSegment.ffprobe   = os.getcwd()+ "\\ffprobe.exe"
#use this if files are not detected


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
        sound = AudioSegment.from_mp3(dst)
        sound.export(AUDIO_FILE, format="wav")
        
    
    # use the audio file as the audio source                                        
    r = sr.Recognizer()
    silence_based_conversion(AUDIO_FILE, TEXT_FILE)

    if delete_after_completion:
        print("deleting files after completion")
        os.remove(dst)
        os.remove(AUDIO_FILE)

