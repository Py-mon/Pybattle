from src.window.screen import AnsiEscapeCode
from src.window.coord import Coord
from src.window.matrix import Matrix


def str_with_text(str_: str, *codes) -> str:
    # TODO: Make codes[0] not a int instead a coord 
    # TODO: Don't make codes collide. Adding the escape code all at one time instead of each char being added separately might fix this
    
    
    matrix = Matrix(str_)
    
    for i in range(1, len(codes)):
        for j in range(0, i):
            codes[i][0] -= len(codes[j][1])
                
    offset = 0
    for (pos, escape_code) in codes:
        # Convert escape code to insertable format (Meaning you can only insert separated symbols)
        escape_code = list(escape_code)
        pos += offset
        for char in escape_code:
            matrix.insert(pos, char)
            # Increasing the pos to insert sequentially
            pos += 1
            offset += 1
    print(matrix._matrix)
    return str(matrix)
