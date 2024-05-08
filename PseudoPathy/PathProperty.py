
from PseudoPathy.Globals import *
import PseudoPathy.Globals as Globals

class PathProperty(property):
	def __truediv__(self, right):
		return PathProperty(lambda instance : self.fget(instance) / right)
	def __add__(self, right):
		return PathProperty(lambda instance : self.fget(instance) + right)
	def __rtruediv__(self, left):
		return PathProperty(lambda instance : left / self.fget(instance))
	def __or__(self, right):
		return PathProperty(lambda instance : self.fget(instance) | right)
	def __ror__(self, left):
		return PathProperty(lambda instance : left | self.fget(instance))