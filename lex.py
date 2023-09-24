from enum import Enum
from typing import Optional, Self

# class TokenType(Enum):
#     PLUS = "+"
#     DASH = "-"
#     STAR = "*"
#     SLASH = "/"
#     CARET = "^"

#     NUMBER = "3.14"

#     IDENTIFIER = "x"

#     RIGHT_PARENTHESIS = "("
#     LEFT_PARENTHESIS = ")"

#     ERROR = "error"


# class TokenType(Enum):
#     OPERATOR = "+-"
#     NUMBER = "3.14"
#     IDENTIFIER = "xy"
#     PARENTHESIS = "()"
#     ERROR = "error"


class NodeType(Enum):
    """What the tokens do"""

    DIVIDE = -3
    SUBTRACT = -2
    NEGATIVE = -1

    NUMBER = 0

    POSITIVE = 1
    ADD = 2
    MULTIPLY = 3
    POWER = 4

    IDENTIFIER = "abc"


class PreType(Enum):
    """What the tokens do"""

    NEGATIVE = -1

    POSITIVE = 1

    ADD_PRIORITY = 5
    REMOVE_PRIORITY = 0


class Node:
    def __init__(
        self, node_type: NodeType, value=None, operand=None, left=None, right=None
    ) -> None:
        self.node_type = node_type
        self.value = value
        self.operand = operand
        self.left = left
        self.right = right


class IdentifiableToken:
    def __init__(
        self,
        string: str,
        node_type: Optional[NodeType] = None,
        priority: Optional[int] = None,
        pre_type: Optional[PreType] = None,
    ) -> None:
        self.string = string
        self.node_type = node_type
        self.pre_type = pre_type
        self.priority = priority


class Token:
    def __init__(
        self, node_type: NodeType, value: str, pre_type: Optional[PreType] = None
    ) -> None:
        self.node_type = node_type
        self.string = value or node_type.value
        self.pre_type = pre_type

    def __repr__(self) -> str:
        return str(self.node_type.name)

    def __eq__(self, __value: Self | IdentifiableToken) -> bool:
        return self.node_type == __value.node_type and self.string == __value.string


class Priority:
    MIN = 0
    TERM = 1
    FACT = 2
    POWER = 3


possible_tokens = [
    IdentifiableToken("**", NodeType.POWER, 3),
    IdentifiableToken("+", NodeType.SUBTRACT, 1, PreType.POSITIVE),
    IdentifiableToken("-", NodeType.SUBTRACT, 1, PreType.NEGATIVE),
    IdentifiableToken("*", NodeType.MULTIPLY, 2),
    IdentifiableToken("/", NodeType.DIVIDE, 2),
    IdentifiableToken("(", pre_type=PreType.ADD_PRIORITY),
    IdentifiableToken(")", pre_type=PreType.REMOVE_PRIORITY),
]


class Lexer:
    def __init__(self, string: str, start: int = 0, current: int = 0) -> None:
        self.string = string
        self.start_i = start
        self.current_i = current
        self.tokens = []

    @property
    def start(self):
        if self.start_i < len(self.string):
            return self.string[self.start_i]
        return None

    @property
    def current(self):
        if self.current_i < len(self.string):
            return self.string[self.current_i]
        return None

    @property
    def span(self):
        return self.string[self.start_i : self.current_i]

    def add_token_type(self, token_type: NodeType):
        token = Token(token_type, self.span)
        self.tokens.append(token)
        self.start_i = self.current_i
        return token

    def number(self):
        while self.current and self.current.isnumeric():
            self.current_i += 1
        if self.current == ".":
            self.current_i += 1
            while self.current and self.current.isnumeric():
                self.current_i += 1
        return self.add_token_type(NodeType.NUMBER)

    def pre_token(self) -> Token:
        return self.tokens[-2]

    def next_token(self):
        while self.start and self.start.isspace():
            self.start_i += 1
        self.current_i = self.start_i

        for token in possible_tokens:
            for length in range(1, len(token.string) + 1):
                if token.string == self.string[self.start_i : self.current_i + length]:
                    self.current_i += length
                    token = Token(token.node_type, token.string, token.pre_type)
                    self.tokens.append(token)
                    self.start_i = self.current_i
                    return token

        if self.current and (self.current.isdigit() or self.current == "."):
            return self.number()

        if self.current and self.current.isalpha():
            while self.current and self.current.isalpha():
                self.current_i += 1
            return self.add_token_type(NodeType.IDENTIFIER)

        raise ValueError()  # called too much (EOF)


def evaluate(node: Node):
    if node.node_type == NodeType.NUMBER:
        return node.value
    elif node.node_type == NodeType.POSITIVE:
        return evaluate(node.operand)
    elif node.node_type == NodeType.NEGATIVE:
        return -evaluate(node.operand)
    elif node.node_type == NodeType.ADD:
        return evaluate(node.left) + evaluate(node.right)
    elif node.node_type == NodeType.SUBTRACT:
        return evaluate(node.left) - evaluate(node.right)
    elif node.node_type == NodeType.MULTIPLY:
        return evaluate(node.left) * evaluate(node.right)
    elif node.node_type == NodeType.DIVIDE:
        return evaluate(node.left) / evaluate(node.right)
    elif node.node_type == NodeType.POWER:
        return evaluate(node.left) ** evaluate(node.right)


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current = self.lexer.next_token()

    def advance(self):
        if lexer.current_i < len(lexer.string):
            self.current = self.lexer.next_token()

    def parse_number(self):
        node = Node(NodeType.NUMBER, float(self.current.string))
        self.advance()
        return node

    def get_priority(self, token: Token):
        for p_token in possible_tokens:
            if p_token == token:
                return p_token.priority or 0
        return 0

    def parse_expression(self, prev=Priority.MIN):
        left = self.parse_terminal_expr()
        current_operator = self.current
        current_priority = self.get_priority(current_operator)
        while current_priority != Priority.MIN:
            if prev >= current_priority:
                break
            else:
                self.advance()
                left = self.parse_infix_expr(current_operator, left)
                current_operator = self.current
                current_priority = self.get_priority(current_operator)
        return left

    def parse_infix_expr(self, operator: Token, left):
        for token in possible_tokens:
            if operator.string == token.string:
                node_type = token.node_type

        return Node(
            node_type,
            left=left,
            right=self.parse_expression(self.get_priority(operator)),
        )

    def parse_terminal_expr(self):
        if self.current.node_type == NodeType.NUMBER:
            node = self.parse_number()
            
        elif self.current.pre_type == PreType.ADD_PRIORITY:
            self.advance()
            node = self.parse_expression()
            if self.current.pre_type == PreType.REMOVE_PRIORITY:
                self.advance()
            else:
                raise ValueError("no end")

        elif self.current.pre_type == PreType.POSITIVE:
            self.advance()
            node = Node(NodeType.POSITIVE, operand=self.parse_terminal_expr())

        elif self.current.pre_type == PreType.NEGATIVE:
            self.advance()
            node = Node(NodeType.NEGATIVE, operand=self.parse_terminal_expr())
        else:
            raise ValueError()

        # implicit mult
        if self.current.pre_type == PreType.ADD_PRIORITY:
            if self.lexer.pre_token().node_type == NodeType.NUMBER:
                return Node(
                    NodeType.MULTIPLY,
                    left=node,
                    right=self.parse_expression(Priority.FACT),
                )

        return node


string = input(">>> ")

lexer = Lexer(string)
parser = Parser(lexer)

nodes = parser.parse_expression()
print(evaluate(nodes))
