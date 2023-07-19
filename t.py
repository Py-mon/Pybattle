import tkinter as tk


class Text:
    def __init__(self, x):
        self.x = x

        def disable_text_select(event):
            text.tag_remove("sel", "1.0", "end")
            return "break"

        def center(event):
            y, x_ = root.winfo_height(), root.winfo_width()

            new_font_size = round(min(x_ * 1.02, y * 1.2) / 20)  # Adjust the scaling factor as per your preference
            text.config(font=("Consolas", new_font_size))

            # Calculate the new center position
            text_width = text.winfo_width()
            text_height = text.winfo_height()
            new_x = (x_ - text_width) // 2
            new_y = (y - text_height) // 2
            text.place(x=new_x, y=new_y)

        root = tk.Tk()
        root.geometry("700x520")
        root.minsize(300, 300)
        root.title("Pybattle")
        root.configure(bg="#2A3439")

        text = tk.Text(
            root,
            font=("Consolas", 20),
            background="#2A3439",
            foreground="white",
            bd=0,
        )
        text.bind("<Button-1>", disable_text_select)
        text.grid(row=0, column=0)
        center(None)

        text.tag_config("red", foreground="red", justify="center")
        text.tag_config("center")

        last_coord = None
        for coord in self.x.coords:
            cell = self.x[coord]

            if last_coord is None:
                print(coord)
            if coord.y != last_coord.y:
                text.insert(f"{coord.y + 1}.{last_coord.x}", "\n")

            text.insert(f"{coord.y + 1}.{coord.x}", cell.value)
            text.tag_add("center", "1.0", "end")
            if cell.color == Colors.RED:
                text.tag_add("red", f"{coord.y + 1}.{coord.x}")

            last_coord = coord

        text.configure(state="disabled")

        root.bind("<Configure>", center)
        root.mainloop()


Text(x)