import os, re
import markdown


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
		print(self.dirs)
		print(self.files)
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

	def generateDirectories(self):
		"""
		"""
		while len(self.dirs) > 0:
			if not os.path.exists(os.path.join(self.outDir, self.dirs[0][len(self.dir) + 1:])):
				os.makedirs(os.path.join(self.outDir, self.dirs[0][len(self.dir) + 1:]))
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
			if filestr.split(".")[len(filestr.split("."))-1] in ["mdhtml"]:
				with open(filestr, "r") as file:
					data = file.read()
				with open(os.path.join(self.outDir, filestr[len(self.dir) + 1:-7] + ".html"), "w") as file:
					file.write("<!-- Compiled by WeaveDown -->\n" + data)
			else:
				with open(filestr, "rb") as file:
					data = file.read()
				with open(os.path.join(self.outDir, filestr[len(self.dir) + 1:]), "wb") as file:
					file.write(data)
	#generateFiles

	def parseImports(self):
		"""
		"""
		files: list[str] = list.copy(self.files)
		while len(files) > 0:
			filestr: str = os.path.join(self.outDir, files.pop()[len(self.dir) + 1:])
			if filestr[-7:] == ".mdhtml":
				print("=====")
				print(filestr)
				filestr = filestr[:-7] + ".html"
				print(filestr)

			with open(filestr, "r") as file:
				data = file.read()
				while re.search(r'!\[.*?\]\((.*?)\)', data) is not None:
					search: object = re.search(r'!\[.*?\]\((.*?)\)', data)
					path: str = search.group(1) # type: ignore
					if path.startswith("./"):
						path = os.path.join(self.outDir, path[2:])
					if path[-7:] == ".mdhtml":
						path = path[:-7] + ".html"

					importedData: str
					with open(path, "r") as imported:
						importedData = imported.read()

					data = re.sub(rf'!\[.*?\]\({re.escape(search.group(1))}\)', # type: ignore
						"<!-- Imported by WeaveDown -->" + importedData + "<!-- End Import -->", data)

					print(path)
			
			with open(filestr, "w") as file:
				file.write(data)

	#parseImports

