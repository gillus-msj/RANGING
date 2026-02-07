import threading
import queue
from abc import ABC, abstractmethod

class ProducerThread(threading.Thread, ABC):
    QUEUE_SIZE = 1

    def __init__(self):
        super(ProducerThread, self).__init__()
        self.exitFlag = False
        self.queue = queue.Queue(ProducerThread.QUEUE_SIZE)

    def run(self):
        while not self.exitFlag:
            self.queue.put(self.produce())
        return

    def get(self):
        ''' Called from external thread to wait for item ''' 
        return self.queue.get()

    def terminate(self):
        ''' Called from external thread to stop ''' 
        self.exitFlag = True
        # Flush the queue
        self.queue.get()
        self.close()

    @abstractmethod
    def produce(self):
        pass
    
    @abstractmethod
    def close(self):
        pass
    