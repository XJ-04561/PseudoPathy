
from PseudoPathy.Globals import *
import PseudoPathy.Globals as Globals

class PathProperty(property):

	def __get__(self, *args, **kwargs):
		print(self, args, kwargs)
		property.__get__(self, *args, **kwargs)

	def __truediv__(self, right):
		def truediv(instance):
			self.fget(instance) / right
		return PathProperty(truediv)
	def __add__(self, right):
		def add(instance):
			return self.fget(instance) + right
		return PathProperty(add)
	def __rtruediv__(self, left):
		def rtruediv(instance):
			return left / self.fget(instance)
		return PathProperty(rtruediv)
	def __or__(self, right):
		def _or(instance):
			return self.fget(instance) | right
		return PathProperty(_or)
	def __ror__(self, left):
		def ror(instance):
			return left | self.fget(instance)
		return PathProperty(ror)

class PathAlias(Alias, PathProperty):

	def __get__(self, instance, owner=None):
		from PseudoPathy import Path, PathGroup
		if os.pathsep not in (path := super().__get__(instance, owner=owner)):
			return Path(path)
		else:
			return PathGroup(*path.split(os.pathsep))

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