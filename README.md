# adventrue
Python Adventure game

# Jon's Python adventure game.
This is a simple game where you are put into a room.
The objective is to find the exit room located somewhere in the building.
Get there as fast as possible.
Start the game with: $python3 adventure.py

# Customize your experience.
You can customize what rooms come up by modifying the .room_list file.
If you don't see the .room_list file run the game first to create id.
Some further customization can be done in .config.

- num_rooms controls the number of rooms to put in the game.
- min_connections is a soft minimum for the connections.
- max_connections is a hard maximum for the connections.
- log_level determines how much information is printed. All the info is put in the log file. 1 <= log_level <= 2


# Potential features to come.
- Maps: Maps give information about the links between rooms or what room is the exit.
- Keys: Keys allow you to pass connections that have a locked door.
