from __future__ import annotations

from io import StringIO
from typing import Optional, List, Tuple


class WalkmanException(Exception):

    pass


class ParsingError(WalkmanException):

    def __init__(self, message: str, begin: Location, end: Location = None):
        super().__init__(
            f'{begin}: {message}' if end is None else
            f'{begin.area(end)}: {message}'
        )


class Location:

    def __init__(self, source: Source, position: int):
        self.source = source
        self.position = position

    def area(self, end: Location) -> LocationArea:
        return LocationArea(self, end)

    def error(self, message: str) -> ParsingError:
        return ParsingError(message, self)

    def __str__(self):
        line, column = self.source.get_coordinates(self.position)
        return f'{self.source.src}@[{line + 1},{column + 1}]'


class LocationArea:

    def __init__(self, begin: Location, end: Location):
        if begin.source != end.source:
            raise WalkmanException('Begin and end sources do not match.')

        self.begin = begin
        self.end = end

    def error(self, message: str) -> ParsingError:
        return ParsingError(message, self.begin, self.end)

    def __str__(self):
        src = self.begin.source.src
        l1, c1 = self.begin.source.get_coordinates(self.begin.position)
        l2, c2 = self.end.source.get_coordinates(self.end.position)
        return (
            f'{src}@[{l1 + 1}, {c1 + 1}]-[{l2 + 1}, {c2 + 1}]')


class Source:

    def __init__(
            self,
            text: str,
            src: Optional[str] = None,
            position: int = 0):
        self.text = text
        self.length = len(text)
        self.src = src
        self.position = position

    @staticmethod
    def from_file(file_path):
        with open(file_path, mode='r') as f:
            text = f.read()

        return Source(text, file_path)

    @property
    def location(self) -> Location:
        return Location(self, self.position)

    def error(self, message: str):
        return self.location.error(message)

    def substring(self, begin: int, end: int) -> str:
        if begin > end:
            raise WalkmanException(
                'Begin position must be less than end position.')
        return self.text[begin:end]

    def peek(self) -> Optional[str]:
        if self.position < self.length:
            return self.text[self.position]
        return None

    def move_next(self) -> bool:
        if self.position < self.length:
            self.position += 1
            return True
        return False

    def try_move(self, delta=1) -> int:
        count = 0

        for i in range(delta):
            if self.move_next():
                count += 1
            else:
                break

        return count

    def test_any(self, tokens: List[str]) -> bool:
        for token in tokens:
            if self.test(token):
                return True
        return False

    def test(self, token: Optional[str]) -> bool:
        if token is None:
            return False

        pos0 = self.position

        for expected_char in token:
            actual_char = self.peek()

            if actual_char is None or actual_char != expected_char:
                self.position = pos0
                return False

            self.move_next()

        self.position = pos0
        return True

    def pull_any(self, tokens: List[str]) -> Optional[str]:
        for token in tokens:
            if self.pull(token):
                return token
        return None

    def pull(self, token: Optional[str]) -> bool:
        if token is None:
            return False

        pos0 = self.position

        for expected_char in token:
            actual_char = self.peek()

            if actual_char is None or actual_char != expected_char:
                self.position = pos0
                return False

            self.move_next()

        return True

    def read(self, length: int = 1) -> str:
        out = StringIO()

        for i in range(length):
            c = self.peek()

            if c is None:
                raise self.error('Unexpected EOF.')

            out.write(c)
            self.move_next()

        return out.getvalue()

    def expect(self, token: str):
        if not self.pull(token):
            return self.error(f'Expected token: {token}')

    def expect_any(self, tokens: List[str]):
        pulled = False

        for token in tokens:
            if self.pull(token):
                pulled = True
                break

        if not pulled:
            return self.error(f'Expected any of tokens: {", ".join(tokens)}')

    def get_coordinates(self, some_position: int) -> Tuple[int, int]:
        line = 0
        column = 0

        for index, c in enumerate(self.text):
            if c == '\n':
                line += 1
                column = 0
            else:
                column += 1

            if index >= some_position:
                break

        return line, column
