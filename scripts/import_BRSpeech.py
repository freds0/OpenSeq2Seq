import os
import re
import unicodedata
from tqdm import tqdm
import pandas 
import argparse

vocab="abcdefghijklmnopqrstuvwxyzçãàáâêéíóôõúû\- "

def text_normalize(text):
    accents = ('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT') #portuguese
    chars = [c for c in unicodedata.normalize('NFD', text) if c not in accents]
    text = unicodedata.normalize('NFC', ''.join(chars))# Strip accent
    text = text.lower()
    text = re.sub("[^{}]".format(vocab), " ", text)
    text = re.sub("[ ]+", " ", text)
    return text

def preprocess(dataset_dir, out_dir): 
  if out_dir is None:
    out_dir = dataset_dir

  normalised_lines = []

  lines = open(os.path.join(dataset_dir,'metadata.csv')).readlines()[1:] # by pass head
  for i in tqdm(range(len(lines))):
      #format: filename|subtitle|transcript|levenshtein
      splits= lines[i].split('|')
      transcript = text_normalize(splits[1])
      audiopath = os.path.abspath(os.path.join(dataset_dir,splits[0]))
      wavfilesize = os.path.getsize(audiopath)
      normalised_lines.append((audiopath, wavfilesize, transcript))

  df = pandas.DataFrame(data=normalised_lines, columns=["wav_filename", "wav_filesize", "transcript"])
  df.to_csv(os.path.join(out_dir, "metadata_brspeech3_openseq2seq.csv"), index=False)


if __name__ == "__main__":
    """
    
    Usage
    python import_brspeech.py --dataset_dir=/data/BRSpeech-ASR-beta3/

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset_dir', type=str, help='BRSpeech dataset root dir')
    parser.add_argument('-o', '--output_dir', type=str, default=None,
                        help='Output Dataset dir')
    
    args = parser.parse_args()
    preprocess(args.dataset_dir, args.output_dir)