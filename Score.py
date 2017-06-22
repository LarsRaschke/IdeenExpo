class Score:
    def __init__(self, data="/home/pi/Public/aktuell/scoreBoard.txt"):
        self.data = data
        self.ranked = []
        self.load()

    def load(self):
        self.ranked = []
        fob = open(self.data, "r+")
        lines = fob.readlines()[:4]
        for line in lines:
            tmp = line.rstrip().split(":")
            points = eval(tmp[1][:6])
            name = tmp[2].strip()
            tmp = [points, name]
            self.ranked.append(tmp)
        fob.close()
        self.ranked.sort(reverse=True)

    def save(self):
        fob = open(self.data, "r+")
        place = 1
        self.ranked.sort(reverse=True)
        p1 = self.ranked[0]
        p2 = self.ranked[1]
        p3 = self.ranked[2]
        last = self.ranked[3]
        fob.write(str(place) + "1. Punkte: " + str(p1[0]) + " Name: " + str(p1[1] + "\n"))
        fob.write(str(place) + "2. Punkte: " + str(p2[0]) + " Name: " + str(p2[1] + "\n"))
        fob.write(str(place) + "3. Punkte: " + str(p3[0]) + " Name: " + str(p3[1] + "\n"))
        fob.write(str(place) + "Lastplayer Punkte: " + str(last[0]) + " Name: " + str(last[1] + "\n"))

    def add(self, points=0.0, name=" Expo"):
        self.ranked.append([points, name])
        self.ranked.sort(reverse=True)

    def show(self):
        return self.ranked


s = Score()
