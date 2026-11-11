# Obstacle-counting analysis
# Count the objects obstructing the target's goal path.
# Detect fixed obstacles that make the goal unreachable.
# Identify dependencies between obstructions.
# Represent linear dependency chains using a linked list.
def obstacle_heuristic(current_state: TrafficState, goal_state: TrafficState) -> int:
    """
    Count the distinct objects that must move to clear the
    target's goal path
    Args:
        state (TrafficState): The current state of the puzzle.
    Returns:
        int: The number of distinct objects identified as
            necessary to clear the goal path.
    """
    def get_orientation(coordinates):
        # horizontal
        if coordinates[0][0] == coordinates[1][0]:
            return '-'
        # vertical
        if coordinates[0][1] == coordinates[1][1]:
            return '|'
    def count_horizontal_obstructions(current_coordinates, end_coordinates):
        if current_coordinates[0][1] < end_coordinates[0][1]:
            # Moving right
            # check from the current right edge to the goal's right edge
            start = current_coordinates[-1][1] + 1
            end = end_coordinates[-1][1] + 1
        else:
            # Moving left
            # check from the goal's left edge to the current left edge
            start = end_coordinates[0][1]
            end = current_coordinates[0][1]
        obstacles_count = 0
        for i in range(start, end):
            cell_r, cell_c = (current_coordinates[0][0], i)
            cell_value = current_state.blockstate[cell_r][cell_c]
            if cell_value == 0:
                # free cell
                continue
            else:
                obstacles_count += 1
        return obstacles_count
    def count_vertical_obstructions(current_coordinates, end_coordinates):
        if current_coordinates[0][0] < end_coordinates[0][0]:
            # Moving down
            # Check from the current bottom edge to the goal's bottom edge
            start = current_coordinates[-1][0] + 1
            end = end_coordinates[-1][0] + 1
        else:
            # Moving up
            # Check from the goal's top edge to the current top edge
            start = end_coordinates[0][0]
            end = current_coordinates[0][0]
        obstacles_count = 0
        for i in range(start, end):
            cell_r, cell_c = (i, current_coordinates[0][1])
            cell_value = current_state.blockstate[cell_r][cell_c]
            if cell_value == 0:
                # free cell
                continue
            else:
                obstacles_count += 1
        return obstacles_count
    total_obstacles = 0
    for target_num in goal_state.blocknumlist:
        current_coordinates = current_state.blockcells(target_num)
        end_coordinates = goal_state.blockcells(target_num)
        o = get_orientation(current_coordinates)
        if o == '-': 
            total_obstacles += count_horizontal_obstructions(
                current_coordinates, end_coordinates
            )
        elif o == '|':
            total_obstacles += count_vertical_obstructions(
                current_coordinates, end_coordinates
            )
    return total_obstacles

