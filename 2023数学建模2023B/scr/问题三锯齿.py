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
x, y =WIDTH ,LENGTH # 西边最深
# x, y =0,0 # 东边最浅

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
    overlap_rate = 1 - (d / prev_coverage_width)
    return overlap_rate * 100  # 转换为百分比

lines_positions_down = [0, 40.504746028626776, 84.31235825121242, 131.69216128190178, 182.9354411899895, 238.357236296182, 298.2982739952151, 363.12706551220884, 433.24217147110414, 509.074652203657, 591.0907178632348, 679.7945946360355, 775.7316246708989, 879.4916187857498, 991.7124825627657, 1113.0841381251198, 1244.3527657059726, 1386.3253910864353, 1539.8748471055915, 1705.9451397454245, 1885.5572517807748, 2079.815419674563, 2289.9139223079724, 2517.1444232819913, 2762.9039119300223, 3028.7032918620657, 3316.17666984195, 3627.0914021046606, 3963.3589598774606, 4327.046680904906, 4720.390479224887, 5145.808591334077, 5605.916443252776, 6103.542729890291, 6641.746805565139, 7223.837492595134, 7853.393423590635]
lines_positions_up = [22.5, 64.83945668973182, 110.63138682719902, 160.15731440536797, 213.72171964259397, 271.6539108951306, 334.31004921043194, 402.07533796798907, 475.3663910693841, 554.6337942369457, 640.3648751676023, 733.0866995725494, 833.3693115220683, 941.8292380167981, 1059.1332793311967, 1186.002608431828, 1323.2172046732671, 1471.6206490295237, 1632.125310341564, 1805.717954465438, 1993.4658108054668, 2196.523133528903, 2416.1382977997237, 2653.6614746584555, 2910.552931732399, 3188.392010808137, 3488.8868374595136, 3813.884822424854, 4165.384019294798, 4545.545408336615, 4956.706181974678, 5401.394113604827, 5882.343098080603, 6402.509959412617, 6965.092629013048, 7573.549806243207]

def adjust_position_for_overlap(prev_position, prev_coverage_width, initial_estimate_position):
    """
    根据初始估计的位置进行调整，以满足重叠率要求。
    """
    current_position = initial_estimate_position
    current_depth = calculate_depth(current_position, 0)
    current_coverage_width = calculate_coverage_width(current_depth)

    overlap_rate = calculate_overlap_rate(prev_position, current_position, prev_coverage_width, current_coverage_width)

    # 微调的量
    adjustment = METERS_IN_ONE_NAUTICAL_MILE * 0.01  # 1% of a nautical mile as initial adjustment

    max_iterations = 100  # Set a max iteration limit
    no_improvement_iterations = 0  # Track iterations without improvement
    last_overlap_rate = 0  # Track last overlap rate

    # 如果重叠率不在10%~20%范围内，进行调整
    while not (10 <= overlap_rate <= 20) and max_iterations > 0 and adjustment > 1:  # Check for adjustment threshold
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

        # Check for improvement
        if abs(overlap_rate - last_overlap_rate) < 0.01:  # less than 0.01% change is considered no improvement
            no_improvement_iterations += 1
        else:
            no_improvement_iterations = 0

        if no_improvement_iterations > 5:  # exit if no improvement for 5 consecutive iterations
            break

        last_overlap_rate = overlap_rate
        max_iterations -= 1

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

print(lines_positions)

# 绘制图像来显示
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def calculate_diagonal_endpoints(prev_position, prev_coverage_width):
    next_movement = estimate_next_line_position(calculate_depth(prev_position[0], prev_position[1]), prev_coverage_width)
    new_x_position = prev_position[0] + next_movement

    # 如果是奇数线，则从北边斜向南边，偶数线从南边斜向北边
    y_position = LENGTH if prev_position[1] == 0 else 0

    return new_x_position, y_position

def calculate_survey_lines_diagonal(total_width):
    lines_positions = [(0, 0)]  # 初始位置在东北角
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
def visualize_survey_lines_diagonal(lines_positions, total_width, total_length):
    plt.figure(figsize=(10, 5))
    for idx, (start, end) in enumerate(zip(lines_positions[:-1], lines_positions[1:])):
        color = 'blue' if idx % 2 == 0 else 'red'
        plt.plot([start[0], end[0]], [start[1], end[1]], color=color, label=f"Line {idx+1}")
    plt.xlim(0, total_width)
    plt.ylim(0, total_length)
    plt.xlabel("东---<长度 (m)--->西")
    plt.ylabel("北---<宽度 (m)--->南")
    plt.title("船舶路径及海域视图")
    handles, labels = plt.gca().get_legend_handles_labels()
    new_labels, new_handles = [], []
    for handle, label in zip(handles, labels):
        if label not in new_labels:
            new_labels.append(label)
            new_handles.append(handle)

    plt.legend(new_handles, new_labels)
    plt.grid(True)
    plt.show()

lines_positions = calculate_survey_lines_diagonal(WIDTH)
visualize_survey_lines_diagonal(lines_positions, WIDTH, LENGTH)


def visualize_survey_lines_diagonal(lines_positions_down, lines_positions_up, total_width, total_length):
    plt.figure(figsize=(10, 5))

    for idx, (down_x, up_y) in enumerate(zip(lines_positions_down, lines_positions_up)):
        color = 'blue' if idx % 2 == 0 else 'red'

        # 绘制从上到下的线
        if idx > 0:
            plt.plot([lines_positions_down[idx - 1], down_x], [0, 0], color=color)

        # 绘制从下到上的线
        if idx < len(lines_positions_up) - 1:
            plt.plot([up_y, lines_positions_up[idx + 1]],
                     [2 * METERS_IN_ONE_NAUTICAL_MILE, 2 * METERS_IN_ONE_NAUTICAL_MILE], color=color)

        # 添加线的标签
        plt.text(down_x, -50, f'Line {idx + 1}', ha='center', color=color)
        plt.text(up_y, 2 * METERS_IN_ONE_NAUTICAL_MILE + 50, f'Line {idx + 1}', ha='center', color=color)

    plt.xlim(0, total_width)
    plt.ylim(0, total_length)
    plt.xlabel("东---<长度 (m)--->西")
    plt.ylabel("北---<宽度 (m)--->南")
    plt.title("船舶路径及海域视图")
    plt.grid(True)
    plt.show()