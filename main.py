"""
TODO:
- [ ] get a list of files to parse
- [ ] parse md
	- [ ] normal md
	- [ ] weavedown specific
		- [ ] imports

for every file, parse (if it references an unparsed file, parse that one), put parsed file in output


STEPS:
Get a list of every file
while the list is not empty
	process the first file
	remove file from list
while

process file
	process.....
	if it references another file and that file is not processed
		process that file
	if
process file

NOTES:
processed files are stored in ./out/...
Takes the directory as the parameter, if none provided, currect '.' dir
The list of files is a list of relative paths for the files


generate output folder directories
copy files to output directory, if md file, parse to html
go through files and look for imports, if it contains an import, replace it with the referenced file

"""




import sys, subprocess, os
from weavedown import Generator

def main():
	"""
	The main function to run weavedown.
	"""
	# TODO add better param handling
	if len(sys.argv) < 2:
		sys.exit("ERROR: Missing in directory")
	if len(sys.argv) < 3:
		sys.exit("ERROR: Missing out directory")

	directory: str = sys.argv[1]
	outDirectory: str = sys.argv[2]

	parser: Generator = Generator(directory, outDirectory)

	parser.generateDirectories()
	parser.generateFiles()
	parser.parseImports()

#main

if __name__ == "__main__":
	if "--update" in sys.argv:
		subprocess.run(["bash", "update.sh"], cwd=os.path.dirname(os.path.realpath(__file__)))
		sys.exit()
	main()
#if