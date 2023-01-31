from threading import Thread

class MiniMaxThread(Thread):
    value = None
    def __init__(self):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.value = None
 
    # function executed in a new thread
    def run(self):
        # block for a moment
        sleep(1)
        # store data in an instance variable
        self.value = 'Hello from a new thread'