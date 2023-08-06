def square(t, size, flag=True):
    for x in range(4):
        t.fd(size)
        if flag:
            t.right(90)
        else:
            t.left(90)


def circle(t, radius):
    t.circle(radius)


def triangle(t, size, flag=True):
    for x in range(3):
        t.fd(size)
        if flag:
            t.right(120)
        else:
            t.left(120)


def star(t, size, flag=True):
    for x in range(5):
        t.fd(size)
        if flag:
            t.right(144)
        else:
            t.left(144)
