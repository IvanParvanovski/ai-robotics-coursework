from math import inf
# Clearance-space analysis
# Check whether an obstruction has enough space to clear the goal path.
# Account for board boundaries, fixed obstacles, and movable objects.
# Identify dependencies when other objects block the required movement.
# Trace from the goal path to discover dependencies.
# Work backwards through the dependencies to determine movement order.
def clearance_heuristic(current_state: TrafficState, goal_state: TrafficState) -> float:
    """
    Estimate the minimum number of moves required to clear
    all next obstructions along the target object's goal path.
    The heuristic considers dependencies between objects and
    favours states that avoid introducing additional dependencies.
    Args:
        current_state (TrafficState): The current state of the puzzle.
        goal_state (TrafficState): The goal state of the puzzle.
    Returns:
        float: The estimated clearance cost, or infinity if impossible.
    """
    def get_orientation(coordinates):
        """
        Determine the orientation of an object based on its coordinates.
        Args:
            coordinates (list[tuple[int, int]]): Coordinates occupied by the object.
        Returns:
            str: '-' for horizontal or '|' for vertical orientation.
        """
        # horizontal
        if coordinates[0][0] == coordinates[1][0]:
            return '-'
        # vertical
        if coordinates[0][1] == coordinates[1][1]:
            return '|'
    def object_at(cell):
        """
        Identify the object occupying a cell
        """
        r, c = cell
        value = current_state.blockstate[r][c]
        if value == 0:
            return None
        if value == '#':
            return '#'
        if value == '*':
            return ('cone', r, c)
        block_num = current_state.blocknum(value)
        if block_num is None:
            raise ValueError(f"Unsupported cell value: {value!r}")
        return ('block', block_num)
    def distance_to_board_boundary(direction_name, coordinates):
        max_distance = 0
        if direction_name == 'right':
            max_distance = current_state.ncols - 1 - max(c for r, c in coordinates)
        elif direction_name == 'left':
            max_distance = min(c for r, c in coordinates)
        elif direction_name == 'down':
            max_distance = current_state.nrows - 1 - max(r for r, c in coordinates)
        elif direction_name == 'up':
            max_distance = min(r for r, c in coordinates)
        return max_distance
    def generate_clearance_movements(cell, path_cells_to_clear):
        directions = {
            'down': (1, 0),
            'right': (0, 1),
            'up': (-1, 0),
            'left': (0, -1)
        }
        obj = object_at(cell)
        # The cell is empty or it contains a box
        if obj is None or obj == '#':
            return
        obj_type = obj[0]
        # Identify permitted movement directions
        if obj_type == 'cone':
            coordinates = [(obj[1], obj[2])]
            allowed_directions = directions
        elif obj_type == 'block':
            coordinates = current_state.blockcells(obj[1])
            orientation = get_orientation(coordinates)
            if orientation == '-':
                allowed_directions = {
                    'right': directions['right'],
                    'left': directions['left']
                }
            else:
                allowed_directions = {
                    'down': directions['down'],
                    'up': directions['up']
                }
        # Evaluate each permitted direction to find the minimum displacement
        # required to move the obstruction away from the target's path
        for direction_name, (dr, dc) in allowed_directions.items():
            # Determine how far the object can move before reaching the board boundary
            max_distance = distance_to_board_boundary(
                direction_name, coordinates
            )
            # Multiply by the distance to move the object that many cells
            for distance in range(1, max_distance + 1):
                # Calculate the object's hypothetical position after moving
                shifted_coordinates = {
                    (r + distance * dr, c + distance * dc)
                    for r, c in coordinates
                }
                # Stop shifting once the block has moved far enough
                # to completely clear the required path
                if shifted_coordinates.isdisjoint(path_cells_to_clear):
                    # Exclude cells already occupied by the object to identify newly entered cells
                    movement_path = shifted_coordinates - set(coordinates)
                    yield direction_name, distance, movement_path
                    break
    def resolve_obstruction(cell, active=None):
        """
        Estimate the minimum movements required to clear an obstruction,
        including dependencies on other objects.
        Evaluate all feasible clearance directions and recursively calculate
        the cost of resolving additional obstructions. Select the direction
        with the lowest total estimated cost.
        The algorithm consists of six steps:
        1. Identify the obstruction and its permitted movement directions.
        2. Calculate the minimum displacement required to clear the path.
        3. Construct the movement path for each direction.
        4. Eliminate directions blocked by board boundaries or fixed obstacles.
        5. Recursively calculate the cost of resolving dependencies.
        6. Return the lowest total estimated clearance cost.
        The recursive dependency structure resembles a decision tree,
        with each branch representing a possible clearance direction.
        Exploring tree-search optimization techniques could help reduce
        redundant calculations and improve efficiency.
        Args:
            cell (tuple[int, int]): Cell where the obstruction intersects the path.
        Returns:
            float: The estimated minimum clearance cost, including dependencies.
        """
        if active is None:
            active = set()
        obj = object_at(cell)
        if obj == '#' or obj == ('block', target_num):
            return inf
        if obj in active:
            return inf
        path_cells_to_clear = {cell}
        best_cost = inf
        # Calculate cost to clear an obstruction
        for direction_name, distance, movement_path in generate_clearance_movements(
            cell, path_cells_to_clear
        ):
            # Start with the cost of moving the obstruction itself
            cost = distance
            # Traverse the cells required for this movement
            for path_cell in movement_path:
                dependency = object_at(path_cell)
                # Ignore empty cells and the moving object itself
                if dependency is None or dependency == obj:
                    continue
                # A wall makes this direction impossible
                if dependency == '#':
                    cost = inf
                    break
                # Calculate the cost of clearing another obstruction
                cost += resolve_obstruction(path_cell, active | {obj})
            # Keep the cheapest direction
            best_cost = min(best_cost, cost)
        return best_cost
    def calculate_path_clearance(current_coordinates, end_coordinates):
        """
        Estimate the movements required to clear obstructions along
        the target object's path to its goal.
        Args:
            current_coordinates (list): Current coordinates of the target.
            end_coordinates (list): Goal coordinates of the target.
        Returns:
            float: The estimated total clearance cost.
        """
        orientation = get_orientation(current_coordinates)
        # Select the movement axis.
        axis = 1 if orientation == '-' else 0
        current_head = current_coordinates[0][axis]
        goal_head = end_coordinates[0][axis]
        if current_head == goal_head:
            return 0
        if current_head < goal_head:
            # Moving right / down
            start = current_coordinates[-1][axis] + 1
            end = end_coordinates[-1][axis] + 1
        else:
            # Moving left / up
            start = goal_head
            end = current_head
        clearance_cost = 0
        # Traverse the goal path and identify obstructions.
        for position in range(start, end):
            if orientation == '-':
                cell = (current_coordinates[0][0], position)
            else:
                cell = (position, current_coordinates[0][1])
            obj = object_at(cell)
            # Ignore empty cells
            if obj is None:
                continue
            clearance_cost += resolve_obstruction(cell)
        return clearance_cost
    if not goal_state.blocknumlist:
        return 0
    target_num = goal_state.blocknumlist[0]
    current_coordinates = current_state.blockcells(target_num)
    end_coordinates = goal_state.blockcells(target_num)
    return calculate_path_clearance(current_coordinates, end_coordinates)

