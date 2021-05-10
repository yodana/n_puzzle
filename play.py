import argparse
from src.parserTools import *
from src.game import TaquinGame

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="Must be a valid taquin file")
	args = parser.parse_args()
	if not getattr(args, 'file'):
		error('file expected')
	TaquinGame(getBoard(args.file), [])