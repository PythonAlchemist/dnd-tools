from src.dataloader.script import ScriptParser
from src.utils import ROOT_DIR

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

data = f"{ROOT_DIR}/data/crititcalrole/(2x01)_CuriousBeginnings.txt"
parser = ScriptParser(data)

example = parser.lines[2]["dialogue"]


from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/distilbert-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/distilbert-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

ner_results = nlp(example)

# print meanful results
for result in ner_results:
    if result["entity"] != "LABEL_0":
        print(result)
