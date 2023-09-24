from pybattle.types_ import Direction, JunctionDict, Thickness

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


def get_junction(dct: JunctionDict) -> str:
    """Get a str junction from a dict of Directions and Thicknesses."""
    return table[dct.get(Direction.UP)][dct.get(Direction.DOWN)][
        dct.get(Direction.LEFT)
    ][dct.get(Direction.RIGHT)]
