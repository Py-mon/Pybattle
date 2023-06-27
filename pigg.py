structure = {
    "plank": ({}, ["wrench"]),
    "red_key_card": ({}, ["wrench", 'plank', "blue_key_card"]),
    "wrench": ({}, ["yellow_key"]),
    "hammer": ({}, ["green_key"]),
    "blue_key_card": (
        {
            "green_key_card": ({"yellow_key": ({}, ["fire"])}, ["wrench"]),
            "dynamite": ({}, ["green_key_card"]),
            "blue_key": ({}, ["dynamite"]),
            "hammer": ({}, ["plank"]),
            "fire": (
                {
                    "orange_key_card": ({}, ["hammer"]),
                    "green_key": ({}, ["orange_key_card"]),
                    "wrench": ({}, ["hammer", 'red_key']),
                    "red_key": ({"plank": ({}, ["white_key"])}, ["orange_key_card"]),
                },
                ["orange_key_card"],
            ),
        },
        ["blue_key"],
    ),
}
unlocked = ["red_key_card", "blue_key_card"]















# for key, value in structure.items():
#     if isinstance(key, str) and key != '__unlocked__':
#         structure['__unlocked__'] = value
#     else:
#         for key, value in value.items():
#             if isinstance(key, str) and key != '__unlocked__':
#                 structure[] = value


def put(struct, upper_key=None):
    for key, value in struct.copy().items():
        if upper_key is None:
            unlocked.append(key)

        elif isinstance(key, str):
            struct[upper_key] = key

        if isinstance(value, dict):
            put(value, key)


put(structure)
print(unlocked)
print(structure)
