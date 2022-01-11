import os
from zoom import transcribe
#os.chdir("/mydir")
for root, dirs, files in os.walk(os.getcwd()):
  for file in files:
    if file.endswith('.mkv'):
        
        print("directory: ",root)
        filename=file.split(".")[0]
        extension=file.split(".")[1]
        print("file: ",file)
        transcribe(root,filename,delete_after_completion=False)
