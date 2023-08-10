import tkinter as tk
from collections.abc import Iterable
from enum import Enum
from math import ceil
from tkinter import Tk
from tkinter.font import Font
from typing import Optional, Self

from pybattle.screen.colors import Color, Colors
from pybattle.screen.grid.matrix import Matrix
from pybattle.screen.grid.point import Coord, Size

keys_pressing = set()


SPEED = 1


class Event:
    fps = 60

    _events: list[Self] = []

    def __init__(self, func, every, *args, time_affected: bool = True):
        """Minimum sleep 0.03 with 30 fps"""
        if time_affected:
            every /= SPEED

        self.every_frames = ceil(type(self).fps * every)
        self.func = func
        self.args = args

        type(self)._events.append(self)


class EventExit(Enum):
    BREAK_QUEUE = 2
    BREAK = 1
    QUIT = 0


class EventQueue:
    def __init__(self, *events: list[Event]):
        self.events = list(events)
        self._i = 0
        self.current_events = self.events[self._i]
        self.last_results = {}
        self.new_results = {}

    def next(self):
        self._i += 1
        if self._i >= len(self.events):
            return "end"
        self.current_events = self.events[self._i]
        self.last_results = self.new_results
        self.new_results = {}

    def add(self, events: list[Event]):
        self.events.append(events)


class Window:
    STARTING_SIZE = Size(520, 700)
    BACKGROUND = Color.from_hex("BACKGROUND", "#2c2c34")
    MIN_SIZE = Size(260, 300)
    TITLE = "Pybattle"
    FONT = "Consolas"
    PIXELS_TO_FONT_SIZE: int = 25

    def change(self, text: Matrix):
        Colors.init_color_tags(self.text)

        self.text.delete("1.0", "end")

        for row in text.dct_rows:
            for coord, cell in row.items():
                self.text.insert(f"{coord.y + 1}.{coord.x}", cell.value)
                self.text.tag_add(cell.color.name, f"{coord.y + 1}.{coord.x}")

            self.text.insert(f"999.end", "\n")

    def disable_selection(self) -> None:
        def disable_selection(_):
            self.text.tag_remove("sel", "1.0", "end")
            return "break"

        self.text.bind("<Button-1>", disable_selection)

    def resize_text(self, window_size: Size):
        new_font_size = max(
            min(round(min(window_size) / self.pixels_to_font_size), 50), 10
        )

        self.font.config(size=new_font_size)
        self.text.config(font=self.font)

    def text_size(self):
        text_width = self.font.measure(" ") * self.matrix.size.x

        line_height = self.font.metrics("linespace")
        line_count = float(self.text.index("end-1c").split(".")[0]) - 1
        text_height = int(line_count * line_height)

        text_size = Size(text_height, text_width)

        return text_size

    def center_text(self, window_size: Size):
        text_size = self.text_size()

        y, x = window_size.center - text_size.center

        self.text.place(x=x, y=y)

    def center_resize(self, _=None):
        window_size = Size(self.root.winfo_height(), self.root.winfo_width())

        self.resize_text(window_size)
        self.center_text(window_size)

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

        self.event_queue: EventQueue

        self.root = Tk()

        self.root.geometry(str(starting_size.width) + "x" + str(starting_size.height))
        self.root.minsize(*min_size)
        self.root.title(title)

        self.root.configure(bg=background.hex)

        self.font = Font(family=font)

        self.text = tk.Text(
            self.root,
            font=self.font,
            background=background.hex,
            foreground="white",
            border=0,
        )
        self.matrix = text

        self.disable_selection()

        Colors.init_color_tags(self.text)

        self.change(text)

        def events(frame_count):
            if not self.event_queue.current_events:
                if self.event_queue.next() == "end":
                    self.root.destroy()

            for event in self.event_queue.current_events:
                if frame_count % event.every_frames != 0:
                    continue

                if self.event_queue.last_results:
                    result = event.func(self.event_queue.last_results, *event.args)
                else:
                    result = event.func(*event.args)

                if result is not None:
                    break_ = False
                    if isinstance(result, tuple):
                        if EventExit.BREAK_QUEUE == result[0]:
                            break_ = True
                            result = result[1]
                    elif result == EventExit.BREAK_QUEUE:
                        break_ = True
                    elif result == EventExit.QUIT:
                        self.root.destroy()

                    self.event_queue.current_events.remove(event)
                    self.event_queue.new_results[event.func.__name__] = result

                    if break_:
                        self.event_queue.current_events = []
                        break

            self.root.after(1000 // Event.fps, events, frame_count + 1)

        self.root.after(10, events, 0)

        self.root.bind("<KeyPress>", lambda key: keys_pressing.add(key.keysym))
        self.root.bind("<KeyRelease>", lambda key: keys_pressing.remove(key.keysym))

        def zoom(event):
            if not (self.pixels_to_font_size - event.delta // 30) <= 0:
                if not ((self.pixels_to_font_size > 50) and event.delta < 0):
                    self.pixels_to_font_size -= event.delta // 30
                    print(self.pixels_to_font_size)
                    self.center_resize()

        self.root.bind("<MouseWheel>", zoom)

        self.root.bind("<Configure>", self.center_resize)

    def run(self, event_queue: EventQueue):
        self.event_queue = event_queue
        self.root.mainloop()

    def extend_event_queue(self, events: list[Event]):
        self.event_queue.add(events)

    def extend_current_events(self, event: Event, time_after=0):
        self.one_time_event(
            lambda: self.event_queue.current_events.append(event), time_after
        )

    def one_time_event(self, func, time_after):
        self.root.after(time_after * 1000, func)


# f = Frame.from_str(
#     """
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |               ))              |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|"""
# )

# pos = Coord(5, 5)

# w = Window(f)


# def update():
#     global pos
#     f[pos, "value"] = " "

#     for key in keys_pressing:
#         if key == "a":
#             pos = Coord(pos.y, pos.x - 1)
#         elif key == "s":
#             pos = Coord(pos.y + 1, pos.x)
#         elif key == "w":
#             pos = Coord(pos.y - 1, pos.x)
#         elif key == "d":
#             pos = Coord(pos.y, pos.x + 1)
#         print(key)

#     f[pos, "value"] = "♀"

#     w.change(f)


# Event(update, 0.05)

# w.run()


# import tkinter as tk

# # def center_text(text, offset=(0, 0)):
# #     window_size = Size(root.winfo_height(), root.winfo_width())

# #     # Get the text size
# #     text_width = canvas.bbox(text)[2] - canvas.bbox(text)[0] + offset[0]
# #     text_height = canvas.bbox(text)[3] - canvas.bbox(text)[1] + offset[1]

# #     text_size = Size(text_height, text_width)

# #     # Switch for some reason
# #     y, x = (window_size - text_size).center

# #     y -= canvas.bbox(text)[1]
# #     x -= canvas.bbox(text)[0]

# #     # Move the text to the center
# #     # canvas.create_oval(x - 10, y - 10, x + 10, y + 10)
# #     # canvas.create_line(0, 0, window_size.x, window_size.y)
# #     canvas.move(text, x + offset[0], y + offset[1])


# def center_text(dct):
#     # Get the bounding box that covers all the text elements

#     # Move all the text elements to the center of the canvas
#     for text, offset in dct.items():
#         canvas.move(
#             text,
#             canvas_center_x - center_x + offset[0],
#             canvas_center_y - center_y + offset[1],
#         )


# root = tk.Tk()
# root.geometry("700x300")
# canvas = tk.Canvas(root, width=700, height=300)
# canvas.pack(expand=True)


# canvas_center_x = None
# canvas_center_y = None
# center_x = None
# center_y = None


# def do():
#     global canvas_center_x, canvas_center_y, center_x, center_y
#     bbox_all = canvas.bbox(tk.ALL)

#     # Calculate the center coordinates of the bounding box
#     center_x = (bbox_all[2] + bbox_all[0]) / 2
#     center_y = (bbox_all[3] + bbox_all[1]) / 2

#     # Get the center of the canvas
#     window_size = Size(root.winfo_height(), root.winfo_width())
#     canvas_center_x = window_size.width / 2
#     canvas_center_y = window_size.height / 2


# width = Font(root, ("Consolas", 12)).measure("\n")
# linespace = Font(root, ("Consolas", 12)).metrics()["linespace"]

# m = Matrix.from_str("hello\nthere")

# texts = {}
# for coord, cell in m.dct.items():
#     texts[
#         (
#             canvas.create_text(
#                 *(Coord(0, 0) + (coord * (linespace // 2, width // 2))).reversed,
#                 text=cell.value,
#                 fill="blue",
#                 font=("Consolas", 12),
#             )
#         )
#     ] = (Coord(0, 0) + (coord * (linespace // 2, width // 2))).reversed


# def y():
#     canvas.create_rectangle(
#         *(
#             canvas.bbox("all")[0],
#             canvas.bbox("all")[1],
#             canvas.bbox("all")[2],
#             canvas.bbox("all")[3],
#         )
#     )


# font = 24


# def x1(event):
#     global font
#     new_font_size = font + event.delta // 50
#     for text in texts:
#         canvas.itemconfig(text, font=("Consolas", new_font_size))
#     font = new_font_size
#     do()
#     center_text(texts)


# root.bind("<MouseWheel>", x1)


# # def x2(event):
# #     window_size = Size(root.winfo_height(), root.winfo_width())
# #     canvas.config(height=window_size.y, width=window_size.x)
# #     center_text(texts)


# # root.bind("<Configure>", x2)

# canvas.after(100, y)
# canvas.after(50, center_text, texts)
# canvas.after(10, do)

# root.mainloop()

# text = canvas.create_text(50, 50, text="h", fill="blue", font=("Consolas", 24))
# text2 = canvas.create_text(
#     50 + 18, 50, text="i", fill="blue", font=("Consolas", 24)
# )
# text2 = canvas.create_text(
#     50, 50 + 24, text="Y", fill="blue", font=("Consolas", 24)
# )
# text2 = canvas.create_text(
#     50 + 18, 50 + 24, text="O", fill="blue", font=("Consolas", 24)
# )

# text2 = canvas.create_text(52, 52, text="T", fill="blue", font=("Consolas", 12))


# https://www.desmos.com/calculator/clv5rmph8u


# root.mainloop()

# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# text = canvas.create_text(0, 0, text="Hello, centered text!", fill="blue")
# center_text(canvas, text)

# root.mainloop()

# root = Tk()


# def center_text(canvas, text):
#     # Get the canvas size
#     canvas_width = canvas.winfo_width()
#     canvas_height = canvas.winfo_height()

#     # Get the text size
#     text_width = canvas.bbox(text)[2] - canvas.bbox(text)[0]
#     text_height = canvas.bbox(text)[3] - canvas.bbox(text)[1]

#     # Calculate the center coordinates
#     center_x = (canvas_width - text_width) / 2
#     center_y = (canvas_height - text_height) / 2

#     # Move the text to the center
#     canvas.move(text, center_x, center_y)


# canvas = tk.Canvas(root, width=400, height=300)
# text = canvas.create_text(
#     100, 100, text="hello\nworld", justify="center", fill="blue", font=("consolas", 24)
# )
# canvas.pack()
# center_text(canvas, text)


# root.mainloop()


# f = Frame.box(Size(15, 40))
# map_ = Frame.map(
#     """
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |               ))              |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|
# """
# )
# from time import time

# f.add_frame(map_)

# w = Window(f.matrix)
# pos = Coord(5, 5)
# f.update()


# def update():
#     start_time = time()

#     global pos
#     map_.matrix[pos]._value = " "

#     for key in keys_pressing:
#         if key == "a":
#             pos = Coord(pos.y, pos.x - 1)
#         elif key == "s":
#             pos = Coord(pos.y + 1, pos.x)
#         elif key == "w":
#             pos = Coord(pos.y - 1, pos.x)
#         elif key == "d":
#             pos = Coord(pos.y, pos.x + 1)
#         print(key)

#     map_.matrix[pos]._value = "♀"

#     f.update()

#     w.change(f.matrix)

#     print(time() - start_time)


# Event(update, 0.05)
# w.run()


# matrix = Matrix.from_str(
#     """
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |               ))              |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|
# """
# )
# w = Window(matrix)
# pos = Coord(5, 5)


# def update():
#     global pos
#     matrix[pos].value = " "

#     for key in keys_pressing:
#         if key == "a":
#             pos = Coord(pos.y, pos.x - 1)
#         elif key == "s":
#             pos = Coord(pos.y + 1, pos.x)
#         elif key == "w":
#             pos = Coord(pos.y - 1, pos.x)
#         elif key == "d":
#             pos = Coord(pos.y, pos.x + 1)
#         print(key)

#     matrix[pos].value = "♀"

#     w.change(matrix)


# Event.queue.append(Event(update, 0.05))

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


# pybattle.window.window
