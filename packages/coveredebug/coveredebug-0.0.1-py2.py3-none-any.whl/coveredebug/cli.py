import os
import json, uuid


class LocationUpdate():
    def __init__(self):
        self.id = str(uuid.uuid4())



def main():

    p = os.getcwd()
    print(f"👋 coveredebug is running in {os.getcwd()}")
    # get all json in dir and print

 
    files = [f.name for f in os.scandir(p) if f.is_file()]
    
    if len(files) > 0:
        for file in files:
            print(f"found a file called {file} in {p}")
    else:
        print(f"😢 No json files found in {p}")


def version():
    print("version")


if __name__ == '__main__':
    main()
