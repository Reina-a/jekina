#!/usr/bin/env python3
import os

def action():
    jekyll_home = '/mnt/c/Users/Reina/OneDrive/Chirpy/'
    os.chdir(jekyll_home)
    print("\033[1;36;40mbuilding jekyll, it may take minutes...:\033[0m")
    os.system("jekyll build")
    print("\033[1;36;40mbuild sucess:\033[0m")

if __name__ == "__main__":
    action()