from pybattle.types_ import Thickness, Direction, JunctionDict


# [UP][DOWN][LEFT][RIGHT]
table = {
    Thickness.THICK: {
        Thickness.THICK: {
            Thickness.THICK: {
                Thickness.THICK: "╋",
                Thickness.THIN: "╉",
                None: "┫",
            },
            Thickness.THIN: {
                Thickness.THICK: "╊",
                Thickness.THIN: "╂",
                None: "┨",
            },
            None: {Thickness.THICK: "┣", Thickness.THIN: "┠", None: "┃"},
        },
        Thickness.THIN: {
            Thickness.THICK: {
                Thickness.THICK: "╇",
                Thickness.THIN: "╃",
                None: "┩",
            },
            Thickness.THIN: {Thickness.THICK: "╄", Thickness.THIN: "╀", None: "┦"},
            None: {Thickness.THICK: "┡", Thickness.THIN: "┞", None: "╿"},
        },
        None: {
            Thickness.THICK: {Thickness.THICK: "┻", Thickness.THIN: "┹", None: "┛"},
            Thickness.THIN: {Thickness.THICK: "┺", Thickness.THIN: "┸", None: "┚"},
            None: {Thickness.THICK: "┗", Thickness.THIN: "┖", None: "╹"},
        },
    },
    Thickness.THIN: {
        Thickness.THICK: {
            Thickness.THICK: {
                Thickness.THICK: "╈",
                Thickness.THIN: "╅",
                None: "┪",
            },
            Thickness.THIN: {
                Thickness.THICK: "╆",
                Thickness.THIN: "╁",
                None: "┧",
            },
            None: {Thickness.THICK: "┢", Thickness.THIN: "┟", None: "╽"},
        },
        Thickness.THIN: {
            Thickness.THICK: {
                Thickness.THICK: "┿",
                Thickness.THIN: "┽",
                None: "┥",
            },
            Thickness.THIN: {Thickness.THICK: "┾", Thickness.THIN: "┼", None: "┤"},
            None: {
                Thickness.THICK: "┝",
                Thickness.THIN: "├",
                None: "│",
                Thickness.DOUBLE: "╞",
            },
            Thickness.DOUBLE: {
                None: "╡",
                Thickness.DOUBLE: "╪",
            },
        },
        None: {
            Thickness.THICK: {Thickness.THICK: "┷", Thickness.THIN: "┵", None: "┙"},
            Thickness.THIN: {Thickness.THICK: "┶", Thickness.THIN: "┴", None: "╯"},
            None: {
                Thickness.THICK: "┕",
                Thickness.THIN: "╰",
                None: "╵",
                Thickness.DOUBLE: "╘",
            },
            Thickness.DOUBLE: {
                None: "╛",
                Thickness.DOUBLE: "╧",
            },
        },
    },
    None: {
        Thickness.THICK: {
            Thickness.THICK: {
                Thickness.THICK: "┳",
                Thickness.THIN: "┱",
                None: "┓",
            },
            Thickness.THIN: {
                Thickness.THICK: "┮",
                Thickness.THIN: "┰",
                None: "┒",
            },
            None: {Thickness.THICK: "┏", Thickness.THIN: "┎", None: "╻"},
        },
        Thickness.THIN: {
            Thickness.THICK: {
                Thickness.THICK: "┯",
                Thickness.THIN: "┭",
                None: "┑",
            },
            Thickness.THIN: {Thickness.THICK: "┲", Thickness.THIN: "┬", None: "╮"},
            None: {
                Thickness.THICK: "┍",
                Thickness.THIN: "╭",
                None: "╷",
                Thickness.DOUBLE: "╒",
            },
            Thickness.DOUBLE: {
                None: "╕",
                Thickness.DOUBLE: "╤",
            },
        },
        None: {
            Thickness.THICK: {Thickness.THICK: "━", Thickness.THIN: "╾", None: "╸"},
            Thickness.THIN: {Thickness.THICK: "╼", Thickness.THIN: "─", None: "╴"},
            None: {
                Thickness.THICK: "╺",
                Thickness.THIN: "╶",
            },
            Thickness.DOUBLE: {Thickness.DOUBLE: "═"},
        },
        Thickness.DOUBLE: {
            Thickness.THIN: {
                Thickness.THIN: "╥",
                None: "╖",
            },
            None: {
                Thickness.THIN: "╓",
                Thickness.DOUBLE: "╔",
            },
            Thickness.DOUBLE: {
                None: "╗",
                Thickness.DOUBLE: "╦",
            },
        },
    },
    Thickness.DOUBLE: {
        None: {
            Thickness.THIN: {
                Thickness.THIN: "╨",
                None: "╜",
            },
            None: {
                Thickness.THIN: "╙",
                Thickness.DOUBLE: "╚",
            },
            Thickness.DOUBLE: {None: "╝", Thickness.DOUBLE: "╩"},
        },
        Thickness.DOUBLE: {
            Thickness.THIN: {
                Thickness.THIN: "╫",
                None: "╢",
            },
            None: {
                Thickness.THIN: "╟",
                None: "║",
                Thickness.DOUBLE: "╠",
            },
            Thickness.DOUBLE: {
                None: "╣",
                Thickness.DOUBLE: "╬",
            },
        },
    },
}


def get_junction(dct: JunctionDict):
    return table[dct.get(Direction.UP)][dct.get(Direction.DOWN)][
        dct.get(Direction.LEFT)
    ][dct.get(Direction.RIGHT)]
