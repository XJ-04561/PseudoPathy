
from PseudoPathy.Alignments import *
from PseudoPathy import FilePath

def test_align2():
	path1, path2 = FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_1.fastq"), FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_2.fastq")

	assert align2(path1, path2) == "/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_X.fastq"

	assert align2(path1.file, path2.file) == "FSC148_X.fastq"

def test_align():
	path1, path2 = FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_1.fastq"), FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_2.fastq")

	assert align(path1, path2) == "/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_X.fastq"

	assert align(path1.file, path2.file) == "FSC148_X.fastq"

def test_alignSignature():
	path1, path2 = FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_1.fastq"), FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_2.fastq")

	assert alignSignature(path1, path2) == "home_fredrik_Data_FASTQ_DATA_FSC148_illumina_FSC148_fastq"

	assert alignSignature(path1.file, path2.file) == "FSC148_fastq"

def test_alignName():
	path1, path2 = FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_1.fastq"), FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_2.fastq")

	assert alignName(path1, path2) == "/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_.fastq"

	assert alignName(path1.file, path2.file) == "FSC148_.fastq"
	assert alignName(path1.name, path2.name) == "FSC148"

def test_alignPattern():
	path1, path2 = FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_1.fastq"), FilePath("/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_2.fastq")

	assert alignPattern(path1, path2) == "/home/fredrik/Data/FASTQ_DATA/FSC148/illumina/FSC148_?.fastq"

	assert alignPattern(path1.file, path2.file) == "FSC148_?.fastq"