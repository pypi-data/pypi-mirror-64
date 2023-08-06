import turtle

turtle.tracer(0)


def square(t, size, flag=True):
    for x in range(4):
        t.fd(size)
        if flag:
            t.right(90)
        else:
            t.left(90)
    turtle.update()


def circle(t, radius):
    t.circle(radius)
    turtle.update()