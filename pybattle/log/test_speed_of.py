import argparse
import cProfile

import pandas

with open("pybattle/log/log.py") as file:
    code = file.read()

cProfile.run(code, "restats")


# parser = argparse.ArgumentParser()

# parser.add_argument("file", type=str)
# args = parser.parse_args()

# with open(args.file) as file:
#     code = file.read()

# # cProfile.run(code, "logs/time.log", "tottime")
# profile = cProfile.Profile().run(code)
# # profile.dump_stats('logs/time.log')
# # profile.print_stats()
# profile.snapshot_stats()

# with open("logs/time.log", "w") as file:
#     # print(pandas.array(profile.stats))
#     print(pandas.DataFrame(profile.stats))

#     dct = {'calls': [], ''}

#     for key, value in profile.stats.items():
#         print(key, value)
#     file.write(str(pandas.DataFrame(profile.stats)))

# {'col1': [1, 2], 'col2': [3, 4]}

# {'}

# ('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\_distutils_hack\\__init__.py', 96, '<lambda>') (4, 4, 5.000000000000001e-07, 5.000000000000001e-07,

# ('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\re\\_compiler.py', 571, '_code')
# (6, 6, 5.14e-05, 0.0013941000000000001, {('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\re\\_compiler.py', 738, 'compile'): (6, 6, 5.14e-05, 0.0013941000000000001)})

# {('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\_distutils_hack\\__init__.py', 89, 'find_spec'): (4, 4, 5.000000000000001e-07, 5.000000000000001e-07)})

# {('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\toml\\decoder.py', 113, 'load'): (1, 1, 3.72e-05, 0.00047640000000000003, {('<string>', 1, '<module>'): (1, 1, 3.72e-05, 0.00047640000000000003)}),

#  ('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\logging\\__init__.py', 1, '<module>'): (1, 1, 6.170000000000001e-05, 0.0032293, {('~', 0, '<built-in method builtins.exec>'): (1, 1, 6.170000000000001e-05, 0.0032293)}),

#  ('<string>', 1, '<module>'): (1, 1, 3.0000000000000004e-07, 3.0000000000000004e-07, {('~', 0, '<built-in method builtins.eval>'): (1, 1, 3.0000000000000004e-07, 3.0000000000000004e-07)}), ('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\logging\\__init__.py', 1157, '__init__'): (1, 1, 9.100000000000001e-06, 0.00015800000000000002, {('<string>', 113, '_create_logger'): (1, 1, 9.100000000000001e-06, 0.00015800000000000002)}), ('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\toml\\decoder.py', 684, '_get_split_on_quotes'): (10, 10, 1.36e-05, 1.84e-05, {('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\toml\\decoder.py', 165, 'loads'): (3, 3, 4.4e-06, 5.4e-06), ('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\toml\\decoder.py', 706, 'load_line'): (7, 7, 9.2e-06, 1.3000000000000001e-05)}), ('C:\\Users\\jacob\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\toml\\decoder.py', 90, '_stri
