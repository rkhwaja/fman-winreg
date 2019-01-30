from datetime import datetime, timedelta, timezone
from os.path import basename, dirname
from winreg import ConnectRegistry, EnumKey, EnumValue, HKEY_CURRENT_USER, OpenKey, QueryInfoKey, QueryValueEx

from fman import DirectoryPaneCommand, show_alert
from fman.fs import Column, FileSystem
from fman.url import splitscheme

_scheme = "winreg://"

class WinReg(DirectoryPaneCommand):
	def __call__(self):
		self.pane.set_path(_scheme)

class Value(Column):
	def get_str(self, url):
		scheme, path = splitscheme(url)
		rootKey = ConnectRegistry(None, HKEY_CURRENT_USER)
		parent = dirname(path).replace("/", "\\")
		valueName = basename(path)
		try:
			key = OpenKey(rootKey, parent)
		except EnvironmentError:
			return None
		try:
			value = QueryValueEx(key, valueName)
		except EnvironmentError:
			return None
		return str(value[0])

class WinRegFileSystem(FileSystem):

	scheme = _scheme

	def iterdir(self, path):
		localPath = path.replace("/", "\\")
		rootKey = ConnectRegistry(None, HKEY_CURRENT_USER)
		key = OpenKey(rootKey, localPath)
		result = []
		index = 0
		while True:
			try:
				result.append(EnumKey(key, index))
			except EnvironmentError:
				break
			index = index + 1

		index = 0
		while True:
			try:
				name, value, type_ = EnumValue(key, index)
				result.append(name)
			except EnvironmentError:
				break
			index = index + 1
		return result

	def get_default_columns(self, path):
		return "core.Name", "core.Modified", "winreg_plugin.Value"

	def modified_datetime(self, path):
		localPath = path.replace("/", "\\")
		rootKey = ConnectRegistry(None, HKEY_CURRENT_USER)
		try:
			key = OpenKey(rootKey, localPath)
			subKeyCount, valueCount, lastModified = QueryInfoKey(key)
			return datetime(1600, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=lastModified * 100e-9)
		except EnvironmentError:
			# TODO raise FileNotFoundError if path isn't a value
			return None

	def is_dir(self, path):
		localPath = path.replace("/", "\\")
		rootKey = ConnectRegistry(None, HKEY_CURRENT_USER)
		try:
			key = OpenKey(rootKey, localPath)
			return True
		except EnvironmentError:
			pass
		parent = dirname(path).replace("/", "\\")
		valueName = basename(path)
		key = OpenKey(rootKey, parent)
		value = QueryValueEx(key, valueName)
		return False
