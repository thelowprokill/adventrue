from room import Room
import random
import crypto
import sys

class GenerateGame:
    def __init__(self, message, config, EP, exit_game):
        self.message = message
        self.config = config
        self.exit_game = exit_game
        self.read_room_list()
        self.EP = EP
        try:
            import key
            self.key = key.key()
        except:
            try:
                self.key = crypto.key_gen(128)
                self.key = self.key.replace("\n", "")
                key_file = open("key.py", "w+")
                key_file.write("def key():")
                key_file.write("\treturn \"{}\"".format(self.key))
                key_file.close()
            except:
                self.message(0, "Keygen failed. Try again later")
                self.message(0, "Defaulting to non encrypted save games")
                self.config.DEBUG = True

    def load_game(self):
        saved_game = open(self.config.SAVE_GAME, "r", encoding='utf-8')
        string = ""
        i = 0
        for line in saved_game:
            if i == 0:
                encrypted = line
                i = 1
            else:
                string += line


        saved_game.close()

        pre, encrypted = self.read_config_line(encrypted)

        if encrypted == "1":
            try:
                string = crypto.de_code(self.key, string)
            except:
                self.message(0, "Decryption failed.")

        splits = string.split("\n")
        i = 0
        rooms = []
        tmp = None
        try:
            for s in splits:
                prefix, data = self.read_config_line(s)

                if prefix == "current_room":
                    current_room = int(data)
                elif prefix == "turns":
                    turns = int(data)
                elif prefix == "room":
                    tmp = Room(self.config)
                elif prefix == "room_end":
                    rooms.append(tmp)
                elif prefix == "room_name":
                    tmp.name = data
                elif prefix == "room_num":
                    tmp.room_num = int(data)
                elif prefix == "conn_target":
                    tmp.set_target_connections(int(data))
                elif prefix == "room_type":
                    tmp.room_type = int(data)
                elif prefix == "conn":
                    tmp.add_room(int(data))
            return rooms, rooms[current_room], turns
        except Exception as e:
            self.EP.print_error(1, e)
            self.exit_game()



    def save_game(self, rooms, current_room, turns):
        string = ""
        string += "current_room ={}\n".format(current_room.room_num)
        string += "turns        ={}\n".format(turns)
        for r in rooms:
            string += "room:\n".format(r.room_num)
            string += "\troom_name   ={}\n".format(r.name)
            string += "\troom_num    ={}\n".format(r.room_num)
            string += "\troom_type   ={}\n".format(r.room_type)
            string += "\tconn_target ={}\n".format(r.target_connections)
            for conn in r.connections:
                string += "\t\tconn ={}\n".format(conn)
            string += "room_end:\n"

        encrypted = "0"
        if not self.config.DEBUG:
            encrypted = "1"
            string = crypto.in_code(self.key, string)

        string = "is_encrypted ={}\n".format(encrypted) + string
        new_save = open(self.config.SAVE_GAME, "w+", encoding='utf-8')
        new_save.write(string)
        new_save.close()
        pass

    def read_config_line(self, s):
        prefix = s[:s.rfind("=")].replace('\t', '').replace(" ", "")
        suffix = s[s.rfind("=") + 1:].replace('\n', '')

        return prefix, suffix

    def new_game(self):
        number_of_rooms = self.config.NUM_ROOMS
        list_len = len(self.room_list)
        if number_of_rooms > list_len - 1:
            number_of_rooms = list_len - 1

        new_rooms = []
        for i in range(number_of_rooms):
            tmp = self.add_room(new_rooms)
            new_rooms.append(tmp)

        rooms = []
        i = 0
        for r in new_rooms:
            tmp = Room(self.config)
            tmp.set_up(r, 0, i)
            rooms.append(tmp)
            i += 1

        for r in rooms:
            target_connections = random.randrange(self.config.MIN_CONNECTIONS, self.config.MAX_CONNECTIONS)
            r.set_target_connections(target_connections)
            for i in range(target_connections):
                self.add_connection(rooms, r)

        self.set_start_room(rooms)
        self.set_end_room(rooms)
        return rooms

    def set_start_room(self, rooms):
        start_room = random.randrange(0, len(rooms))
        if rooms[start_room].room_type == 0:
            rooms[start_room].room_type = 1
            return
        return self.set_start_room(rooms)

    def set_end_room(self, rooms):
        end_room = random.randrange(0, len(rooms))
        if rooms[end_room].room_type == 0:
            rooms[end_room].room_type = 2
            return
        return self.set_end_room(rooms)

    def add_room(self, new_rooms):
        tmp = random.randrange(0, len(self.room_list))
        tmp = self.room_list[tmp]
        if tmp in new_rooms:
            return self.add_room(new_rooms)
        return tmp

    def add_connection(self, rooms, room):
        target, _, _ = room.can_add_connections()
        if target:
            rooms_without_target = []
            rooms_without_min    = []
            rooms_without_max    = []
            for r in rooms:
                t, mi, ma = r.can_add_connections()
                has_conn = r.has_connection(room.room_num)
                if r.room_num != room.room_num:
                    if not has_conn and mi:
                        rooms_without_min.append(r)
                        rooms_without_target.append(r)
                        rooms_without_max.append(r)
                    if not has_conn and t:
                        rooms_without_target.append(r)
                        rooms_without_max.append(r)
                    elif not has_conn and ma:
                        rooms_without_max.append(r)

            if len(rooms_without_min) + len(rooms_without_target) + len(rooms_without_max) == 0:
                return
            new_conn = 0
            if len(rooms_without_min) > 0:
                new_conn  = random.randrange(0, len(rooms_without_min))
                dest_room = rooms_without_min[new_conn]
                new_conn  = dest_room.room_num
            if len(rooms_without_target) > 0:
                new_conn  = random.randrange(0, len(rooms_without_target))
                dest_room = rooms_without_target[new_conn]
                new_conn  = dest_room.room_num
            elif len(rooms_without_max) > 0:
                new_conn  = random.randrange(0, len(rooms_without_max))
                dest_room = rooms_without_max[new_conn]
                new_conn  = dest_room.room_num
            else:
                return

            room.add_room(new_conn)
            dest_room.add_room(room.room_num)
            return
        else:
            return



    def write_stock_room_list(self):
        room_list = [
            "Kitchen",
            "Living Room",
            "Basement",
            "Office",
            "Basement",
            "Porch",
            "Foyer",
            "Yard"
        ]

        fp = open(".room_list", "w+")
        for line in room_list:
            fp.write(line + "\n")
        fp.close()

    def read_room_list(self):
        try:
            fp = open(".room_list", "r")
            lines = fp.readlines()
            fp.close()

            res = []
            for line in lines:
                res.append(line.replace("\n", ""))

            self.room_list = res
            return res
        except:
            self.write_stock_room_list()
            return self.read_room_list()

if __name__ == "__main__":
    import config_loader as CL
    import log_writer    as LW
    log = LW.LogWriter()
    config = CL.ConfigLoader(log.write)

    gen_room = GenerateGame(log.write, config)
    print(room_names)
    rooms = gen_room.new_game()
    for r in rooms:
        r.print_room()
