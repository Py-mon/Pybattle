from pynput.keyboard import KeyCode, Listener


class Keyboard:
    pressed_keys = set()

    @classmethod
    def on_press(cls, key):
        if isinstance(key, KeyCode):
            key = key.char
        cls.pressed_keys.add(key)

    @classmethod
    def on_release(cls, key):
        if isinstance(key, KeyCode):
            key = key.char
        cls.pressed_keys.remove(key)


key_listener = Listener(on_press=Keyboard.on_press, on_release=Keyboard.on_release)
