from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Store map as graph dictionary
map_graph = {}

# create a function for direction of travel
def travel_direction(direction):
    return player.travel(direction)

# create dictionary for each room visited
def current_room_vertex():
    room = {}
    for exit in player.current_room.get_exits():
        room[exit] = "X"
        map_graph[player.current_room.id] = room

# Find the exits that haven't been visited
def current_room_unexplored_exit():
# Gotta have a place to keep track of unexplored exits
    unexplored = []
# now check the current room for exits
    for exit in player.current_room.get_exits():
# look for the "X" which marks an exit as unexplored
        if map_graph[player.current_room.id][exit] == "X":
            unexplored.append(exit)
# now we'll randomize the options from unexplored
    return random.choice(unexplored)

# We're going to use BFT 
def find_nearest_unexplored_exit(room_id):
    visited = set()
    q = Queue()
    q.enqueue([room_id])

    while q.size() > 0:
        path = q.dequeue()
        current_room = path[-1]
# this is where we check to see if this room has unexplored exits, and return path
        if list(map_graph[current_room].values()).count('X') != 0:
            return path
        if current_room not in visited:
            visited.add(current_room)
# Now that we put the current room in the visited list, queue up the rooms that still need checks done
            for new_room in map_graph[current_room].values():
                new_path = path.copy()
                new_path.append(new_room)
                q.enqueue(new_path)

# initialize the map graph at the first location
current_room_vertex()
# now we're going to loop through the map and build a graph
while len(map_graph) < len(room_graph):
# So now we will go down the path of rooms marked unexplored with the "X"
# check map_graph for the current room, and then look for the "X" exits
# we'll return a list of values for the current room, when the count is 0, the room has no unexplored exits and we'll need to backtrack
    if list(map_graph[player.current_room.id].values()).count('X') != 0:
# we need to track the room numbers
        room_id_before_move = player.current_room.id
# traverse in a random direction
        random_exit = current_room_unexplored_exit()
# move in the random direction
        travel_direction(random_exit)
# add it to the traversal path
        traversal_path.append(random_exit)
# check the room, is it part of map_graph? if not, create a new room
        if player.current_room.id not in map_graph:
            current_room_vertex()
# assign room number to previous room exits
        map_graph[room_id_before_move][random_exit] = player.current_room.id
# assign previous room id to current room, reverse directions
        reversed_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        map_graph[player.current_room.id][reversed_directions[random_exit]] = room_id_before_move
    else:
# use bft to find the nearest room marked with "X"
# room_id can be used to create edges
        reverse_path = find_nearest_unexplored_exit(player.current_room.id)
# traverse backwards
        for each_room_id in reverse_path:
            for each_direction in map_graph[player.current_room.id]:
                if map_graph[player.current_room.id][each_direction] == each_room_id:
                    player.travel(each_direction)
                    traversal_path.append(each_direction)
                    break




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
