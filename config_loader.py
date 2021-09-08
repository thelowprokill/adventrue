###################################################
#                                                 #
# Program: config_loader                          #
#                                                 #
# Purpose: Loads config file                      #
#                                                 #
# Input:                                          #
#      none:                                      #
#                                                 #
# Output:                                         #
#      none:                                      #
#                                                 #
# Author: Jonathan Hull         Date: 16 Nov 2020 #
#                                                 #
###################################################

from os import path

############################################
#                                          #
# class: config_loader                     #
#                                          #
# Purpose: load a configuration file       #
#                                          #
############################################
class ConfigLoader:
    ############################################
    #                                          #
    # Function: __init__                       #
    #                                          #
    # Purpose: constructor for config_loader   #
    #          class                           #
    #                                          #
    # args:                                    #
    #   self:                                  #
    #   message: function callback to writ to  #
    #            program log file              #
    #                                          #
    # outputs:                                 #
    #   none:                                  #
    #                                          #
    ############################################
    def __init__(self, message):
        self.message           = message
        self.NUM_ROOMS_d       = "6"
        self.MIN_CONNECTIONS_d = "1"
        self.MAX_CONNECTIONS_d = "4"
        self.DEBUG_d           = "0"
        self.LOG_FILE_d        = ".log"
        self.LOG_LEVEL_d       = "1"
        self.SAVE_GAME_d       = ".save_game.dat"
        self.CONFIG_FILE_d     = ".config"
        self.read()

    ############################################
    #                                          #
    # Function: write                          #
    #                                          #
    # Purpose: create a new config file based  #
    #          on default values               #
    #                                          #
    # args:                                    #
    #   self:                                  #
    #                                          #
    # outputs:                                 #
    #   none:                                  #
    #                                          #
    ############################################
    def write(self):
        self.message(0, "config file failed to load. Making new one.")
        config = open(self.CONFIG_FILE_d, "w+")
        config.write("num_rooms       =" + self.NUM_ROOMS_d       + "\n")
        config.write("min_connections =" + self.MIN_CONNECTIONS_d + "\n")
        config.write("max_connections =" + self.MAX_CONNECTIONS_d + "\n")
        config.write("debug           =" + self.DEBUG_d           + "\n")
        config.write("log_file        =" + self.LOG_FILE_d        + "\n")
        config.write("log_level       =" + self.LOG_LEVEL_d       + "\n")
        config.write("save_game       =" + self.SAVE_GAME_d       + "\n")
        config.close()
        self.message(0, "Successfully created new config file.")
        self.read()

    ############################################
    #                                          #
    # Function: read                           #
    #                                          #
    # Purpose: read config file                #
    #                                          #
    # args:                                    #
    #   self:                                  #
    #                                          #
    # outputs:                                 #
    #   none:                                  #
    #                                          #
    ############################################
    def read(self):
        try:
            self.message(1, "Reading config file.")
            config = open(self.CONFIG_FILE_d, "r")
            self.NUM_ROOMS       = int(self.read_config_line(config))
            self.MIN_CONNECTIONS = int(self.read_config_line(config))
            self.MAX_CONNECTIONS = int(self.read_config_line(config))
            self.DEBUG           = self.read_config_line(config) == "1"
            self.LOG_FILE        = self.read_config_line(config)
            self.LOG_LEVEL       = int(self.read_config_line(config))
            self.SAVE_GAME       = self.read_config_line(config)
            config.close()

            self.message(1, "Successfully read config file.")
        except:
            self.write()


    ############################################
    #                                          #
    # Function: read_config_line               #
    #                                          #
    # Purpose: read after '=' in line          #
    #                                          #
    # args:                                    #
    #   fp = file pointer                      #
    #                                          #
    # outputs:                                 #
    #   line                                   #
    #                                          #
    ############################################
    def read_config_line(self, fp):
        line = fp.readline()
        return line[line.rfind("=") + 1:].replace('\n','')

if __name__ == "__main__":
    def message(num, s):
        print(s)
    config = ConfigLoader(message)
    print(config.NUM_ROOMS)
