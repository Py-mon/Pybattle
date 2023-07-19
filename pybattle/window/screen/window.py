import tkinter as tk
from tkinter import Tk
from tkinter.font import Font
from typing import Optional

from pybattle.window.colors import Color, Colors
from pybattle.window.text.grid.matrix import Matrix
from pybattle.window.text.grid.point import Coord, Size

keys_pressing = set()


class Window:
    STARTING_SIZE = Size(520, 700)
    BACKGROUND = Color.from_hex("BACKGROUND", "#2d2833")
    MIN_SIZE = Size(260, 300)
    TITLE = "Pybattle"
    FONT = "Consolas"
    PIXELS_TO_FONT_SIZE: int = 25

    def __init__(
        self,
        text: Matrix,
        background: Color = BACKGROUND,
        starting_size: Size = STARTING_SIZE,
        min_size: Size = MIN_SIZE,
        title: str = TITLE,
        font: str = FONT,
    ):
        self.pixels_to_font_size = type(self).PIXELS_TO_FONT_SIZE

        self.root = Tk()

        self.root.geometry(str(starting_size.width) + "x" + str(starting_size.height))
        self.root.minsize(*min_size)
        self.root.title(title)
        self.root.iconbitmap(
            r"C:\Users\jacob\Downloads\Programming\Python\Pybattle\Github\pybattle\window\screen\good.ico"
        )
        self.root.configure(bg=background.hex)

        self.font = Font(family=font, size=20)

        self.text = tk.Text(
            self.root,
            font=self.font,
            background=background.hex,
            foreground="white",
            border=0,
        )
        self.matrix = text
        self.pos = Coord(5, 5)

        def change(text1: Matrix):
            self.text.delete("1.0", "end")

            last_coord = Coord(0, 0)
            for coord, cell in text1.dct.items():
                if coord.y != last_coord.y:
                    self.text.insert(f"{coord.y + 1}.end", "\n")

                self.text.insert(f"{coord.y + 1}.{coord.x}", cell.value)
                self.text.tag_config(cell.color.name, foreground=cell.color.hex)
                self.text.tag_add(cell.color.name, f"{coord.y + 1}.{coord.x}")

                last_coord = coord

        change(text)

        def disable_text_select(_):
            self.text.tag_remove("sel", "1.0", "end")
            return "break"

        self.text.bind("<Button-1>", disable_text_select)

        def resize_text(window_size: Size):
            new_font_size = round(min(window_size) / self.pixels_to_font_size)

            self.font = Font(family=font, size=new_font_size)
            self.text.config(font=self.font)

        def center_text(window_size: Size):
            # Thanks to chat gpt for getting the text size in pixels
            canvas = tk.Canvas(self.root)
            text_item = canvas.create_text(
                0, 0, text=self.text.get("1.0", "end"), font=self.font
            )
            text_width = canvas.bbox(text_item)[2] - canvas.bbox(text_item)[0]

            line_height = self.font.metrics("linespace")
            line_count = float(self.text.index("end-1c").split(".")[0])
            text_height = int(line_count * line_height)

            text_size = Size(text_height, text_width)

            y, x = window_size.center - text_size.center

            if y + text_height > window_size.y or x + text_width > window_size.x:
                self.pixels_to_font_size += 1
                center_resize()

            self.text.place(x=x, y=y)

        def center_resize(_=None):
            window_size = Size(self.root.winfo_height(), self.root.winfo_width())
            resize_text(window_size)
            center_text(window_size)

        def add(key):
            keys_pressing.add(key.keysym)

        def remove(key):
            keys_pressing.remove(key.keysym)

        def update(_=None):
            self.matrix[self.pos].value = " "

            for key in keys_pressing:
                if key == "a":
                    self.pos = Coord(self.pos.y, self.pos.x - 1)
                elif key == "s":
                    self.pos = Coord(self.pos.y + 1, self.pos.x)
                elif key == "w":
                    self.pos = Coord(self.pos.y - 1, self.pos.x)
                elif key == "d":
                    self.pos = Coord(self.pos.y, self.pos.x + 1)
                print(key)

            self.matrix[self.pos].value = "x"

            self.text.configure(state="normal")

            change(text)

            self.text.configure(state="disabled")

            self.root.after(100, update)

        center_resize()

        self.root.bind("<Configure>", center_resize)
        self.root.bind("<KeyPress>", add)
        update()
        self.root.bind("<KeyRelease>", remove)
        #self.root.bind("<KeyRelease>", update)
        # update(_)

    def run(self):
        self.text.configure(state="disabled")
        self.root.mainloop()


m1 = Matrix.from_str(
    """
HOME____________________________
|  _____  | []             |    |
|  |   |  | []             |____|
|  |   |__| []             |====|
|__|                       |====|
|      X                        |
|                               |
                      () ____   |
|                        [==]   |
|     __              [|      | |
| [= |__| =]          [|  ()  | |
|                     [|      | |
|_______________________________|
"""
)
from pybattle.window.text.grid.range import rect_range

m1.color(Colors.BLUE, rect_range(Coord(5, 12), Coord(1, 1)))

w = Window(m1)
w.run()

# w.place_text(
# w.place_text(
#     Matrix.from_str(
#         """
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|
# """
#     ),
#     Coord(0, 0),
#     True,
# )
# w.place_text(
#     Matrix.from_str("""0"""),
#     Coord(0, 0),
#     True,
# )
# w.place_text(
#     Matrix.from_str("""Hello"""),
#     Coord(5, 5),
#     True,
# )
# w.run()
# w.place_text(
#     Matrix.from_str(
#         """
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
# |                     () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|
# """
#     ),
#     Coord(5, 5),
# )
# w.run()

# x = Matrix.from_str(
#     """HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|"""
# )
# x.color(Colors.RED, rect_range(Coord(5, 20), Coord(2, 5)))


# class Text:
#     def update(self, key):
#         self.x[self.pos].value = " "

#         print(key.keysym)
#         if key.keysym == "a":
#             self.pos.x -= 1
#         elif key.keysym == "s":
#             self.pos.y += 1
#         elif key.keysym == "w":
#             self.pos.y -= 1
#         elif key.keysym == "d":
#             self.pos.x += 1

#         self.x[self.pos].value = "x"

#         self.text.configure(state="normal")

#         self.text.delete("1.0", "end")

#         last_coord = Coord(0, 0)
#         for coord in self.x.coords:
#             cell = self.x[coord]

#             if coord.y != last_coord.y:
#                 self.text.insert(f"{coord.y + 1}.{last_coord.x}", "\n")

#             self.text.insert(f"{coord.y + 1}.{coord.x}", cell.value)
#             self.text.tag_add("center", "1.0", "end")
#             if cell.color == Colors.RED:
#                 self.text.tag_add("red", f"{coord.y + 1}.{coord.x}")

#             last_coord = coord
#         # last_coord = Coord(5, 5)
#         # for coord in [coord for coord in self.x.coords]:
#         #     cell = self.x[coord]

#         #     if coord.y != last_coord.y:
#         #         self.text.insert(f"{coord.y + 6}.{last_coord.x + 5}", "\n")

#         #     self.text.insert(f"{coord.y + 6}.{coord.x + 5}", cell.value)
#         #     self.text.tag_add("center", "1.0", "end")
#         #     if cell.color == Colors.RED:
#         #         self.text.tag_add("red", f"{coord.y + 6}.{coord.x + 5}")

#         #     last_coord = coord

#         self.text.configure(state="disabled")

#     def __init__(self, x: Matrix):
#         self.x = x
#         self.pos = Coord(5, 10)

#         def disable_text_select(event):
#             text.tag_remove("sel", "1.0", "end")
#             return "break"

#         def center(event=None):
#             y, x_ = root.winfo_height(), root.winfo_width()
#             new_font_size = round(
#                 min(x_, y) / 25
#             )  # Adjust the scaling factor as per your preference

#             font1 = font.Font(root, family="Consolas", size=new_font_size)
#             font1.configure(tracking=2)
#             text.config(font=("Consolas", new_font_size))

#             s = Size(y, x_)
#             # 1.71 height to width (width to height 0.583)
#             size = x.size
#             size.y *= round(new_font_size * 1.65)
#             size.x *= round(new_font_size * 0.737)

#             s -= size
#             s = s.center

#             text.place(x=s.x, y=s.y)

#         text = tk.Text(
#             root,
#             font=("Consolas", 20),
#             background="#2A3439",
#             foreground="white",
#             # highlightbackground=root["background"],
#             # highlightcolor=root["background"],
#             # highlightthickness=0,
#             bd=0,  # remove border without changing size
#             # pady=300
#         )
#         text.bind("<Button-1>", disable_text_select)

#         center()

#         text.tag_config("red", foreground="red", justify="center")
#         text.tag_config("center")

#         last_coord = Coord(0, 0)
#         for coord in self.x.coords:
#             cell = self.x[coord]

#             if last_coord == Coord(0, 0):
#                 print(coord)
#             if coord.y != last_coord.y:
#                 text.insert(f"{coord.y + 1}.{last_coord.x}", "\n")

#             text.insert(f"{coord.y + 1}.{coord.x}", cell.value)
#             text.tag_add("center", "1.0", "end")
#             if cell.color == Colors.RED:
#                 text.tag_add("red", f"{coord.y + 1}.{coord.x}")

#             last_coord = coord

#         text.configure(state="disabled")

#         self.text = text

#         root.bind("<Configure>", center)
#         root.bind("<KeyPress>", self.update)


# root = tk.Tk()

# root.geometry("700x520")
# root.minsize(300, 250)
# root.title("Pybattle")
# root.configure(bg="#2A3439")

# Text(x)


# root.mainloop()


# import tkinter as tk
# from tkinter.font import Font


# def resize_font(event):
#     new_font_size = round(
#         int(min(event.width, event.height) / 20) * 0.75
#     )  # Adjust the scaling factor as per your preference
#     label.config(font=("Consolas", new_font_size))


# def key_press(event):
#     print("Key pressed:", event.keysym)


# root = tk.Tk()
# root.geometry("500x600")

# label = tk.Label(
#     root,
#     text="""
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|
# """,
#     font=("Consolas", 10),
# )
# label.pack(fill=tk.BOTH, expand=True)


# root.bind("<Configure>", resize_font)
# root.bind("<KeyRelease>", key_press)

# root.minsize(250, 250)
# root.title("Pybattle")
# root.mainloop()

# root = tk.Tk()

# # 'Consolas, 'Courier New', monospace'

# font = Font(family='Consolas')

# label = tk.Label(root, text="""
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|""", font=font).pack()


# root.mainloop()
