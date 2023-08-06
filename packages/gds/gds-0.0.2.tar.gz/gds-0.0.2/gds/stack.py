class Stack:
	
	def __init__(self):
		'''Create an empty stack'''
		self.stack = list()
	
	def push(self, obj):
		'''Push object to the stack'''
		self.stack.append(obj)
	
	def pop(self):
		'''Pop object from the stack'''
		return self.stack.pop()
	
	def peek(self):
		'''Peek object at the top of the stack'''
		return self.stack[-1]
	
	def is_empty(self):
		'''Check if stack is empty or not'''
		return not self.stack