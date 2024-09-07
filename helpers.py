import os

def cleanup():
  """Cleans temporary storage"""
  files = []
  for (dirpath, dirnames, filenames) in os.walk("./temp_storage"):
    files.extend(filenames)
    break
  if(len(files) > 10):
    for fn in files:
      os.remove(f"../temp_storage/{fn}")
    print("-----\nTemp storage was cleaned")

def create_temp_storage():
  """Creates temporary storage"""
  if not os.path.exists("./temp_storage"):
    os.makedirs("./temp_storage")
    print("-----\nTemp storage was created")
  else:
    print("-----\nTemp storage already exists")