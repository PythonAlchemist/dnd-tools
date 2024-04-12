class Line(dict):
    def __init__(self, speaker: str, dialogue: str):
        self.speaker = speaker
        self.dialogue = dialogue

    def __str__(self):
        return f"{self.speaker}: {self.dialogue}"


class Script(list[Line]):
    def __init__(self, lines: list[Line]):
        self.lines = [Line(**line) for line in lines]

    def __str__(self):
        return "\n".join([str(line) for line in self.lines])
