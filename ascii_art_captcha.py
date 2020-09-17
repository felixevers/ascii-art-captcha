from art import text2art
from typing import NoReturn, List
from string import ascii_uppercase
from random import choices


class Captcha:
    def __init__(self, ascii_art: str, solution: str, *, max_fails: int = 0):
        self._ascii_art = ascii_art
        self._fails = 0
        self._max_fails = max_fails
        self._solution = solution
        self._solved = False

    @property
    def failed(self) -> bool:
        return 0 < self._max_fails <= self._fails

    @property
    def solved(self) -> bool:
        return self._solved

    def check(self, user_input: str, /) -> bool:
        if self.failed:
            return False

        if user_input.lower() == self._solution.lower() or self._solved:
            self._solved = True
            return True

        self._fails += 1
        return False

    def print(self) -> NoReturn:
        print(self)
        print()

    def check_user_input(self, prompt: str = "ENTER CODE > ") -> bool:
        user_input: str = input(prompt)
        return self.check(user_input)

    def execute(self) -> bool:
        self.print()

        while not self.failed and not self._solved:
            if self._max_fails > 0:
                print(self._max_fails - self._fails, "attempts left...")

            result: bool = self.check_user_input()

            if result:
                print("SOLVED!")
                return True
            elif self.failed:
                print("FAILED!")
                return False

            print("WRONG!")

    def __repr__(self) -> str:
        return self._ascii_art

    def __str__(self) -> str:
        return self._ascii_art

    @staticmethod
    def generate(*, length: int = 5, max_fails: int = 3) -> "Captcha":
        base: List[str] = [""]
        solution: str = "".join(choices(ascii_uppercase, k=length))

        current_length: int = 0

        for character in solution:
            ascii_art: str = text2art(character, font="random")
            lines: List[str] = ascii_art.split("\r\n")

            max_length: int = max(map(len, lines))

            for index, line in enumerate(lines):
                if index >= len(base):
                    base.append(current_length * " ")

                base[index] += line

            for index in range(len(base)):
                base[index] = base[index].ljust(current_length + max_length)

            current_length = max(map(len, base))

        while len(base[0].strip()) == 0:
            del base[0]

        while len(base[-1].strip()) == 0:
            del base[-1]

        ascii_art: str = "\r\n".join(base)

        return Captcha(ascii_art=ascii_art, solution=solution, max_fails=max_fails)


if __name__ == "__main__":
    captcha: Captcha = Captcha.generate()
    captcha.execute()
