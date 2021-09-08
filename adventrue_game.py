import generate_game  as GG
import config_loader  as CL
import log_writer     as LW
import text_display   as TD
import error_printing as EP
import sys

class main:
    def __init__(self):
        self.log = LW.LogWriter()
        self.config = CL.ConfigLoader(self.log.write)
        self.log.construct(self.config.LOG_FILE, "Adventure Game Log", "1.0.1", self.config.LOG_LEVEL)
        self.log.write(1, "System Online")
        self.EP = EP.error_printing(self.log)
        self.generate_game = GG.GenerateGame(self.log.write, self.config, self.EP, self.exit_game)
        self.text_display = TD.TextDisplay(self.get_room, self.EP, self.exit_game)
        self.main()

    def main(self):
        self.text_display.render_menu(self.new_game, self.load_game, True)

    def load_game(self):
        self.log.write(1, "Loading Game...")
        self.rooms, self.current_room, self.turns = self.generate_game.load_game()
        if self.current_room == None:
            EP.print_error(37)
            self.exit_game()

        self.get_ending_room()

        self.game_over = False

        self.log.write(0, "Load Successful")
        print("")

        self.game_loop()

    def new_game(self):
        self.log.write(1, "Creating New Game")
        self.turns = 0
        self.rooms = self.generate_game.new_game()

        self.get_starting_room()
        self.get_ending_room()

        self.game_over = False
        self.generate_game.save_game(self.rooms, self.current_room, self.turns)
        self.log.write(0, "New Game Created")
        self.game_loop()

    def get_starting_room(self):
        self.current_room = None
        for r in self.rooms:
            if r.room_type == 1:
                self.current_room = r
                break
        if self.current_room == None:
            EP.print_error(37)
            sys.exit(0)

    def get_ending_room(self):
        self.ending_room = None
        for r in self.rooms:
            if r.room_type == 2:
                self.ending_room = r
                break
        if self.ending_room == None:
            EP.print_error(38)
            sys.exit(0)

    def game_loop(self):
        next_room = self.text_display.print_room(self.current_room)
        self.current_room = self.get_room(next_room)
        self.game_over = self.current_room.room_num == self.ending_room.room_num
        self.turns += 1
        if not self.game_over:
            self.log.write(4, "Moved to {}, {} turn(s) used.".format(self.current_room.name, self.turns))
            self.text_display.move(self.current_room, self.turns)
            self.generate_game.save_game(self.rooms, self.current_room, self.turns)
            return self.game_loop()
        return self.end_game()

    def end_game(self):
        self.log.write(0, "You won in {} turns.".format(self.turns))
        self.exit_game()

    def get_room(self, room_num):
        return self.rooms[room_num]

    def exit_game(self):
        self.log.close()
        print("Have a nice day")
        sys.exit(0)

if __name__ == "__main__":
    main()
