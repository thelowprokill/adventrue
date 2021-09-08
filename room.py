##################################################
#                                                #
# Class Room                                     #
#                                                #
# name:        :string                           #
# room_type:   :int                              #
# room_num:    :int                              #
# connections: :list[int]                        #
#                                                #
##################################################
class Room:
    def __init__(self, config):
        self.config = config
        self.set_up("", 0, 0)

    def set_up(self, name, room_type, room_num):
        self.name               = name
        self.room_type          = room_type
        self.room_num           = room_num
        self.connections        = []
        self.target_connections = 0

    def set_target_connections(self, connections):
        self.target_connections = connections

    def can_add_connections(self):
        conn_len = len(self.connections)
        return conn_len < self.target_connections, conn_len < self.config.MIN_CONNECTIONS, conn_len < self.config.MAX_CONNECTIONS

    def set_type(self, room_type):
        self.room_type = room_type

    def has_connection(self, room_num):
        for conn in self.connections:
            if conn == room_num:
                return True
        return False

    def add_room(self, new_room_number):
        self.connections = self.connections + [new_room_number]

    def print_room(self):
        print("Room: {} number: {} type: {} target_connections: {}".format(self.name, self.room_num, self.room_type, self.target_connections))
        for conn in self.connections:
            print("conn: {}".format(conn))


if __name__ == "__main__":
    import config_loader as cl
    import log_writer    as lw
    log = lw.LogWriter()
    config = cl.ConfigLoader(log.write)

    room = Room(config)
    room.set_up("Awesome room name", 0, 1)
    room.set_target_connections(3)
    room.print_room()
    room.add_room(2)
    room.add_room(3)
    room.add_room(4)
    room.add_room(5)
    room.add_room(6)
    room.print_room()
    target_conn, max_conn = room.can_add_connections()
    print("Can add with target: {}, can add: {}".format(target_conn, max_conn))



