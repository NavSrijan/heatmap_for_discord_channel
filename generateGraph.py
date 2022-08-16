import csv
import datetime
import math
from PIL import Image, ImageDraw, ImageFont

# Reading the csv and storing it's time field in a list
with open("15.csv") as csvfile:
    times = []
    reader = csv.reader(csvfile)
    for i in reader:
        times.append(i[2])
    times = times[1:]


def return_datetime_obj(date_str):
    """Returns the datetimeo object from the string."""
    # 14-Aug-22 12:10 AM
    time = datetime.datetime.strptime(date_str, '%d-%b-%y %I:%M %p')
    return (time)


def get_heat_dict(times, am_pm="am"):
    heat = {}
    for i in times:
        i = return_datetime_obj(i)
        if i.date().day == date:
            if am_pm == "am":
                if i.time().hour > 11:
                    break
            if am_pm == "pm":
                if i.time().hour < 12:
                    continue
            try:
                heat[i.time().hour] = heat[i.time().hour] + 1
            except:
                heat[i.time().hour] = 1
    j = 0
    to_add = []
    if len(heat) < 12:
        keys = heat.keys()
        for i in keys:
            if j not in keys:
                to_add.append(j)
            j += 1
        for i in to_add:
            heat[i] = 0

    return heat


def draw_heat(heat):
    colors = [
        '#ffc599', '#ffb780', '#ffa966', '#ff9a4d', '#ff8c33', '#ff7d19',
        '#e66400', '#cc5900', '#b34e00', '#994300', '#803800', '#662c00'
    ]
    font = ImageFont.truetype("B612Mono-Bold", 16)
    im = Image.new('RGBA', (im_size[0], im_size[1]))
    draw = ImageDraw.Draw(im)

    def draw_slice(hour, color):
        start = -90 + 30 * hour
        end = start + 30
        draw.pieslice((0, 0, im_size[0], im_size[1]),
                      start=start,
                      end=end,
                      fill=color)

    def draw_text(hour):
        theta = (30 * hour - 90)
        radius = 250

        s, t = (im_size[0] // 2, 0)

        x = abs(radius * math.sin(theta))
        y = abs(radius * math.cos(theta))
        draw.text((x, y), str(hour), font=font)
        print(hour)
        print(theta)
        print(x, y)
        print("")

    j = 0
    for i in heat:
        if heat[i] != 0:
            draw_slice(i, colors[j])
            j += 1
        else:
            draw_slice(i, "#000000")
    #for i in heat:
    #    draw_text(i)

    return im


date = 15
im_size = (1000, 1000)

heat_am = get_heat_dict(times, am_pm="am")
heat_pm = get_heat_dict(times, am_pm="pm")
sorted_heat_am = {
    k: v
    for k, v in sorted(heat_am.items(), key=lambda item: item[1])
}
sorted_heat_pm = {
    k: v
    for k, v in sorted(heat_pm.items(), key=lambda item: item[1])
}

am = draw_heat(sorted_heat_am)
pm = draw_heat(sorted_heat_pm)

extra_x = 100
extra_y = 50

im = Image.new('RGBA', (im_size[0] * 2 + extra_x, im_size[1] + extra_y))
im.paste(am, box=(extra_x // 3, extra_y // 2))
im.paste(pm, box=(extra_x // 3 * 2 + im_size[0], extra_y // 2))

im.show()
im.save("img.png")
