from re import split
from typing import Optional, Self


def contains_item_at_every_pos(string, items):
    for i in range(len(string)):
        found_match = False
        for item in items:
            if string[i] == item:
                found_match = True
                break
        if not found_match:
            return False
    return True


class Type:
    def __init__(self, name: str, type_category: Optional[Self] = None) -> None:
        self.name = name
        self.type_category = type_category

    def __repr__(self) -> str:
        type_ = self
        lst = [self.name]
        while type_.type_category is not None:
            lst.append(type_.type_category.name)
            type_ = type_.type_category
        lst.reverse()
        return ":".join(lst)

    def __call__(self, val):
        return Token(self, val)

    def __hash__(self) -> int:
        return hash(self.name)


UNKNOWN = Type("UNKNOWN")

KEYWORD = Type("KEYWORD")
TYPE = Type("TYPE", KEYWORD)

VALUE = Type("VALUE")
NUM = Type("NUM", VALUE)
FRAC = Type("FRAC", NUM)

LST = Type("LST", VALUE)

STR = Type("STR", VALUE)


OPERATOR = Type("OPERATOR")


class IdToken:
    tokens: list[Self] = []

    def __init__(self, type_: Type, values: str | list[str]) -> None:
        self.type_ = type_
        self.values = values

        type(self).tokens.append(self)

        if isinstance(values, str):
            self.value = values


NUMBER = list("1234567890.")


IdToken(TYPE, "num")
IdToken(TYPE, "frac")

IdToken(OPERATOR, "=")
IdToken(OPERATOR, "/")
IdToken(OPERATOR, "-")

IdToken(NUM, NUMBER)


class Token:
    def __init__(self, type_: Type, value: str) -> None:
        self.type_ = type_
        self.value = value

    def __repr__(self) -> str:
        return repr(self.type_) + f'("{self.value}")'

    def __eq__(self, __value: Self) -> bool:
        return str(self) == str(__value)

    def __hash__(self) -> int:
        return hash(str(self.type_) + str(self.value))


class Lexer:
    def __init__(self, code) -> None:
        self.code = code.replace(" ", "")

    def split(self):
        """Split the code into pieces based of the IdTokens."""
        pattern = (
            "("
            + "|".join(
                token.value for token in IdToken.tokens if hasattr(token, "value")
            )
            + ")"
        )
        self.splits = list(
            filter(
                None,
                split(
                    pattern,
                    self.code,
                ),
            )
        )

    def lex(self):
        """Covert the split pieces into Token objects."""
        tokens = []
        for token in self.splits:
            for token_ in IdToken.tokens:
                if token == token_.values or contains_item_at_every_pos(
                    token, token_.values
                ):
                    tokens.append(Token(token_.type_, token))
                    break
            else:
                tokens.append(Token(UNKNOWN, token))
        self.tokens: list[Token] = tokens
        return tokens

    def stop_keywords_in_names(self, types: tuple[Type, ...]):
        """
        Turns this
        ```
        int varint = 5 -> TYPE("int"), TYPE("var"), TYPE("int"), OPERATOR("="), NUM("5")
        ```
        Into this
        ```
        int varint = 5 -> TYPE("int"), TYPE("varint"), OPERATOR("="), NUM("5")

        """

        def remove_and_add_duplicates(lst):
            seen = set()
            for i in range(len(lst)):
                if lst[i].type_ in types:
                    if lst[i] in seen:
                        lst[i - 1].value += lst[i].value
                        lst.pop(i)
                        break
                    else:
                        seen.add(lst[i])

        remove_and_add_duplicates(self.tokens)

    def fractions_combine(self):
        pre = 0
        next_ = 0
        for i in range(len(self.tokens)):
            pre = i - 1
            next_ = i + 1

            if i > 0 and i < len(self.tokens):
                if (
                    self.tokens[pre].type_ is NUM
                    and self.tokens[i] == OPERATOR("/")
                    and self.tokens[next_].type_ is NUM
                ):
                    value = (
                        self.tokens[pre].value
                        + self.tokens[i].value
                        + self.tokens[next_].value
                    )

                    self.tokens.pop(pre)
                    self.tokens.pop(i - 1)
                    self.tokens.pop(next_ - 2)
                    self.tokens.insert(
                        i,
                        Token(
                            FRAC,
                            value,
                        ),
                    )

    def combine(self, converts: dict[tuple[Type | Token], Type | Token]) -> None:
        """
        Combine types and tokens into one token.

        ```
        [NUM('1'), OPERATOR('/'), NUM('2')]
        >>> lexer.combine({(NUM, OPERATOR("/"), NUM): FRAC)})
        [FRAC('1/2')]


        """
        max_len = max([len(lst) for lst in list(converts.keys())])
        indexes = [0 for _ in range(max_len)]
        for i in range(len(self.tokens)):
            if not i < len(self.tokens) - 2:  # ?
                continue

            for j in range(max_len):
                indexes[j] = i + j

            for lst, to in list(converts.items()):
                conditions = []
                for i, condition in enumerate(lst):
                    if isinstance(condition, Type):
                        conditions.append(self.tokens[indexes[i]].type_ is condition)
                    elif isinstance(condition, Token):
                        conditions.append(self.tokens[indexes[i]] == condition)

                if not all(conditions):
                    continue

                value = ""
                for i in range(len(lst)):
                    value += self.tokens[indexes[i]].value

                for _ in range(len(lst)):
                    self.tokens.pop(indexes[0])

                if isinstance(to, Type):
                    self.tokens.insert(
                        indexes[0],
                        Token(
                            to,
                            value,
                        ),
                    )
                elif isinstance(to, Token):
                    self.tokens.insert(indexes[0], to)


print(Token(OPERATOR, "/") is OPERATOR("/"))
code = input(">>> ")

lexer = Lexer(code)
lexer.split()
lexer.lex()
lexer.stop_keywords_in_names((TYPE,))
lexer.combine({(NUM, OPERATOR("/"), NUM): FRAC, (FRAC, OPERATOR("/"), NUM): FRAC})

print(lexer.tokens)


class Parser:
    globals_ = {}

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.pos = 0
        self.current_token = self.lexer.tokens[self.pos]

    def advance(self):
        self.pos += 1
        self.current_token = self.lexer.tokens[self.pos]
        return self.current_token

    def parse(self):
        x = ""
        for token in self.lexer.tokens:
            if token.type_ is NUM or token.type_ is OPERATOR:
                x += token.value

            # self.advance()
        print(x)
        print(eval(x))

        # if token.type_ is TYPE:  # VARIABLE
        #     name = self.advance()
        #     self.advance()
        #     value = self.advance()


parser = Parser(lexer)
parser.parse()
