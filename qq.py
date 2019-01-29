import threading
from queue import Queue
import time
exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, lqueue):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.tqueue = lqueue
      
      
   def run(self):
      print ("Starting " + self.name)
      # print_time(self.name, self.counter, 5)
      msg=0
      while msg != -1:
        msg = self.tqueue.get()
        self.do_work(msg)
        self.tqueue.task_done()
      print ("Exiting " + self.name)


   def do_work(self, count):
   	   print ("Work " + self.name +" :"+str(count))
   	   print_time(self.name, self.counter,  count)
        

def print_time(threadName, delay, counter):
   for i in range(counter):
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1


def main():
	# Create new threads
	tq1= Queue()
	tq2= Queue()
	thread1 = myThread(1, "Thread-1", 5, tq1)
	thread2 = myThread(2, "Thread-2", 4, tq2)
	
	# Start new Threads
	thread1.start()
	thread2.start()
	tq1.put(2)
	tq2.put(3)
	tq1.put(-1)
	tq2.put(1)
	tq2.put(-1)
	
	thread1.join()
	thread2.join()


if __name__== "__main__":
  main()
