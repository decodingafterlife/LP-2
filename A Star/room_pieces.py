import heapq
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Set, Dict

@dataclass
class Object:
    id: int
    width: int
    height: int
    is_square: bool

@dataclass
class Position:
    x: int
    y: int

@dataclass
class PlacedObject:
    obj: Object
    pos: Position
    rotation: bool  # True if rotated 90 degrees

@dataclass
class State:
    room_width: int
    room_height: int
    placed_objects: List[PlacedObject]
    remaining_objects: List[Object]
    occupied_grid: np.ndarray
    
    def is_goal(self) -> bool:
        return len(self.remaining_objects) == 0
    
    def get_occupied_area(self) -> int:
        occupied = 0
        for placed in self.placed_objects:
            width = placed.obj.height if placed.rotation else placed.obj.width
            height = placed.obj.width if placed.rotation else placed.obj.height
            occupied += width * height
        return occupied
    
    def get_empty_area(self) -> int:
        return self.room_width * self.room_height - self.get_occupied_area()
    
    def compute_utilization(self) -> float:
        return self.get_occupied_area() / (self.room_width * self.room_height)
    
    def get_state_hash(self) -> str:
        return str(self.occupied_grid.tobytes())

class RoomArrangement:
    def __init__(self, room_width: int, room_height: int):
        self.room_width = room_width
        self.room_height = room_height
    
    def can_place_object(self, state: State, obj: Object, pos: Position, rotated: bool) -> bool:
        width = obj.height if rotated else obj.width
        height = obj.width if rotated else obj.height
        
        # Check if object fits within room boundaries
        if pos.x < 0 or pos.y < 0 or pos.x + width > state.room_width or pos.y + height > state.room_height:
            return False
        
        # Check if object overlaps with any placed objects
        for x in range(pos.x, pos.x + width):
            for y in range(pos.y, pos.y + height):
                if state.occupied_grid[y, x] == 1:
                    return False
        
        return True
    
    def update_grid(self, grid: np.ndarray, obj: Object, pos: Position, rotated: bool, value: int = 1) -> np.ndarray:
        width = obj.height if rotated else obj.width
        height = obj.width if rotated else obj.height
        
        new_grid = grid.copy()
        for x in range(pos.x, pos.x + width):
            for y in range(pos.y, pos.y + height):
                new_grid[y, x] = value
        
        return new_grid
    
    def get_valid_positions(self, state: State, obj: Object) -> List[Tuple[Position, bool]]:
        valid_positions = []
        
        # Try placing the object with and without rotation
        for rotated in [False, True]:
            # Skip rotation for squares as it doesn't matter
            if obj.is_square and rotated:
                continue
                
            width = obj.height if rotated else obj.width
            height = obj.width if rotated else obj.height
            
            for x in range(state.room_width - width + 1):
                for y in range(state.room_height - height + 1):
                    pos = Position(x, y)
                    if self.can_place_object(state, obj, pos, rotated):
                        valid_positions.append((pos, rotated))
        
        return valid_positions
    
    def heuristic(self, state: State) -> float:
        # Heuristic: estimate quality of placement
        # 1. Space utilization (higher is better)
        utilization = state.compute_utilization()
        
        # 2. Penalty for fragmentation (lower is better)
        fragmentation = self.calculate_fragmentation(state)
        
        # Combined score (we want to maximize utilization and minimize fragmentation)
        # We return negative because A* minimizes cost
        return -1 * (utilization - 0.3 * fragmentation)
    
    def calculate_fragmentation(self, state: State) -> float:
        # Count number of isolated empty cells
        empty_cells = 0
        for y in range(state.room_height):
            for x in range(state.room_width):
                if state.occupied_grid[y, x] == 0:
                    empty_neighbors = 0
                    # Check four adjacent cells
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < state.room_width and 0 <= ny < state.room_height and state.occupied_grid[ny, nx] == 0:
                            empty_neighbors += 1
                    
                    # If cell has no empty neighbors, it's isolated
                    if empty_neighbors == 0:
                        empty_cells += 1
        
        return empty_cells / (state.room_width * state.room_height)
    
    def get_successors(self, state: State) -> List[Tuple[State, float]]:
        successors = []
        
        if not state.remaining_objects:
            return successors
        
        # Try placing the next object at each valid position
        next_obj = state.remaining_objects[0]
        valid_positions = self.get_valid_positions(state, next_obj)
        
        for pos, rotated in valid_positions:
            # Create new state with the object placed
            new_occupied_grid = self.update_grid(state.occupied_grid, next_obj, pos, rotated)
            new_state = State(
                room_width=state.room_width,
                room_height=state.room_height,
                placed_objects=state.placed_objects + [PlacedObject(next_obj, pos, rotated)],
                remaining_objects=state.remaining_objects[1:],
                occupied_grid=new_occupied_grid
            )
            
            # Calculate cost for this placement
            cost = self.heuristic(new_state)
            successors.append((new_state, cost))
        
        return successors
    
    def a_star_search(self, objects: List[Object]) -> List[PlacedObject]:
        # Sort objects by area (largest first) for better initial placement
        objects.sort(key=lambda obj: obj.width * obj.height, reverse=True)
        
        # Create initial state
        initial_state = State(
            room_width=self.room_width,
            room_height=self.room_height,
            placed_objects=[],
            remaining_objects=objects,
            occupied_grid=np.zeros((self.room_height, self.room_width), dtype=int)
        )
        
        # Priority queue for A* search
        open_set = []
        heapq.heappush(open_set, (0, 0, initial_state))  # (f_score, tiebreaker, state)
        
        # Track visited states to avoid cycles
        closed_set = set()
        
        # Track best path
        g_score = {initial_state.get_state_hash(): 0}
        came_from = {}
        tiebreaker = 1
        
        while open_set:
            _, _, current_state = heapq.heappop(open_set)
            
            # If goal reached, return solution
            if current_state.is_goal():
                return current_state.placed_objects
            
            # Mark state as visited
            state_hash = current_state.get_state_hash()
            if state_hash in closed_set:
                continue
            closed_set.add(state_hash)
            
            # Generate successors
            for successor, cost in self.get_successors(current_state):
                successor_hash = successor.get_state_hash()
                
                if successor_hash in closed_set:
                    continue
                
                tentative_g_score = g_score[state_hash] + cost
                
                if successor_hash not in g_score or tentative_g_score < g_score[successor_hash]:
                    # This path is better
                    came_from[successor_hash] = current_state
                    g_score[successor_hash] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(successor)
                    heapq.heappush(open_set, (f_score, tiebreaker, successor))
                    tiebreaker += 1
        
        # No solution found
        return []

def create_objects():
    objects = []
    
    # Create 5 rectangular objects
    for i in range(5):
        width = np.random.randint(3, 8)
        height = np.random.randint(3, 8)
        while width == height:  # Ensure it's not a square
            height = np.random.randint(3, 8)
        objects.append(Object(id=i, width=width, height=height, is_square=False))
    
    # Create 4 square objects
    for i in range(5, 9):
        size = np.random.randint(3, 8)
        objects.append(Object(id=i, width=size, height=size, is_square=True))
    
    return objects

def visualize_placement(room_width, room_height, placed_objects):
    grid = np.zeros((room_height, room_width), dtype=int)
    
    for placed in placed_objects:
        obj = placed.obj
        pos = placed.pos
        rotated = placed.rotation
        
        width = obj.height if rotated else obj.width
        height = obj.width if rotated else obj.height
        
        for y in range(pos.y, pos.y + height):
            for x in range(pos.x, pos.x + width):
                grid[y, x] = obj.id + 1  # +1 to avoid 0 (empty)
    
    # Print the grid
    for y in range(room_height):
        for x in range(room_width):
            print(f"{grid[y, x]:2}", end=" ")
        print()

# Example usage
room_width = 20
room_height = 15
objects = create_objects()

# Print object dimensions
print("Objects:")
for obj in objects:
    obj_type = "Square" if obj.is_square else "Rectangle"
    print(f"ID: {obj.id}, Type: {obj_type}, Dimensions: {obj.width}x{obj.height}")

room_arrangement = RoomArrangement(room_width, room_height)
solution = room_arrangement.a_star_search(objects)

if solution:
    print("\nSolution found!")
    print(f"Placed {len(solution)} objects")
    
    total_area = room_width * room_height
    occupied_area = sum(
        (obj.obj.width if not obj.rotation else obj.obj.height) * 
        (obj.obj.height if not obj.rotation else obj.obj.width) 
        for obj in solution
    )
    utilization = occupied_area / total_area * 100
    
    print(f"Room dimensions: {room_width}x{room_height}")
    print(f"Total room area: {total_area}")
    print(f"Occupied area: {occupied_area}")
    print(f"Space utilization: {utilization:.2f}%")
    
    print("\nPlacement visualization:")
    visualize_placement(room_width, room_height, solution)
else:
    print("No solution found.")