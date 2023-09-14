import math

# 计算深度，输入距离中心点距离，输出深度
# 定义常量
METERS_IN_ONE_NAUTICAL_MILE = 1852
LENGTH = 2 * METERS_IN_ONE_NAUTICAL_MILE
WIDTH = 4 * METERS_IN_ONE_NAUTICAL_MILE
CENTER_DEPTH = 110  # m
SLOPE = math.radians(1.5)  # convert degree to radian


def calculate_depth(x, y):
    """
    Calculate the depth at a given position (x, y).

    Args:
    - x (float): x-coordinate from the western boundary
    - y (float): y-coordinate from the northern boundary

    Returns:
    - float: depth at the given position
    """
    horizontal_distance_from_center = x - WIDTH / 2
    depth_change = math.tan(SLOPE) * horizontal_distance_from_center
    return CENTER_DEPTH + depth_change


# 测试
# x, y =WIDTH ,LENGTH # 西边最深
x, y =0,0 # 东边最浅

print("位置的深度",calculate_depth(x, y))  # 应该输出110

import math

# 定义常量
METERS_IN_ONE_NAUTICAL_MILE = 1852
LENGTH = 2 * METERS_IN_ONE_NAUTICAL_MILE
WIDTH = 4 * METERS_IN_ONE_NAUTICAL_MILE
CENTER_DEPTH = 110  # m
SLOPE = math.radians(1.5)  # convert degree to radian

# 计算给定位置的覆盖宽度，输入深度，输出宽度
OPENING_ANGLE = math.radians(120)  # convert degree to radian


def calculate_coverage_width(depth):
    """
    Calculate the coverage width for a given depth.

    Args:
    - depth (float): depth at the given position

    Returns:
    - float: coverage width at the given depth
    """
    return 2 * depth * math.tan(OPENING_ANGLE / 2)


# 测试
depth_at_center = calculate_depth(x, y)
print("当前位置覆盖宽度：",calculate_coverage_width(depth_at_center))  # 输出中心点的覆盖宽度

# 计算下一条测线的位置：输入前一个位置的深度和前一个位置的覆盖宽度，输出输出距离上一条测试线的位置
SLOPE = math.radians(1.5)  # convert degree to radian
def estimate_next_line_position(prev_depth, prev_coverage_width):
    """
    根据先前的深度和覆盖宽度估计下一条测量线的位置。

    参数：
    - prev_depth（浮点）：前一个位置的深度
    - prev_coverage_width（浮点）：前一个位置的覆盖宽度

    返回：
    - 浮点数：下一条测量线的估计位置
    """
    # 计算减少深度所需的水平移动 覆盖宽度
    horizontal_movement = prev_coverage_width * math.tan(SLOPE)

    # 计算预期的下一个深度
    next_depth = prev_depth - horizontal_movement * math.sin(SLOPE)

    # 计算预期的下一个覆盖范围
    next_coverage_width = calculate_coverage_width(next_depth)

    # 调整 10% 重叠
    adjusted_movement = 0.9 * (prev_coverage_width + next_coverage_width) / 2

    return adjusted_movement


# 测试
initial_depth = 110.0
initial_coverage_width = calculate_coverage_width(initial_depth)
print(estimate_next_line_position(initial_depth, initial_coverage_width))



# 计算东边的深度，然后从东边开始逐渐向西移动。输入海域宽度，输出为测线位置
def calculate_overlap_rate(prev_position, current_position, prev_coverage_width, current_coverage_width):
    """
    根据先前和当前的位置以及覆盖宽度，计算实际的重叠率。

    参数：
    - prev_position (float): 先前的位置
    - current_position (float): 当前位置
    - prev_coverage_width (float): 先前的覆盖宽度
    - current_coverage_width (float): 当前的覆盖宽度

    返回：
    - float: 重叠率（百分比）
    """
    d = current_position - prev_position  # 两条测线之间的距离
    overlap_rate = 1 - (d / current_coverage_width)
    return overlap_rate * 100  # 转换为百分比

def adjust_position_for_overlap(prev_position, prev_coverage_width, initial_estimate_position):
    """
    根据初始估计的位置进行调整，以满足重叠率要求。

    参数：
    - prev_position (float): 先前的位置
    - prev_coverage_width (float): 先前的覆盖宽度
    - initial_estimate_position (float): 初始估计的当前位置

    返回：
    - float: 调整后的位置
    """
    current_position = initial_estimate_position
    current_depth = calculate_depth(current_position, 0)
    current_coverage_width = calculate_coverage_width(current_depth)

    overlap_rate = calculate_overlap_rate(prev_position, current_position, prev_coverage_width, current_coverage_width)

    # 微调的量
    adjustment = METERS_IN_ONE_NAUTICAL_MILE * 0.40  # 1% of a nautical mile as initial adjustment

    # 如果重叠率不在10%~20%范围内，进行调整
    while not (10 <= overlap_rate <= 20):
        if overlap_rate < 10:
            current_position -= adjustment  # 减少位置以增加重叠

        else:
            current_position += adjustment  # 增加位置以减少重叠

        current_depth = calculate_depth(current_position, 0)
        current_coverage_width = calculate_coverage_width(current_depth)
        overlap_rate = calculate_overlap_rate(prev_position, current_position, prev_coverage_width,
                                              current_coverage_width)

        # 减少微调量，确保最终会接近目标重叠率
        adjustment *= 0.9


    return current_position


def calculate_survey_lines(total_width):
    lines_positions = [0]  # 初始位置
    overlap_rates = []

    current_position = 0
    current_depth = calculate_depth(current_position, 0)
    current_coverage_width = calculate_coverage_width(current_depth)

    while current_position < total_width:
        next_movement = estimate_next_line_position(current_depth, current_coverage_width)
        initial_estimate_position = current_position + next_movement

        # 根据实际重叠率进行调整
        adjusted_position = adjust_position_for_overlap(current_position, current_coverage_width,
                                                        initial_estimate_position)

        current_position = adjusted_position
        lines_positions.append(current_position)

        current_depth = calculate_depth(current_position, 0)
        current_coverage_width = calculate_coverage_width(current_depth)

        # 计算并添加重叠率到列表中
        if len(lines_positions) >= 2:
            overlap_rate = calculate_overlap_rate(lines_positions[-2], current_position, current_coverage_width,
                                                  calculate_coverage_width(calculate_depth(lines_positions[-2], 0)))
            overlap_rates.append(overlap_rate)

    # 打印所有的重叠率
    for idx, rate in enumerate(overlap_rates, 1):
        print(f"Overlap Rate between Line {idx} and Line {idx + 1}: {rate:.2f}%")

    return lines_positions


# 测试函数
lines_positions = calculate_survey_lines(WIDTH)

# 各个测点的海水深度
positions = lines_positions

# 计算所有位置的深度
depths = [calculate_depth(x, 0) for x in positions]

# 输出深度和覆盖宽度
# for idx, depth in enumerate(depths):
    # print(f"位置 {positions[idx]} 的深度为 {depth:.2f} 米")
    # print(f"深度 {depth} 的覆盖宽度为 {calculate_coverage_width(depth):.2f} 米")

# 绘制图像来显示
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def calculate_diagonal_endpoints(prev_position, prev_coverage_width):
    next_movement = estimate_next_line_position(calculate_depth(prev_position[0], prev_position[1]), prev_coverage_width)
    new_x_position = prev_position[0] + next_movement

    # 如果是奇数线，则从北边斜向南边，偶数线从南边斜向北边
    y_position = LENGTH if prev_position[1] == 0 else 0

    return new_x_position, y_position

def calculate_survey_lines_diagonal(total_width):
    lines_positions = [(22.5, 0)]  # 初始位置在东北角
    overlap_rates = []

    current_position = lines_positions[0]
    current_depth = calculate_depth(current_position[0], current_position[1])
    current_coverage_width = calculate_coverage_width(current_depth)

    while current_position[0] < total_width:
        new_x_position, y_position = calculate_diagonal_endpoints(current_position, current_coverage_width)

        # 根据实际重叠率进行调整
        adjusted_position_x = adjust_position_for_overlap(current_position[0], current_coverage_width, new_x_position)
        current_position = (adjusted_position_x, y_position)
        lines_positions.append(current_position)

        current_depth = calculate_depth(current_position[0], current_position[1])
        current_coverage_width = calculate_coverage_width(current_depth)

    return lines_positions



# 设置支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def visualize_survey_lines_diagonal_with_coverage(lines_positions, width, length):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim([0, width])
    ax.set_ylim([0, length])

    for idx, pos in enumerate(lines_positions):
        x, y = pos

        # 绘制船的路径
        if idx % 2 == 0:
            plt.plot([x, x], [0, length], 'b-', label='North Start Line' if idx == 0 else "")
        else:
            plt.plot([x, x], [length, 0], 'g-', label='South Start Line' if idx == 0 else "")

        # 添加船舶影响范围
        current_depth = calculate_depth(x, y)
        coverage_width = calculate_coverage_width(current_depth)
        rect = patches.Rectangle((x - coverage_width / 2, 0), coverage_width, length, linewidth=1, edgecolor='none',
                                 facecolor='c', alpha=0.3)
        ax.add_patch(rect)


    plt.xlabel("东---<长度 (m)--->西")
    plt.ylabel("北---<宽度 (m)--->南")
    plt.title("船舶路径及海域视图")
    ax.legend(loc='upper left')
    plt.show()


# 测试新的可视化函数
lines_positions = calculate_survey_lines_diagonal(WIDTH)
visualize_survey_lines_diagonal_with_coverage(lines_positions, WIDTH, LENGTH)


def calculate_total_distance_with_turns(lines_positions):
    """
    Calculate the total distance traveled by the ship based on line positions, including turns.

    Args:
    - lines_positions (list of tuples): Each tuple represents the (x, y) position of a line.

    Returns:
    - float: Total distance traveled by the ship.
    """
    total_distance = 0
    for idx in range(1, len(lines_positions)):
        vertical_distance = abs(lines_positions[idx][1] - lines_positions[idx-1][1])
        horizontal_distance = abs(lines_positions[idx][0] - lines_positions[idx-1][0])
        total_distance += vertical_distance + horizontal_distance
    return total_distance

lines_positions = calculate_survey_lines_diagonal(WIDTH)
total_distance = calculate_total_distance_with_turns(lines_positions)
print(f"考虑转弯，船行驶的总距离为：{total_distance:.2f} 米")
# 考虑转弯，船行驶的总距离为：141197.39 米
print(lines_positions)
