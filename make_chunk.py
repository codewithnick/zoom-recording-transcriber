# importing libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil
import traceback
def format_text(s):
    n=15
    '''returns a string where \\n is inserted between every n words'''
    a = s.split()
    ret = ''
    for i in range(0, len(a), n):
        ret += ' '.join(a[i:i+n]) + '\n'

    return ret


def silence_based_conversion(path,textfilepath):

	# open the audio file stored in
	# the local system as a wav file.
	song = AudioSegment.from_wav(path)

	# open a file where we will concatenate
	# and store the recognized text
	fh = open(textfilepath, "w+")
		
	# split track where silence is 5 seconds
	# or more and get chunks
	print("making file chunks for \n",path)
	chunks = split_on_silence(song,
		# must be silent for at least 5 seconds
		# or 500 ms. adjust this value based on user
		# requirement. if the speaker stays silent for
		# longer, increase this value. else, decrease it.
		min_silence_len = 5000,

		# consider it silent if quieter than -16 dBFS
		# adjust this per requirement
		silence_thresh = -60
	)
	del song
	# create a directory to store the audio chunks.
	try:
		os.mkdir('audio_chunks')
	except(FileExistsError):
		pass

	# move into the directory to
	# store the audio files.
	os.chdir('audio_chunks')

	i = 0
	# process each chunk
	for chunk in chunks:
			
		# Create 0.5 seconds silence chunk
		chunk_silent = AudioSegment.silent(duration = 10)

		# add 0.5 sec silence to beginning and
		# end of audio chunk. This is done so that
		# it doesn't seem abruptly sliced.
		audio_chunk = chunk_silent + chunk + chunk_silent

		# export audio chunk and save it in
		# the current directory.
		print("saving chunk{0}.wav".format(i))
		# specify the bitrate to be 192 k
		audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")

		# the name of the newly created chunk
		filename = 'chunk'+str(i)+'.wav'

		print("Processing chunk "+str(i))

		# get the name of the newly created chunk
		# in the AUDIO_FILE variable for later use.
		file = filename

		# create a speech recognition object
		r = sr.Recognizer()

		# recognize the chunk
		with sr.AudioFile(file) as source:
			# remove this if it is not working
			# correctly.
			#r.adjust_for_ambient_noise(source)
			#audio_listened = r.listen(source)
			audio_listened = r.record(source)

		try:
			# try converting it to text
			print("trying to transcribe")
			rec = format_text( r.recognize_google(audio_listened))
			print("\nTranscribtion:\n",rec,"\n")
			# write the output to the file.
			fh.write(rec+". ")

		# catch any errors.
		except sr.UnknownValueError:
			print("Could not understand audio")

		except sr.RequestError as e:
			print("Could not request results. check your internet connection")
		except:
			traceback.print_exc()
		i += 1
    
	os.chdir('..')
	shutil.rmtree('audio_chunks')

    