from fman.fs import FileSystem

from fman import DirectoryPaneCommand

class OpenExample(DirectoryPaneCommand):
	def __call__(self):
		self.pane.set_path('example://')

class Example(FileSystem):

	scheme = 'example://'

	def iterdir(self, path):
		if path == '':
			return ['Directory', 'File.txt', 'Image.jpg']
		elif path == 'Directory':
			return ['File in directory.txt']

	def is_dir(self, path):
		return path == 'Directory'
