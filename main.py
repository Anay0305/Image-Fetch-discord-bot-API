from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
from datetime import datetime
import requests

app = Flask(__name__)

def converttime1(seconds):
    if seconds == 0:
        return "0 hours"
    time = int(seconds)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    ls = []
    if hour != 0:
        if hour == 1:
            x = "hour"
        else:
            x = "hours"
        ls.append(f"{hour} {x}")
    if minutes != 0:
        if minutes == 1:
            x = "min"
        else:
            x = "mins"
        ls.append(f"{minutes} {x}")
    if len(ls) == 0:
        if seconds != 0:
            ls.append(f"{seconds} seconds")
    return ' '.join(ls)

def converttime(seconds):
    time = int(seconds)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    ls = []
    if hour != 0:
        ls.append(f"{hour}hrs")
    if minutes != 0:
        ls.append(f"{minutes}mins")
    if seconds != 0:
        ls.append(f"{seconds}secs")
    return ' '.join(ls)

def lb_(icon, name, guild_id, banner, requester, mode:str, typee:str, data, current, total, start_date, end_date=None):
    width = 960
    height = 500
    if end_date is None:
        end_date = str(datetime.now().date())

    if not banner:
        with open("Images/bg.jpg", 'rb') as file:
            image = Image.open(BytesIO(file.read())).convert("RGBA")
            file.close()
        image = image.resize((width,height))
    else:
        _res = requests.get(banner)
        image = Image.open(BytesIO(_res.content)).convert("RGBA")
        image = image.resize((width,height))
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
        brightness_factor = 0.5
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness_factor)
    draw = ImageDraw.Draw(image)
    with open("Images/mask.jpg", 'rb') as file:
        imagee = Image.open(BytesIO(file.read())).convert("RGBA")
        file.close()
    imagee = imagee.resize((width,height))
    image.paste(imagee, (0, 0), mask=imagee)
    logo_res = requests.get(icon)
    AVATAR_SIZE = 83
    avatar_image = Image.open(BytesIO(logo_res.content)).convert("RGB")
    avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) #
    border_radius = 23
    mask = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, AVATAR_SIZE, AVATAR_SIZE), radius=border_radius, fill=255)
    image.paste(avatar_image, (53, 31), mask)
    font = ImageFont.truetype('Fonts/Montserrat-Bold.ttf', 24)
    n = name
    while font.getlength(name) >= 415:
      name = name[0:-1]
    if n != name:
      name = name[0:-2] + "..."
    draw.text( (150, 42), f"{name}", fill="white", font=font)
    draw.text( (150, 74), f"ID: {guild_id}", fill="white", font=font)
    if start_date == end_date:
        if start_date == str(datetime.now().date()):
            hm = f"Today: {start_date}"
        else:
            hm = start_date
    else:
        hm = f"{start_date} to {end_date}"
    if mode.lower() == "messages":
        if typee.lower() == "users":
            xd = "User Messages"
        else:
            xd = "Text Channels"
    else:
        if typee.lower() == "users":
            xd = "Voice Users"
        else:
            xd = "Voice Channels"
    font = ImageFont.truetype('Fonts/Montserrat-Bold.ttf', 21)
    draw.text( (580, 42), f"{xd} LeaderBoard", fill="white", font=font)
    font = ImageFont.truetype('Fonts/Montserrat-SemiBold.ttf', 21)
    draw.text( (580, 74), hm, fill="white", font=font)
    font = ImageFont.truetype('Fonts/Montserrat-SemiBold.ttf', 20)
    draw.text( (45, 476), f"Requested By {str(requester)}", fill="white", font=font, anchor="lm")
    font = ImageFont.truetype('Fonts/Montserrat-Bold.ttf', 20)
    draw.text( (915, 476), f"Powered By Gateway", fill="white", font=font, anchor="rm")
    font = ImageFont.truetype('Fonts/Montserrat-Medium.ttf', 18)
    draw.text( (915, 14), f"Page {current}/{total}", fill="white", font=font, anchor="rm")
    ls = [
        139, 205, 271, 338, 404
    ]
    ls1 = [
        139+26, 205+26, 271+26, 338+26, 404+26
    ]
    c = 0
    for i in data:
        c+=1
        logo_res = requests.get(data[i][2])
        AVATAR_SIZE = 52
        try:
            avatar_image = Image.open(BytesIO(logo_res.content)).convert("RGB")
        except:
            print(data[i][2])
            logo_res = requests.get("https://cdn.discordapp.com/avatars/880765863953858601/2fa5ec0d3cc8d354bf51833543d5074a.png?size=1024")
            avatar_image = Image.open(BytesIO(logo_res.content)).convert("RGB")
        avatar_image = avatar_image.resize((int(AVATAR_SIZE), int(AVATAR_SIZE)))
        mask = Image.new('L', (int(AVATAR_SIZE), int(AVATAR_SIZE)), 0)
        circle_draw = ImageDraw.Draw(mask)
        circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
        num_font = ImageFont.truetype('Fonts/Montserrat-Bold.ttf', 20)
        font = ImageFont.truetype('Fonts/Montserrat-Medium.ttf', 18)
        n = i
        while font.getlength(n) >= 320 - num_font.getlength(f"{data[i][1]}. "):
            n = n[0:-1]
        if n != i:
            n = n[0:-2] + "..."
        if c % 2 != 0:
            image.paste(avatar_image, (53, ls[int((c-1)/2)]), mask)
            draw.text( (130, ls1[int((c-1)/2)]), f"{data[i][1]}. ", fill=(255,255,255), font=num_font, anchor="lm")
            draw.text( (135 + num_font.getlength(f"{data[i][1]}. "), ls1[int((c-1)/2)]), f"{n}\n{data[i][0]}", fill=(255,255,255), font=font, anchor="lm")
        else:
            image.paste(avatar_image, (500, ls[int((c-1)/2)]), mask)
            draw.text( (130+447, ls1[int((c-1)/2)]), f"{data[i][1]}. ", fill=(255,255,255), font=num_font, anchor="lm")
            draw.text( (135+447 + num_font.getlength(f"{data[i][1]}. "), ls1[int((c-1)/2)]), f"{n}\n{data[i][0]}", fill=(255,255,255), font=font, anchor="lm")

    image_binary = BytesIO()
    image.save(image_binary, 'PNG')
    image_binary.seek(0)

    return image_binary
    
def server_top(guild_id, guild_name, icon, mem_ids, chan_ids, data, guild_banner=None):
    width = 1033
    height = 502
    banner = guild_banner
    if not banner:
        with open("Images/bg.jpg", 'rb') as file:
            image = Image.open(BytesIO(file.read())).convert("RGBA")
            file.close()
        image = image.resize((width, height))
    else:
        _res = requests.get(banner)
        image = Image.open(BytesIO(_res.content)).convert("RGBA")
        image = image.resize((width, height))
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
        brightness_factor = 0.5
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness_factor)
    draw = ImageDraw.Draw(image)
    with open("Images/server_stats_mask.png", 'rb') as file:
        imagee = Image.open(BytesIO(file.read())).convert("RGBA")
        file.close()
    imagee = imagee.resize((width, height))
    image.paste(imagee, (0, 0), mask=imagee)
    logo_res = requests.get(icon)
    AVATAR_SIZE = 72
    avatar_image = Image.open(BytesIO(logo_res.content)).convert("RGB")
    avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) #
    border_radius = 20
    mask = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, AVATAR_SIZE, AVATAR_SIZE), radius=border_radius, fill=255)
    image.paste(avatar_image, (18, 23), mask)
    font = ImageFont.truetype('Fonts/Montserrat-Bold.ttf', 26)
    name = guild_name
    n = name
    while font.getlength(name) >= 415:
      name = name[0:-1]
    if n != name:
      name = name[0:-2] + "..."
    draw.text( (105, 46), f"{name}", fill="white", font=font, anchor="lm")
    font = ImageFont.truetype('Fonts/Montserrat-Regular.ttf', 17)
    font = ImageFont.truetype('Fonts/Montserrat-MediumItalic.ttf', 16)
    draw.text( (888, 66), f"Server Lookback Last {data['lookback']} days\n~ TimeZone: UTC", fill="white", font=font, anchor="mm")
    font = ImageFont.truetype('Fonts/Montserrat-SemiBold.ttf', 24)
    x_cords = [60, 399, 736]
    x_cords1 = [100, 438, 776]
    y_cords = [166, 210, 254]
    font1 = ImageFont.truetype('Fonts/Montserrat-Medium.ttf', 22)
    msgs = data['messages']
    while len(msgs) < 3:
        msgs.append(msgs[-1])
    coun = 0
    for i in msgs:
        draw.text( (x_cords[0], y_cords[coun]), f"{i[0]}d", fill="white", font=font, anchor="mm")
        draw.text( (x_cords1[0], y_cords[coun]), f"{i[1]} Messages", fill="white", font=font1, anchor="lm")
        coun +=1
    voice = data['voice']
    if len(voice) == 0:
        for i in msgs:
            voice.append((i, "0 hours"))
    else:
        while len(voice) < 3:
            voice.append(voice[-1])
    coun = 0
    for i in voice:
        draw.text( (x_cords[1], y_cords[coun]), f"{i[0]}d", fill="white", font=font, anchor="mm")
        if i[1] == "":
            draw.text( (x_cords1[1], y_cords[coun]), f"0 hours", fill="white", font=font1, anchor="lm")
        else:
            draw.text( (x_cords1[1], y_cords[coun]), f"{i[1]}", fill="white", font=font1, anchor="lm")
        coun +=1
    contri = data['contributors']
    while len(contri) < 3:
        contri.append(contri[-1])
    coun = 0
    for i in contri:
        draw.text( (x_cords[2], y_cords[coun]), f"{i[0]}d", fill="white", font=font, anchor="mm")
        draw.text( (x_cords1[2], y_cords[coun]), f"{i[1]} Members", fill="white", font=font1, anchor="lm")
        coun +=1
    font = ImageFont.truetype('Fonts/Montserrat-Medium.ttf', 22)
    name_font = ImageFont.truetype('Fonts/Montserrat-MediumItalic.ttf', 24)
    for i in data['top_member_text']:
        if i[0] in mem_ids:
            name = i[1]['display_name']
            n = name
            while name_font.getlength(name) >= 140:
                name = name[0:-1]
            if n != name:
                name = name[0:-2] + "..."
            draw.text( (164, 372), f"{name}", fill="white", font=name_font, anchor="mm")
            draw.text( (248, 372), f"{i[1]['count']} Messages", fill="white", font=font, anchor="lm")
            break
    for i in data['top_member_vc']:
        if i[0] in mem_ids:
            name = i[1]['display_name']
            n = name
            while name_font.getlength(name) >= 140:
                name = name[0:-1]
            if n != name:
                name = name[0:-2] + "..."
            draw.text( (164, 438), f"{name}", fill="white", font=name_font, anchor="mm")
            draw.text( (248, 438), f"{converttime1(i[1]['time'])}", fill="white", font=font, anchor="lm")
            break
    for i in data['top_channel_text']:
        if i[0] in chan_ids:
            name = i[1]['name']
            n = name
            while name_font.getlength(name) >= 128:
                name = name[0:-1]
            if n != name:
                name = name[0:-2] + "..."
            draw.text( (666, 372), f"{name}", fill="white", font=name_font, anchor="mm")
            draw.text( (740, 372), f"{i[1]['count']} Messages", fill="white", font=font, anchor="lm")
            break
    for i in data['top_channel_vc']:
        if i[0] in chan_ids:
            name = i[1]['name']
            n = name
            while name_font.getlength(name) >= 128:
                name = name[0:-1]
            if n != name:
                name = name[0:-2] + "..."
            draw.text( (666, 438), f"{name}", fill="white", font=name_font, anchor="mm")
            draw.text( (740, 438), f"{converttime1(i[1]['time'])}", fill="white", font=font, anchor="lm")
            break
    
    image_binary = BytesIO()
    image.save(image_binary, 'PNG')
    image_binary.seek(0)

    return image_binary

@app.route('/leaderboard', methods=['POST'])
def generate_leaderboard():
    data = request.json
    guild_icon = data.get('guild_icon')
    guild_name = data.get('guild_name')
    guild_id = data.get('guild_id')
    guild_banner = data.get('guild_banner')
    requester = data.get('requester')
    mode = data.get('mode')
    typee = data.get('type')
    xd = data.get('data')
    current = data.get('current')
    total = data.get('total')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    result = lb_(guild_icon, guild_name, guild_id, guild_banner, requester, mode, typee, xd, current, total, start_date, end_date)

    return send_file(result, mimetype='image/png')

@app.route('/server_top', methods=['POST'])
def generate_server_top():
    data = request.json
    guild_id = data.get('guild_id')
    guild_name = data.get('guild_name')
    icon = data.get('icon')
    mem_ids = data.get('mem_ids')
    chan_ids = data.get('chan_ids')
    xd = data.get('data')
    guild_banner = data.get('guild_banner')

    result = server_top(guild_id, guild_name, icon, mem_ids, chan_ids, xd, guild_banner)

    return send_file(result, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)