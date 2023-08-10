# Our Coding Style Guidelines

Note: You do not have to follow these guidelines and they are only if you want to fit with the style of this code.

If you notice any of the code not following these guides, feel free to submit a pull request.

## Type Hinting

- Type hint all functions parameters (except cls and self), and the return type:
```py
def foo(x: int) -> int:
```

- Only type hint variables went the code editor doesnt know what type it is. But when it's obvious you don't have to do this:
```py
x: int = 5
```

## Docstrings

- All of the docstring should be imperative.
For example instead of `Adds one to x` use `Add one to x`

- Usually don't add docstrings to dunder methods.

- Feel free to use the markdown formatting.

### Single Line Docstrings
They don't have a period at the end.
```py
def foo(x: int) -> int:
  """Add one to x"""
  return x + 1
```

### Multiple Line Docstrings
Multiple line docstrings should not have text on the first and last line and should use periods on full sentences.
Start with a summary and then go into the detail.

```py
"""
Level out the rows of the matrix.

Adjust the number of cells in each row of the matrix to be the same by adding blank Cells, according to the alignment
specified during initialization.
"""
```

## Other Things

- Instead of using None to represent the default use the ellipsis `...`:
```py
class Foo:
  def __init__(self, x: int) -> None:
     self.x = x
     
  def bar(self, x: int = ...) -> int:
    if x is not ...:
      self.x = x
 
    return x + 1
```


