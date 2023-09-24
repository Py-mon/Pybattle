import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

# 20 -> 1/5
# 30 -> 3/5
# 40 -> 4/10
# 50 -> 1/2
from pybattle.creatures.rand import Curve

# from pybattle.creatures.rand import solve_beta_parameters

# a = 7
# b = 7

# min_ = 50
# max_ = 0

# m = (a - 1) / (a + b - 2) * (max_ - min_) + min_
# print(m)
# y = solve_beta_parameters(20, 0, 50)
# print(y)


# # Known values
# Mean = 40  # Replace with your desired mean
# min_ = 0
# max_ = 50

# b2 = 7
# a2 = (-(Mean * b2) + (min_ * b2) + 2 * Mean - min_ - max_) / (Mean - max_)

# # x-0, x-0 -> x-0.0
# # x+1, x-0 -> x-0.5
# # x-1, x-0 -> x-0.5

# print(a2)
# # /4 as bigger

# b = b2 - (abs(b2 - a2) / ((abs(b2 - a2) / (b2 / 1.5)) + 1))
# print(b)
# a = (-(Mean * b) + (min_ * b) + 2 * Mean - min_ - max_) / (Mean - max_)

# print(f"a = {a}, b = {b}")

# m = (a - 1) / (a + b - 2) * (max_ - min_) + min_
# print(m)


# a = 7
# b = 7

# a = 7
# b = 7

# min_ = 40 / 2
# max_ = 50

# 30 -> 7, 10
# 25 -> 7, 7
# 20 -> 10, 7


x = Curve.from_mean(10, Curve.even(0, 50, 7))
min_ = x.low
max_ = x.high


num_sections = 9

data = x.num

hist, bins = np.histogram(data, bins=50, density=True)
bin_centers = (bins[:-1] + bins[1:]) / 2

params = beta.fit(data)
line = beta.pdf(bin_centers, *params)

line_min = min(bin_centers)
line_max = max(bin_centers)

section_boundaries = np.linspace(line_min, line_max, num_sections + 1)

plt.plot(bin_centers, line, "r-", lw=2, label="Fitted PDF")

plt.xlabel("Value")
plt.ylabel("Density")


# Function to extend an array
def extend_array(arr, by=10):
    extended_arr = np.empty(0)
    for i in range(len(arr) - 1):
        current_item, next_item = arr[i], arr[i + 1]
        max_value, min_value = max(current_item, next_item), min(
            current_item, next_item
        )
        interpolated_values = np.linspace(min_value, max_value, by)[:-1]
        if next_item < current_item:
            interpolated_values = interpolated_values[::-1]  # Reverse order
        extended_arr = np.concatenate((extended_arr, interpolated_values))
    return extended_arr


extended_bounds = extend_array(bin_centers, 10)
extended_line = extend_array(line, 10)

# Display the section boundaries and their relative frequencies as percentages
for i, boundary in enumerate(section_boundaries[:-1]):
    next_boundary = section_boundaries[i + 1]
    section_data = data[(data >= boundary) & (data < next_boundary)]
    percentage = len(section_data) / len(data) * 100
    section_midpoint = (boundary + next_boundary) / 2
    lowest_adjacent_boundary = (
        boundary if next_boundary < np.mean(bin_centers) else next_boundary
    )
    bin_index = np.digitize(lowest_adjacent_boundary, bins) - 1
    boundary_height = hist[bin_index]  # Subtract 1 because bin_index is 1-based

    plt.annotate(
        f"{percentage:.2f}%",
        xy=(section_midpoint, boundary_height / 3),
        ha="center",
        fontsize=10,
        rotation=-(num_sections * (2 / 3) * 10),
    )

    absolute_differences = np.abs(extend_array(bin_centers - boundary))
    closest_index = np.argmin(absolute_differences)
    boundary_height = extend_array(line)[closest_index]

    plt.plot(
        [boundary, boundary], [0, boundary_height], color="k", linestyle="--", lw=0.5
    )

    condition = (extended_bounds > (boundary * 0.999)) & (
        extended_bounds < (next_boundary * 1.001)
    )
    section_x = extended_bounds[condition]
    section_y = extended_line[condition]
    plt.fill_between(section_x, section_y, alpha=0.2, label=f"Section {i + 1}")

# Create a line plot
plt.xticks(np.linspace(min_, max_, 10))
plt.show()
