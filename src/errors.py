#errors.py

class ParseError(Exception):
    def __init__(self, message, token, source_lines):
        self.message = message
        self.token = token
        self.source_lines = source_lines
        super().__init__(self.__str__())

    def __str__(self):
        line = self.token.line
        col = self.token.column
        code_line = self.source_lines[line - 1] if 0 <= line - 1 < len(self.source_lines) else ""

        pointer = " " * (col - 1) + "^"
        return (
            f"\nParseError: {self.message}"
            f" --> Line {line}"
        )
