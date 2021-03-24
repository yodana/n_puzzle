import sys

class Game:
    def __init__(self, file):
        self.file = file;
        self.taquin = self.__create_taquin();

    def __create_taquin(self):
        ZONE = "";
        LIST = [];
        for line in self.file.readlines():
            line = line.replace('\n', '');
            i = line.find('#');
            if (i >= 0):
                line = line[0:i];
            if line:
                ZONE = ZONE + line + " ";
        LIST = ZONE.split();
        self.size = int(LIST[0]);
        taquin = [[0] * self.size for i in range(self.size)];
        k = 1;
        for i in range(0, self.size):
            for j in range(0, self.size):
                taquin[i][j] = LIST[k];
                k = k + 1;    
        return taquin

if (len(sys.argv) < 2):
    print("Need a file with a n_puzzle inside.");
    sys.exit(1);

f = open(sys.argv[1], "r");
game = Game(f);
print(game.taquin);
for arg in sys.argv:
    print(arg);