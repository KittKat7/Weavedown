import os

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

	def generate(self):
		"""
		Goes through all files, and generate output files in the output directory
		"""

		while len(self.dirs) > 0:
			if not os.path.exists(os.path.join(self.outDir, self.dirs[0])):
				os.makedirs(os.path.join(self.outDir, self.dirs[0]))
			self.dirs.remove(self.dirs[0])
		#while

		# if the directory does not exist, throw an exception
		if not os.path.exists(self.dir):
			raise Exception()
		
		# if the output directory does not exist, make it
		if not os.path.exists(self.outDir):
			os.makedirs(self.outDir)

		while len(self.files) > 0:
			self.__generateFile(0)
		#while
	#generate

	def __generateFile(self, index: int):
		"""
		Generate an output for the given file
		"""
		if self.files[index].split(".")[len(self.files[index].split("."))-1] not in ["html", "md"]:
			data = None
			with open(os.path.join(self.dir, self.files[index]), "rb") as file:
				data = file.read()
			with open(os.path.join(self.outDir, self.files[index]), "wb") as file:
				file.write(data)
			self.files.remove(self.files[index])
			return

		filePath: str = self.files[index]
		inputStr: str
		outputStr: str


		with open(os.path.join(self.dir, filePath), "r") as file:
			inputStr = file.read()

		parser: Parser = Parser(inputStr)
		parser.tokenize()
		parser.parse()

		refs: list[str] = parser.getReferences()
		refsReplace: list[str] = []
		for ref in refs:
			# if the required file has not been parsed, parse it
			if ref not in self.parsedFiles:
				self.__generateFile(self.files.index(ref))
			#if

			# read the file from the output and put it in the replacement reference file
			with open(os.path.join(self.outDir, filePath), "w") as file:
				refsReplace.append(file.read())
			#with
		#for

		outputStr = parser.getOutput()

		filePath = os.path.splitext(filePath)[0]+".html"

		with open(os.path.join(self.outDir, filePath), "w") as file:
			file.write(outputStr)

		self.files.remove(self.files[index])
	#__generateFile
#Generator

class Parser:
	"""
	The parser parses markdown and weavedown syntax
	"""

	__keywords: list[str] = [
		"#","##","###","####","#####","######", # heading
		"*","**","***",
		"![", # embed
	]

	def __init__(self, inputStr: str):
		"""
		Constructor
		Initiates the Parser with the inputStr
		"""
		self.__inputStr: str = inputStr
		self.__outputStr: str = ""

		self.__parts: list[str] = []
		self.__indexsOfRefs: list[int] = []
	#__init__

	def tokenize(self):
		"""
		
		"""
		self.__tokens: list[list[str]] = []

		newLine: bool = True
		continueTo: str = ""

		for c in self.__inputStr:
			if continueTo == c:
				continueTo = ""
				continue
			elif continueTo != "":
				self.__tokens[len(self.__tokens) - 1][1] += c
				continue
			#if/elif

			newLine =  c == '\n'
			if newLine and c == "#":
				self.__tokens.append(["HEADING", ""])
				self.__tokens[len(self.__tokens) - 1][1] += "#"
				continueTo = "\n"
				continue
			#if
		#for

			newLine = False
		print(self.__tokens)
	# tokenize

	def parse(self):
		"""
		Parses the text provided to the constructor. Will generate a list of references if any
		exist.
		""" # TODO
		self.__outputStr = self.__inputStr
	#parse

	def getReferences(self) -> list[str]:
		"""
		TODO
		"""
		return [self.__parts[r] for r in self.__indexsOfRefs] # TODO
	#getReferences

	def setReferences(self, refs: list[str]):
		"""
		TODO
		"""
		for i in range(len(refs)):
			self.__parts[self.__indexsOfRefs[i]] = refs[i]
		#for
	#setReferences

	def getOutput(self) -> str:
		"""
		TODO
		"""
		return self.__outputStr # TODO
	#getOutput
#__Parser

