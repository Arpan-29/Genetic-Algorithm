class Vector :
    def __init__(self, x, y, z = 0) :
        self.x = x
        self.y = y
        self.z = z
        self.mag = (x*x + y*y + z*z) ** 0.5

    def show(self) :
        print(self.x, self.y, self.z)
        print(self.mag)

    def add(self, other) :
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.mag = (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def subtract(self, other) :
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def mult(self, a) :
        self.x *= a
        self.y *= a
        self.z *= a
        self.mag = (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def setMag(self, a) :
        self.x = a * self.x / self.mag
        self.y = a * self.y / self.mag
        self.z = a * self.z / self.mag
        self.mag = a

    def dist(self, other) :
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    def copy(self) :
        return Vector(self.x, self.y, self.z)