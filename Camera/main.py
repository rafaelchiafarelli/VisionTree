#main file of the searcher.

"""
This will be responsible to:
* create all the folders pertinent to this process (in dev/shm)
    * one cam_# for each camera
    * one cam_#/low_res 
    * one cam_#/high_res

* launch one thread per camera available
* establish the connection to the camera
    * low res
    * high res
* ensure there is a frame available
* store this into the out folder with the number
    * the format is still not defined. 
    * the format is going to be the one that is faster
    * there is no reason to save it in JPG if there will be more processing required
    * example: /dev/shm/cam_1/low_res/img_0.png 
    * the amount of picture that is saved is configurable
        * minimum is 5 maximum is 50
* manage deletion of the new files.        
"""

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()