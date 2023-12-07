#main file of the searcher.

"""This will be responsible to:
* launch the flask application that will stream the data
* launch all the thread's of processing and ensure they are alive
* receive notification of processing available for every camera
    * notification will come from a http post.
* every processing house will have an entrance and outgoing
* no database will be available
* processed pictures will be saved with their metadata
"""

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()