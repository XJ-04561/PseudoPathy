
from PseudoPathy.Globals import *
import PseudoPathy.Globals as Globals
from PseudoPathy.PathProperty import PathProperty

class PathAlias(Alias, PathProperty):
	def __get__(self, instance, owner=None):
		from PseudoPathy import Path, PathGroup
		if os.pathsep not in (path := super().__get__(instance, owner=owner)):
			return Path(path)
		else:
			return PathGroup(*path.split(os.path.sep))

class SoftwareDirs(AppDirs, metaclass=Rename):

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