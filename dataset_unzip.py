from zipfile import ZipFile
from tqdm.auto import tqdm
import os

output_path = "competition_support_set.zip"

out_dir  = "competition_support_set"

os.makedirs(out_dir, exist_ok=True)

with ZipFile(output_path, 'r') as z:
    for member in tqdm(z.infolist(), desc="Unzipping", unit="file"):
        z.extract(member, out_dir)