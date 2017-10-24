class Queue():
    def __init__(self, size):
        self.size = size
        self.front = -1
        self.rear = -1
        self.queue = []

    def enqueue(self, ele):
        if self.isfull():
            raise Exception("queue is full")
        else:
            self.queue.append(ele)
            self.rear = self.rear + 1

    def dequeue(self):
        if self.isempty():
            raise Exception("queue is empty")
        else:
            self.queue.pop(0)
            self.front = self.front + 1

    def isfull(self):
        return self.rear - self.front + 1 == self.size

    def isempty(self):
        return self.front == self.rear

    def showQueue(self):
        print self.queue
