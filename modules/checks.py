import datetime


class checks:

    def __init__(self):

        pass

    class definitions:              #CHECKS HAVE TO RETURN A BOOL

        def yourCheck():

            currentTime = datetime.datetime.now().strftime("%H%M")
            if(currentTime == "1435"):
                return True

            return False