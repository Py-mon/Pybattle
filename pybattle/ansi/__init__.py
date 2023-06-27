"""
ANSI escape sequences are a standard terminals to control cursor location, color, font styling, and other options.

All ANSI escape sequences have a prefix escape (ESC). (Not case sensitive)
- Octal: `\\033`
- Unicode: `\\u001b`
- Hexadecimal: `\\x1b`

Most sequences start with CSI (Control Sequence Introducer)
- `ESC[`

For example to make the color red: ESC[31m (\\033[31m) (Any ESC will work)

Learn more at https://en.wikipedia.org/wiki/ANSI_escape_code.
"""