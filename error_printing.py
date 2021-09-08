class error_printing:
    def __init__(self, log):
        self.log = log

    def print_error(self, code, detail = ""):
        string = "Error "
        if code == 1:
            string +="1: Failed to read save game: {}".format(detail)
        elif code == 37:
            string +="{}: No starting room, Game terminating".format(code)
        elif code == 38:
            string +="{}: No ending room, Game terminating".format(code)
        elif code == 42:
            string +="{}: Unkown integer input: {}".format(code, detail)
        elif code == 43:
            string += "{}: Unkown string input: {}".format(code, detail)
        else:
            string += "16384: Unkown Error code: {}, detail: {}".format(code, detail)

        self.log.write(0, string)
