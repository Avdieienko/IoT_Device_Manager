import os

def cleanup():
  """Cleans temporary storage"""
  files = []
  for (dirpath, dirnames, filenames) in os.walk("../temp_storage"):
    files.extend(filenames)
    break
  if(len(files) > 10):
    for fn in files:
      os.remove(f"../temp_storage/{fn}")
    print("-----\nTemp storage was cleaned")