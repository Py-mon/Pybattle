from typing import Literal

# UP DOWN LEFT RIGHT
table = {
    'thick': {
        'thick': {
            'thick': {
                'thick': '╋',
                'thin': '╉',
                'none': '┫',
            },
            'thin': {
                'thick': '╊',
                'thin': '╂',
                'none': '┨',
            },
            'none': {
                'thick': '┣',
                'thin': '┠',
                'none': '┃'  # May exclude
            },
        },
        'thin': {
            'thick': {
                'thick': '╇',
                'thin': '╃',
                'none': '┩',
            },
            'thin': {
                'thick': '╄',
                'thin': '╀',
                'none': '┦'
            },
            'none': {
                'thick': '┡',
                'thin': '┞',
                'none': '╿'  # May exclude
            },
        },
        'none': {
            'thick': {
                'thick': '┻',
                'thin': '┹',
                'none': '┛'  # May exclude
            },
            'thin': {
                'thick': '┺',
                'thin': '┸',
                'none': '┚'  # May exclude
            },
            'none': {
                'thick': '┗',  # May exclude
                'thin': '┖',  # May exclude
                'none': '╹'  # May exclude
            },

        },

    },
    'thin': {
        'thick': {
            'thick': {
                'thick': '╈',
                'thin': '╅',
                'none': '┪',
            },
            'thin': {
                'thick': '╆',
                'thin': '╁',
                'none': '┧',
            },
            'none': {
                'thick': '┢',
                'thin': '┟',
                'none': '╽'  # May exclude
            },
        },
        'thin': {
            'thick': {
                'thick': '┿',
                'thin': '┽',
                'none': '┥',
            },
            'thin': {
                'thick': '┾',
                'thin': '┼',
                'none': '┤'
            },
            'none': {
                'thick': '┝',
                'thin': '├',
                'none': '│',  # May exclude
                'double': '╞',
            },
            'double': {
                'none': '╡',
                'double': '╪',
            },
        },
        'none': {
            'thick': {
                'thick': '┷',
                'thin': '┵',
                'none': '┙'  # May exclude
            },
            'thin': {
                'thick': '┶',
                'thin': '┴',
                'none': '╯'  # May exclude
            },
            'none': {
                'thick': '┕',  # May exclude
                'thin': '╰',  # May exclude
                'none': '╵',  # May exclude
                'double': '╘',  # May exclude
            },
            'double': {
                'none': '╛',  # May exclude
                'double': '╧',  # May exclude

            }

        },

    },

    'none': {
        'thick': {
            'thick': {
                'thick': '┳',
                'thin': '┱',
                'none': '┓',  # May exclude
            },
            'thin': {
                'thick': '┮',
                'thin': '┰',
                'none': '┒',  # May exclude
            },
            'none': {
                'thick': '┏',  # May exclude
                'thin': '┎',  # May exclude
                'none': '╻'  # May exclude
            },
        },

        'thin': {
            'thick': {
                'thick': '┯',
                'thin': '┭',
                'none': '┑',  # May exclude
            },
            'thin': {
                'thick': '┲',
                'thin': '┬',
                'none': '╮'  # May exclude
            },
            'none': {
                'thick': '┍',  # May exclude
                'thin': '╭',  # May exclude
                'none': '╷',  # May exclude
                'double': '╒',  # May exclude
            },
            'double': {
                'none': '╕',  # May exclude
                'double': '╤',
            },
        },
        'none': {
            'thick': {
                'thick': '━',  # May exclude
                'thin': '╾',  # May exclude
                'none': '╸'  # May exclude
            },
            'thin': {
                'thick': '╼',  # May exclude
                'thin': '─',  # May exclude
                'none': '╴'  # May exclude
            },
            'none': {
                'thick': '╺',  # May exclude
                'thin': '╶',  # May exclude
            },
            'double': {
                'double': '═'
            }

        },
        'double': {
            'thin': {
                'thin': '╥',
                'none': '╖',
            },
            'none': {
                'thin': '╓',
                'double': '╔',
            },
            'double': {
                'none': '╗',
                'double': '╦',
            }
        },

    },
    'double': {
        'none': {
            'thin': {
                'thin': '╨',
                'none': '╜',  # May exclude
            },
            'none': {
                'thin': '╙',  # May exclude
                'double': '╚',  # May exclude
            },
            'double': {
                'none': '╝',  # May exclude
                'double': '╩'  # May exclude
            }

        },

        'double': {
            'thin': {
                'thin': '╫',
                        'none': '╢',
            },
            'none': {
                'thin': '╟',
                'none': '║',
                'double': '╠',
            },
            'double': {
                'none': '╣',
                'double': '╬',
            }
        },
    },
}

Direction = Literal['up', 'down', 'left', 'right']
Thickness = Literal['thin', 'thick', 'double']
Conjunction = dict[Direction, Thickness]


def get_conjunction(dct: Conjunction):
    right = dct.get('right', 'none')
    left = dct.get('left', 'none')
    up = dct.get('up', 'none')
    down = dct.get('down', 'none')
    return table[up][down][left][right]


chars = '''
─	━	│	┃	┄	┅	┆	┇	┈	┉	┊	┋	┌	┍	┎	┏

┐	┑	┒	┓	└	┕	┖	┗	┘	┙	┚	┛	├	┝	┞	┟

┠	┡	┢	┣	┤	┥	┦	┧	┨	┩	┪	┫	┬	┭	┮	┯

┰	┱	┲	┳	┴	┵	┶	┷	┸	┹	┺	┻	┼	┽	┾	┿

╀	╁	╂	╃	╄	╅	╆	╇	╈	╉	╊	╋	╌	╍	╎	╏

═	║	╒	╓	╔	╕	╖	╗	╘	╙	╚	╛	╜	╝	╞	╟

╠	╡	╢	╣	╤	╥	╦	╧	╨	╩	╪	╫	╬	╭	╮	╯

╰	╱	╲	╳	╴	╵	╶	╷	╸	╹	╺	╻	╼	╽	╾	╿
'''

all_values = list(chars.replace('\t', '').replace('\n', ''))

values = []


def check_table(table: dict) -> None:
    for value in table.values():
        if isinstance(value, dict):
            check_table(value)
        elif value in values:
            raise ValueError(value)
        else:
            values.append(value)


check_table(table)


def print_missing_values() -> None:
    for value in all_values:
        if value not in values:
            print(value)
