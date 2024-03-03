import subprocess
import time



class actions:

    def __init__(self):

        pass

    class definitions:              #WAIT UNTIL YOUR ACTION HAS FINISHED, DO NOT CATCH ERRORS IF YOU WANT THEM TO BE SENT AS A NOTIFICATION 

        def yourAction():

            returncode = subprocess.call("executing a python script", shell=True)
            return {"myData": "It worked", "returncode": returncode}