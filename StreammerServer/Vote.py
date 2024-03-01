
import shutil
import os
import os.path

from datetime import datetime

class Vote():
    
    def __init__(self, vote) -> None:
        #check the integrity of the file
        self.recorded = "failed"
        vote_file = "/home/rafael/workspace/VisionTree/votes.txt"
        if vote > 9:
            return
        if vote < 0:
            return
        if os.path.isfile(vote_file) is not True:
            return

        #open the file as a append
        with open(vote_file, "a") as vote_file:
            now = datetime.now()
            string = "{};{}\r\n".format(now.strftime('%Y-%m-%d %H:%M:%S'),vote)
            #save the file
            vote_file.writelines(string)
        self.recorded = "success"

    def result(self):
        return self.recorded
