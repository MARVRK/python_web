import logging
import argparse
from shutil import copyfile
from threading import Thread
from pathlib import Path

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--target", "-t", help="Target folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = parser.parse_args()
target = Path(args.target)
output = Path(args.output)

folders = []

def target_folder(path: Path):
    for i in path.iterdir():
        if i.is_dir():
            folders.append(i)
            target_folder(i)


def clone_folder(path: Path):
    for i in path.iterdir():
        if i.is_file():
            ext = i.suffix[1:]
            ext_folder = output / ext
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)  # Create folder if it doesn't exist
                copyfile(i, ext_folder / i.name)
            except OSError as err:
                logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    folders.append(output)
    target_folder(target)
    print(folders)

    threads = []

    for folder in folders:
        th = Thread(target=clone_folder, args=(folder,))
        th.start()
        threads.append(th)

    [th.join()for th in threads]

    print("Original source can be removed")
