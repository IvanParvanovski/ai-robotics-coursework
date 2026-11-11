# Manhattan distance
# Calculate the absolute differences between the current and goal coordinates.
# Sum the horizontal and vertical distances to estimate the remaining movement.
def manhattan_heuristic(current_state: TrafficState, goal_state: TrafficState) -> int:
    """
    Calculate the total Manhattan distance between the current
    positions of target objects and their goal positions.
    Args:
        current_state (TrafficState): The current puzzle state.
        goal_state (TrafficState): The goal puzzle state.
    Returns:
        int: The sum of Manhattan distances for all target objects.
    """
    total = 0
    for target_num in goal_state.blocknumlist:
        current_coordinates = current_state.blockcells(target_num)
        end_coordinates = goal_state.blockcells(target_num)
        r1, c1 = current_coordinates[0]
        r2, c2 = end_coordinates[0]
        distance = abs(r2 - r1) + abs(c2 - c1)
        total += distance
    return total

