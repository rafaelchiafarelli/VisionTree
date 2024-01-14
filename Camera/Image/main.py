
import Maker
from time import sleep
import sys

def main():
    camera.start()
    while camera.isAlive():
        sleep(1)
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)

# Arguments passed
print("\nName of Python script:", sys.argv[0])
for arg in sys.argv:
    print("argument is: {}".format(arg))
camera = Maker.ImageMaker(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],sys.argv[6],int(sys.argv[7]))
                          
try:
    main()
except :
    # terminate main thread
    print('Main interrupted! Exiting.')

    sys.exit()
    