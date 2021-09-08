
class TextDisplay:
    def __init__(self, get_room, EP, exit_game):
        self.get_room  = get_room
        self.EP        = EP
        self.exit_game = exit_game

    def render_menu(self, new_game, load_game, can_load_game):
        print("Welcome to the adventure game")
        if can_load_game:
            print("[1]: Start a New Game (warning: this will overwrite any saved progress)")
            print("[2]: Load Game")
        else:
            print("[1]: Start a New Game")
            print("[2]: Load Game is not available right now. Please start a new game")
        print("[q]: Quit")
        user_input = input("")
        try:
            user_input = int(user_input)
        except Exception as e:
            print("")
            print(e)
            print("")
            user_input = str(user_input)
            if user_input == "q" or user_input == "Q":
                self.exit_game()
            self.EP.print_error(43, user_input)
            return self.render_menu(new_game, load_game, can_load_game)

        if user_input == 1 or (user_input == 2 and not can_load_game):
            return new_game()
        elif user_input == 2:
            return load_game()
        self.EP.print_error(42, user_input)
        return self.render_menu(new_game, load_game, can_load_game)

    def print_room(self, room):
        print("You are in {}".format(room.name))
        print("Available connections:")
        i = 0
        for conn in room.connections:
            i += 1
            conn = self.get_room(conn)
            print("[{}]: {}".format(i, conn.name))

        user_input = input("")
        try:
            user_input = int(user_input)
        except:
            try:
                user_input = str(user_input)
                for conn in room.connections:
                    temp_room = self.get_room(conn)
                    if user_input == temp_room.name:
                        return temp_room.room_num
            except Exception as e:
                print("exception raised: {}".format(e))
                pass
            if user_input == "q" or user_input == "Q":
                self.exit_game()
            self.EP.print_error(43, user_input)
            return self.print_room(room)
        if user_input >= 1 and user_input <= i:
            temp_room = self.get_room(room.connections[user_input - 1])
            return temp_room.room_num
        self.EP.print_error(42, user_input)
        return self.print_room(room)

    def move(self, room, turns):
        print("")
        if turns == 1:
            print("Moving to {}, you have used {} turn".format(room.name, turns))
        else:
            print("Moving to {}, you have used {} turns".format(room.name, turns))
        print("")

if __name__ == "__main__":
    from room import Room
    import log_writer    as LW
    import config_loader as CL
    log = LW.LogWriter()
    config = CL.ConfigLoader(log.write)
    r_1 = Room(config)
    r_2 = Room(config)
    r_3 = Room(config)
    r_1.set_up("Room 1", 0, 1)
    r_2.set_up("Room 2", 0, 2)
    r_3.set_up("Room 3", 0, 3)
    r_1.add_room(r_2.room_num)
    r_1.add_room(r_3.room_num)

    def get_room(room_num):
        if room_num == 1:
            return r_1
        elif room_num == 2:
            return r_2
        else:
            return r_3

    td = TextDisplay(get_room)
    ret = td.print_room(r_1)
    print("returned {}".format(ret))
