from src.dataloader.script import ScriptParser
from src.utils import ROOT_DIR


data = f"{ROOT_DIR}/data/crititcalrole/(2x01)_CuriousBeginnings.txt"
parser = ScriptParser(data)
print(parser.lines[:5])
