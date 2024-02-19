import subprocess
import time



class actions:

    def __init__(self):

        pass

    class definitions:              #WAIT UNTIL YOUR ACTION HAS FINISHED

        def yourAction():

            returncode = subprocess.call("executing a python script", shell=True)
            return