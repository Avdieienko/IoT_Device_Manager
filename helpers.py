import os
from glob import glob

def cleanup():
  """Cleans temporary storage"""
  files = glob("./temp_storage/*/*.mp4")

  if len(files) >= 20:
    for f in files:
      os.remove(f)

    print("-----\nTemp storage was cleaned")

def create_temp_storage():
  """Creates temporary storage"""
  if not os.path.exists("./temp_storage"):
    os.makedirs("./temp_storage")
    os.makedirs("./temp_storage/mp4v")
    os.makedirs("./temp_storage/h264")
    print("-----\nTemp storage was created\n-----")