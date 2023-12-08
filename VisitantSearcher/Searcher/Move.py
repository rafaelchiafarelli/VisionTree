"""movement implementation of the ptz camera. 
This is a wrapper that will call the necessary commands to move the cameras.
One object for each camera
"""

from nodejs import node

class Movement:
    def __init__(self, IP):
        self.IP = IP
        
    def MoveUp(self):
        node.run(['/home/rafael/workspace/VisionTree/VisitantSearcher/Searcher/assets/ptz.js', self.IP, "UP"], )

    def MoveDown(self):
        node.run(['/home/rafael/workspace/VisionTree/VisitantSearcher/Searcher/assets/ptz.js', self.IP, "DWON"], )

    def MoveLeft(self):
        node.run(['/home/rafael/workspace/VisionTree/VisitantSearcher/Searcher/assets/ptz.js', self.IP, "LEFT"], )
    
    def MoveRight(self):
        node.run(['/home/rafael/workspace/VisionTree/VisitantSearcher/Searcher/assets/ptz.js', self.IP, "RIGHT"], )        