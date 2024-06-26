from src.utils import ROOT_DIR
from typing import Union
import re
import json
from src.dataclass.script import Script


class ScriptParser:
    def __init__(self, script_path):
        self.script_path = script_path
        self.lines: Script = Script([])
        self.parse()

    def tokenize(self, line) -> list[str]:
        """
        This function takes a line of dialogue and returns a list of tokens.
        """
        pattern = r"[\w]+|[^\w\s]"
        tokens = re.findall(pattern, line)
        return tokens

    def combine_lines(self):
        """
        This function combines lines of dialogue from the same speaker.
        """

        combined_lines = [self.lines[0]]

        for line in self.lines[1:]:

            # if speaker is different from previous line, add line to list
            if line["speaker"] != combined_lines[-1]["speaker"]:
                combined_lines.append(line)

            # if same speaker as previous line, combine dialogue
            elif line["speaker"] == combined_lines[-1]["speaker"]:
                combined_lines[-1]["dialogue"] += f" {line['dialogue']}"
            else:
                combined_lines.append(line)

        self.lines = combined_lines

    def sentence_splitter(self) -> None:
        """
        This function splits dialogue into individual sentences.
        """

        split_lines = []

        for line in self.lines:
            sentences = line["dialogue"].split(".")
            for sentence in sentences:
                if sentence != "":
                    split_lines.append(
                        {"speaker": line["speaker"], "dialogue": sentence.strip()}
                    )

        self.lines = split_lines

    def tagger(self, line) -> dict[str, str]:
        """
        This function takes a line of dialogue and returns a dictionary with the speaker and the dialogue.
        """

        # re pattern for speaker
        pattern = r"^[A-Z]+:"

        # if line does not match pattern, return line as dialogue
        if not re.match(pattern, line):
            return {"speaker": None, "dialogue": line}

        # find speaker
        speaker = line.split(":")[0]
        speaker = speaker.strip()

        # find dialogue
        dialogue = line.split(":")[1]
        dialogue = dialogue.strip()

        return {"speaker": speaker, "dialogue": dialogue}

    def clean_line(self, line) -> Union[str, None]:
        """
        This function takes a line from a script and returns the line if it is dialogue, otherwise it returns None.
        """

        # clean line
        line = line.strip()

        # check if line is empty
        if not line:
            return None

        # check for non-dialogue lines
        if line.startswith("(") and line.endswith(")"):
            return None
        # check for stage directions
        elif line.startswith("[") and line.endswith("]"):
            return None

        return line

    def parse(self):
        with open(self.script_path, "r") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            if cleaned_line := self.clean_line(line):
                cleaned_lines.append(cleaned_line)

        for line in cleaned_lines:
            self.lines.append(self.tagger(line))

        self.combine_lines()
        # self.sentence_splitter()

    def write_cleaned_script(self, output_path):
        with open(output_path, "w") as f:
            for line in self.lines:
                json.dump(line, f, ensure_ascii=False)
                f.write("\n")

    def prepare_annotation(self, output_path):
        with open(output_path, "w") as f:
            for line in self.lines:
                # line["gameplay"] = False
                # line["tokens"] = self.tokenize(line["dialogue"])
                # line["ner_tags"] = ["O" for _ in line["tokens"]]
                line["text"] = f"{line['speaker']}: {line['dialogue']}"
                del line["dialogue"]
                json.dump(line, f, ensure_ascii=False)
                f.write("\n")


if __name__ == "__main__":
    parser = ScriptParser(f"{ROOT_DIR}/data/raw/(2x01)_CuriousBeginnings.txt")
    parser.write_cleaned_script(f"{ROOT_DIR}/data/clean/1.jsonl")
    parser.prepare_annotation(f"{ROOT_DIR}/data/annotated/1.jsonl")
