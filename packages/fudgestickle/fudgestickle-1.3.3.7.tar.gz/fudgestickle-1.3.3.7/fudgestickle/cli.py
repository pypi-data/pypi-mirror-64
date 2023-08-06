import argparse
from utils import *

def main():
    parser = argparse.ArgumentParser(description="Fudgestickle expectant params")
    args = parser.parse_args()
    
    update()
    
if __name__ == "__main__" :
    main()
    