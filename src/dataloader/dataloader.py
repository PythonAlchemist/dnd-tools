from src.utils import ROOT_DIR
from typing import Union


class ScriptParser:
    def __init__(self, script_path):
        self.script_path = script_path
        self.speakers = {}

    def tagger(self, line) -> dict[str, str]:
        """
        This function takes a line of dialogue and returns a dictionary with the speaker and the dialogue.
        """
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
        line = line.replace("\n", "")

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

        print(cleaned_lines)


if __name__ == "__main__":
    parser = ScriptParser(f"{ROOT_DIR}/data/crititcalrole/(2x01)_CuriousBeginnings.txt")
    lines = parser.parse()
    print(lines)
