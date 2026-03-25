from tkinter import *

# ---------------- WINDOW ----------------
root = Tk()
root.title("Polygon Bounce Game - CGIP")

WIDTH, HEIGHT = 700, 450
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="navy")
canvas.pack()

GROUND = HEIGHT - 20

# ---------------- PIXEL ----------------
def put_pixel(x, y, color):
    canvas.create_rectangle(x, y, x+2, y+2,
                            outline=color,
                            fill=color)

# ---------------- DDA LINE ----------------
def dda(x1, y1, x2, y2, color):

    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))

    if steps == 0:
        put_pixel(x1, y1, color)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1

    for _ in range(steps):
        put_pixel(int(x), int(y), color)
        x += x_inc
        y += y_inc

# ---------------- POLYGON DRAW ----------------
def draw_polygon(points, color):
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % len(points)]
        dda(x1, y1, x2, y2, color)

# ---------------- SCANLINE POLYGON FILL ----------------
def polygon_fill(points, color):

    ymin = int(min(p[1] for p in points))
    ymax = int(max(p[1] for p in points))

    for y_scan in range(ymin, ymax, 2):

        intersections = []

        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i+1) % len(points)]

            if y1 == y2:
                continue

            if min(y1, y2) <= y_scan < max(y1, y2):
                x = x1 + (y_scan - y1) * (x2 - x1) / (y2 - y1)
                intersections.append(int(x))

        intersections.sort()

        for i in range(0, len(intersections), 2):
            if i+1 < len(intersections):
                for x in range(intersections[i],
                               intersections[i+1], 2):
                    put_pixel(x, y_scan, color)

# ---------------- TRANSLATION ----------------
def translate(points, tx, ty):
    return [(px + tx, py + ty) for px, py in points]

# ---------------- RECTANGLE DATA ----------------
x, y = 300, 0
w, h = 120, 70

velocity = 0
gravity = 1.4
bounce_factor = 0.72

compression = 0   # sponge effect

# ---------------- CLICK EVENT ----------------
def on_click(event):
    global velocity

    if x <= event.x <= x+w and y <= event.y <= y+h:
        velocity = -20   # stronger bounce

canvas.bind("<Button-1>", on_click)

# ---------------- ANIMATION ----------------
def animate():
    global x, y, velocity, compression

    canvas.delete("all")

    # ground
    canvas.create_line(0, GROUND, WIDTH, GROUND,
                       fill="white", width=2)

    # ---- GRAVITY ----
    velocity += gravity
    y += velocity

    # ---- BOUNCE + COMPRESSION ----
    if y + h >= GROUND:
        y = GROUND - h

        compression = abs(velocity) * 0.5   # squash
        velocity = -velocity * bounce_factor

        if abs(velocity) < 1:
            velocity = 0
            compression = 0

    else:
        compression = 0

    # ---- CREATE RECTANGLE POLYGON ----
    rect = [
        (x, y + compression),
        (x+w, y + compression),
        (x+w, y+h),
        (x, y+h)
    ]

    # ---- FILL + DRAW ----
    polygon_fill(rect, "pink")
    draw_polygon(rect, "white")

    root.after(12, animate)

# ---------------- START ----------------
animate()
root.mainloop()