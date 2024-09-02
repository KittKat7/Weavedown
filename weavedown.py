import os, re

class Generator:
	"""
	
	"""
	
	def __init__(self, inDir: str, outDir: str):
		"""
		Constructor:
		Inits a Generator in the given directory, the output files will be in [output]
		"""
		self.dir: str = inDir
		self.outDir: str = outDir
		self.files: list[str]
		self.dirs: list[str] = []
		self.parsedFiles: list[str]
		
		self.files = self.__getFiles(self.dir)
	#__init__

	def __getFiles(self, direct: str) -> list[str]:
		"""
		Returns a list of file names in the given directory
		"""
		files: list[str] = []
		directory = os.scandir(direct)
		for item in directory:
			if item.is_file():
				files.append(item.path)
			elif item.is_dir():
				if item.path.startswith(self.outDir):
					continue
				self.dirs.append(item.path)
				files += self.__getFiles(item.path)
		return files
	#__getFiles

	@staticmethod
	def __getFileExtension(path: str) -> str:
		"""
		
		"""
		return path.split(".")[len(path.split("."))-1]
	#getFileExtension

	@staticmethod
	def __setFileExtension(path: str, extension: str) -> str:
		"""
		
		"""
		return path[:-len(Generator.__getFileExtension(path))] + extension
	#getFileExtension

	def generateDirectories(self):
		"""
		"""
		while len(self.dirs) > 0:
			if not os.path.exists(os.path.join(self.outDir, self.dirs[0][len(self.dir):])):
				os.makedirs(os.path.join(self.outDir, self.dirs[0][len(self.dir):]))
			self.dirs.remove(self.dirs[0])
		#while

		# if the directory does not exist, throw an exception
		if not os.path.exists(self.dir):
			raise Exception()
		
		# if the output directory does not exist, make it
		if not os.path.exists(self.outDir):
			os.makedirs(self.outDir)
	#generateDirectories

	def generateFiles(self):
		"""
		"""
		files: list[str] = list.copy(self.files)
		while len(files) > 0:
			filestr: str = files.pop()
			data: object
			if Generator.__getFileExtension(filestr) in ["mdhtml"]:
				with open(filestr, "r") as file:
					data = file.read()
				with open(os.path.join(self.outDir, Generator.__setFileExtension(filestr, "html")[len(self.dir):]), "w") as file:
					file.write("<!-- Compiled by Weavedown -->\n" + data)
			else:
				with open(filestr, "rb") as file:
					data = file.read()
				with open(os.path.join(self.outDir, filestr[len(self.dir):]), "wb") as file:
					file.write(data)
	#generateFiles

	def parseImports(self):
		"""
		"""
		files: list[str] = list.copy(self.files)
		while len(files) > 0:
			filestr: str = os.path.join(self.outDir, files.pop()[len(self.dir):])
			if Generator.__getFileExtension(filestr) not in ["mdhtml", "html", "md", "css", "js", "txt"]:
				continue
			if Generator.__getFileExtension(filestr) == "mdhtml":
				filestr = Generator.__setFileExtension(filestr, "html")

			print("Checking " + filestr + " for imports")

			with open(filestr, "r") as file:
				data = file.read()
				while re.search(r'!\[.*?\]\((.*?)\)', data) is not None:
					search: object = re.search(r'!\[.*?\]\((.*?)\)', data)
					path: str = search.group(1) # type: ignore
					if path.startswith("./"):
						path = os.path.join(self.outDir, path[2:])
					if Generator.__getFileExtension(path) == "mdhtml":
						path = Generator.__setFileExtension(path, "html")

					importedData: str
					with open(path, "r") as imported:
						importedData = imported.read()

					data = re.sub(rf'!\[.*?\]\({re.escape(search.group(1))}\)', # type: ignore
						"<!-- Imported by Weavedown -->" + importedData + "<!-- End Import -->", data)

					print(path)
			
			with open(filestr, "w") as file:
				file.write(data)

	#parseImports

