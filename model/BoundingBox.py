class BoundingBox:
    def __init__(self, point1='', point2='', object_class='', img_name=''):
        self.point1 = point1
        self.point2 = point2
        self.object_class = object_class
        self.img_name = img_name

    def __str__(self):
        return self.point1 + " - " + self.point2 + ", class=" + self.object_class
