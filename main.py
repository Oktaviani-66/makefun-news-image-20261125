#!/usr/bin/env python3
"""THE MERIDIAN STANDARD — entrypoint (Akun 13, News Image 20261125).

The page is finished before this file ever runs: entry.png sits beside
it in the repository, and running this program only carries that page
to /output/entry.png, untouched. Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
