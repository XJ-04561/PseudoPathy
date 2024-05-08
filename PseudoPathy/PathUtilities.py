
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

class PathAlias(Alias):
	def __get__(self, instance, owner=None):
		from PseudoPathy import Path, PathGroup
		if os.pathsep not in (path := super().__get__(instance, owner=owner)):
			return Path(path)
		else:
			return PathGroup(*path.split(os.pathsep))
	
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

class SoftwareDirs(AppDirs):
	"""This is what you want to override for installation/software-related files to go into a folder named after your Software"""

	SOFTWARE_NAME : str = "PseudoPathy"
	AUTHOR_NAME : str = None
	VERSION_NAME : str = None

	workDir : str	= os.curdir
	userDir			= USER_DIRECTORY

	appname : str = Alias("SOFTWARE_NAME")
	appauthor : str = Alias("AUTHOR_NAME")
	version : str = Alias("VERSION_NAME")
	multipath : bool = True

	userDataDir		= PathAlias("user_data_dir")
	siteDataDir		= PathAlias("site_data_dir")
	dataDir = siteDataDir | userDataDir

	userConfigDir	= PathAlias("user_config_dir")
	siteConfigDir	= PathAlias("site_config_dir")
	configDir = siteConfigDir | userConfigDir

	userCacheDir	= PathAlias("user_cache_dir")
	userLogDir		= PathAlias("user_log_dir")

	user_data_dir	= PathAlias("user_data_dir")
	user_config_dir	= PathAlias("user_config_dir")
	site_data_dir	= PathAlias("site_data_dir")
	site_config_dir	= PathAlias("site_config_dir")
	user_cache_dir	= PathAlias("user_cache_dir")
	user_log_dir	= PathAlias("user_log_dir")
	site_data_dir	= PathAlias("site_data_dir")