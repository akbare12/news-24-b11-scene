import os
from PIL import Image, ImageDraw, ImageFont
W, H = 1024, 1024
PAPER = (247, 242, 231); INK = (17, 17, 17); RED = (176, 30, 36); NAVY = (27, 42, 74); GREY = (110, 110, 105); LGREY = (224, 219, 208)
GREEN = (46, 125, 50); BLUE = (21, 101, 192); ORANGE = (230, 81, 0); GOLD = (176, 141, 0); TEAL = (0, 121, 107); PURPLE = (106, 27, 154); SKY = (135, 180, 220); NIGHT = (18, 28, 52)
def F(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_kick = F(SANSB, 11); f_mast = F(SERIF, 34); f_sub = F(SERIF, 13); f_reg = F(SANSB, 10); f_time = F(SANSB, 11); f_num = F(SERIF, 20); f_lab = F(SANS, 9)
f_hkick = F(SANSB, 10); f_hhead = F(SERIF, 15); f_hdeck = F(SANS, 10); f_chip = F(SANSB, 8); f_ckick = F(SANSB, 8); f_chead = F(SANSB, 10)
f_cdeck = F(SANS, 9); f_also = F(SANS, 9); f_dc = F(SANS, 10); f_foot = F(SANS, 9); f_mapt = F(SANSB, 11); f_pin = F(SANSB, 8)
def lines(s, font, w):
    out = []; cur = ""
    for wd in s.split(" "):
        t = (cur + " " + wd).strip()
        if font.getlength(t) <= w: cur = t
        else:
            if cur: out.append(cur)
            cur = wd
    if cur: out.append(cur)
    return out
def txt(d, x, y, s, font, fill=INK, w=300, lh=None, maxl=99):
    lh = lh or int(font.size * 1.28); ls = lines(s, font, w)[:maxl]
    for i, ln in enumerate(ls): d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(ls) * lh
CHIPCOL = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": (90, 90, 90), "CLAIM": ORANGE, "ONGOING": GOLD}
def chip(d, x, y, label):
    c = CHIPCOL[label]; wdt = int(f_chip.getlength(label)) + 10
    d.rounded_rectangle([x, y, x + wdt, y + 13], 2, fill=c); d.text((x + 5, y + 2), label, font=f_chip, fill=(255, 255, 255)); return x + wdt + 4
# world map: real lat/lon outlines, equirectangular
NA = [(-168,66),(-140,70),(-125,71),(-110,68),(-95,69),(-85,66),(-80,73),(-70,62),(-60,55),(-55,47),(-65,44),(-70,42),(-75,35),(-80,32),(-81,26),(-84,30),(-90,29),(-97,26),(-97,16),(-94,16),(-90,14),(-83,9),(-79,9),(-83,15),(-87,13),(-92,15),(-97,16),(-105,20),(-110,23),(-114,28),(-117,33),(-124,40),(-124,48),(-130,55),(-140,60),(-155,58),(-165,60)]
SA = [(-79,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),(-72,-37),(-73,-44),(-74,-52),(-68,-55),(-65,-45),(-62,-40),(-57,-38),(-52,-33),(-48,-28),(-41,-23),(-35,-9),(-35,-6),(-40,-3),(-44,-2),(-50,0),(-53,4),(-58,6),(-62,9),(-68,11),(-72,12),(-77,8)]
AF = [(-6,35),(-10,31),(-15,27),(-17,21),(-17,15),(-15,11),(-12,8),(-8,5),(-4,5),(0,6),(6,4),(9,4),(9,-1),(12,-5),(13,-12),(12,-18),(14,-22),(16,-28),(19,-34),(26,-34),(32,-29),(35,-24),(40,-16),(40,-10),(42,-4),(46,-1),(51,2),(51,11),(44,11),(43,12),(40,15),(38,18),(37,22),(34,27),(32,31),(30,32),(22,33),(19,33),(11,34),(10,37),(5,37),(-1,35)]
EU = [(-10,36),(-9,43),(-2,44),(-1,46),(-4,48),(-1,49),(2,51),(5,53),(8,57),(10,59),(6,61),(10,62),(14,66),(18,69),(25,71),(30,70),(35,68),(40,67),(45,68),(52,69),(58,69),(66,69),(70,68),(60,66),(52,64),(45,62),(40,60),(35,58),(30,60),(25,59),(20,58),(15,56),(10,57),(5,58),(2,55),(0,52),(-5,50),(-8,48),(-10,44),(-10,38)]
AS = [(-10,36),(30,36),(33,36),(36,36),(36,31),(35,29),(36,28),(39,21),(40,18),(42,15),(44,13),(48,14),(52,16),(55,17),(58,19),(59,22),(57,21),(56,24),(54,26),(52,25),(50,29),(48,30),(50,26),(54,24),(56,26),(58,25),(61,25),(64,25),(67,24),(70,22),(72,20),(74,14),(76,9),(78,8),(80,13),(83,18),(86,20),(88,22),(90,22),(92,21),(95,16),(97,12),(99,9),(101,7),(104,8),(106,10),(108,18),(112,22),(118,25),(121,28),(122,31),(120,35),(124,38),(127,40),(130,42),(135,43),(140,45),(140,52),(142,59),(150,59),(156,51),(158,52),(162,56),(170,60),(173,64),(178,65),(170,66),(165,66),(158,69),(150,70),(142,72),(135,71),(128,71),(120,73),(112,74),(105,77),(95,76),(85,75),(78,73),(72,72),(66,70),(58,69),(52,69),(45,68),(40,67),(35,68),(30,70),(25,71),(18,69),(14,66),(10,62),(6,61),(10,59),(8,57),(5,53),(2,51),(-1,49),(-4,48),(-1,46),(-2,44),(-9,43),(-10,36)]
AU = [(113,-22),(114,-30),(115,-35),(120,-34),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-23),(146,-19),(142,-15),(142,-11),(137,-12),(135,-15),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20),(114,-22)]
UK = [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51),(-3,50)]; JP = [(130,31),(132,33),(135,34),(137,35),(139,35),(140,38),(141,41),(143,42),(141,44),(140,40),(137,37),(133,35),(130,33)]
BO = [(109,1),(111,2),(114,3),(117,1),(118,-1),(116,-3),(113,-4),(110,-3)]; SU = [(95,5),(98,3),(101,0),(103,-2),(105,-4),(106,-6),(104,-5),(101,-1),(98,2)]
NG = [(131,-1),(136,-2),(141,-3),(146,-6),(150,-8),(147,-9),(143,-8),(138,-7),(134,-4),(131,-2)]; MD = [(44,-16),(47,-15),(50,-16),(49,-20),(47,-24),(45,-25),(43,-22),(43,-18)]
CONT = [NA, SA, AF, EU, AS, AU, UK, JP, BO, SU, NG, MD]

# scene painters: d, box(x0,y0,x1,y1), kind
def scene(d, x0, y0, x1, y1, kind):
    w, h = x1 - x0, y1 - y0
    if kind == "riyadh":
        d.rectangle([x0, y0, x1, y1], fill=NIGHT)
        for sx, sy in [(x0+30, y0+12), (x0+90, y0+22), (x0+180, y0+10), (x0+250, y0+20), (x0+300, y0+14)]: d.ellipse([sx, sy, sx+2, sy+2], fill=(255, 255, 255))
        for i, bh in enumerate([34, 48, 30, 42, 36, 52, 28]):
            bx = x0 + 8 + i * 30; d.rectangle([bx, y1 - bh, bx + 24, y1], fill=(52, 68, 104))
            for wy in range(y1 - bh + 5, y1 - 4, 9):
                for wx in range(bx + 4, bx + 20, 7): d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        tx = x0 + w // 2 - 14; d.polygon([(tx, y0 + 8), (tx + 10, y0 + 18), (tx + 28, y0 + 18), (tx + 18, y0 + 8)], fill=(70, 90, 130)); d.rectangle([tx + 2, y0 + 18, tx + 26, y1], fill=(88, 112, 152)); d.rectangle([tx + 2, y0 + 18, tx + 26, y1], outline=(200, 210, 225))
        for wy in range(y0 + 24, y1 - 4, 10):
            for wx in range(tx + 6, tx + 22, 7): d.rectangle([wx, wy, wx + 3, wy + 5], fill=(255, 230, 150))
        d.ellipse([x0 + w - 78, y0 + 22, x0 + w - 38, y0 + 62], fill=(255, 120, 40)); d.ellipse([x0 + w - 70, y0 + 30, x0 + w - 46, y0 + 54], fill=(255, 200, 80)); d.ellipse([x0 + w - 95, y0 + 8, x0 + w - 55, y0 + 38], fill=(120, 120, 120)); d.ellipse([x0 + w - 85, y0 + 2, x0 + w - 50, y0 + 28], fill=(150, 150, 150))
        dx, dy = x0 + 42, y0 + 26; d.rectangle([dx - 8, dy, dx + 8, dy + 3], fill=(30, 30, 30)); d.line([dx, dy, dx, dy - 8], fill=(200, 200, 200), width=1); d.ellipse([dx - 9, dy - 11, dx - 5, dy - 7], fill=(200, 200, 200)); d.ellipse([dx + 5, dy - 11, dx + 9, dy - 7], fill=(200, 200, 200))
    elif kind == "chen":
        d.rectangle([x0, y0, x1, y1], fill=(196, 30, 30)); d.rectangle([x0, y0 + h - 26, x1, y1], fill=(120, 20, 20)); d.rectangle([x0 + 18, y0 + 14, x1 - 18, y0 + 58], fill=(240, 235, 220))
        for cx in range(x0 + 30, x1 - 24, 26): d.rectangle([cx, y0 + 20, cx + 8, y0 + 52], fill=(150, 30, 30))
        d.polygon([(x0 + 10, y0 + 14), (x0 + w // 2, y0 - 2), (x1 - 10, y0 + 14)], fill=(140, 25, 25)); d.ellipse([x0 + w // 2 - 9, y0 + 2, x0 + w // 2 + 9, y0 + 20], fill=(255, 210, 60))
        px, py = x0 + w - 96, y0 + h - 44; d.polygon([(px, py + 16), (px + 66, py), (px + 76, py + 26), (px + 10, py + 40)], fill=(255, 255, 255)); d.polygon([(px, py + 16), (px + 66, py), (px + 76, py + 26), (px + 10, py + 40)], outline=(120, 120, 120))
        for i in range(4): d.line([px + 8, py + 8 + i * 6, px + 58, py - 2 + i * 6], fill=(60, 60, 60), width=1)
        d.ellipse([px + 52, py + 20, px + 66, py + 34], fill=(176, 30, 36)); d.text((px + 55, py + 23), "CCD", font=f_pin, fill=(255, 255, 255)); d.text((x0 + 14, y0 + h - 20), "SHANGHAI  ·  INVESTIGATION", font=f_pin, fill=(255, 220, 120))
    elif kind == "huawei":
        d.rectangle([x0, y0, x1, y1], fill=(200, 215, 230)); d.rectangle([x0, y0 + h - 18, x1, y1], fill=(120, 130, 140)); d.polygon([(x0 + 30, y0 + 34), (x0 + w // 2, y0 + 8), (x1 - 30, y0 + 34)], fill=(70, 80, 95)); d.ellipse([x0 + w // 2 - 8, y0 + 16, x0 + w // 2 + 8, y0 + 32], fill=(255, 255, 255))
        for cx in range(x0 + 44, x1 - 50, 30): d.rectangle([cx, y0 + 36, cx + 10, y0 + 72], fill=(240, 240, 240))
        d.rectangle([x0 + 30, y0 + 72, x1 - 30, y0 + 78], fill=(70, 80, 95)); gx, gy = x0 + w - 82, y0 + h - 34; d.line([gx, gy, gx + 52, gy - 6], fill=(120, 80, 30), width=4); d.rectangle([gx + 22, gy, gx + 30, gy + 8], fill=(120, 80, 30)); d.rectangle([x0 + 16, y0 + h - 30, x0 + 96, y0 + h - 12], fill=(176, 30, 36)); d.text((x0 + 22, y0 + h - 28), "HUAWEI", font=f_pin, fill=(255, 255, 255)); d.text((x0 + w - 60, y0 + 12), "10 / 12", font=F(SANSB, 14), fill=RED)
    elif kind == "war":
        d.rectangle([x0, y0, x1, y1], fill=NIGHT); d.rectangle([x0 + 20, y1 - 12, x0 + 70, y1], fill=(60, 60, 70)); d.rectangle([x0 + 90, y1 - 18, x0 + 150, y1], fill=(70, 60, 60)); d.ellipse([x0 + 120, y0 + 4, x0 + 150, y0 + 22], fill=(255, 140, 40)); d.ellipse([x0 + 128, y0 + 9, x0 + 142, y0 + 17], fill=(255, 210, 100))
        for dx, dy in [(x0 + 30, y0 + 8), (x0 + 80, y0 + 14), (x0 + 160, y0 + 6)]: d.rectangle([dx - 5, dy, dx + 5, dy + 2], fill=(220, 220, 220))
    elif kind == "trophy":
        d.rectangle([x0, y0, x1, y1], fill=(20, 90, 60)); cx = x0 + w // 2; d.polygon([(cx - 16, y0 + 4), (cx + 16, y0 + 4), (cx + 10, y0 + 18), (cx - 10, y0 + 18)], fill=(255, 200, 40)); d.rectangle([cx - 3, y0 + 18, cx + 3, y0 + 24], fill=(255, 200, 40)); d.rectangle([cx - 10, y0 + 24, cx + 10, y0 + 27], fill=(255, 200, 40)); d.rectangle([x0 + 8, y1 - 8, x0 + 30, y1 - 2], fill=(0, 120, 60)); d.rectangle([x1 - 30, y1 - 8, x1 - 8, y1 - 2], fill=(200, 30, 30))
    elif kind == "ship":
        d.rectangle([x0, y0, x1, y1], fill=(90, 160, 210)); d.rectangle([x0, y0 + h - 10, x1, y1], fill=(30, 90, 140)); d.rectangle([x0 + 20, y0 + 12, x0 + w - 20, y0 + 22], fill=(40, 50, 60))
        for i, c in enumerate([(200, 60, 40), (240, 180, 40), (40, 120, 200), (220, 120, 40)]): d.rectangle([x0 + 24 + i * 30, y0 + 6, x0 + 50 + i * 30, y0 + 12], fill=c)
        d.rectangle([x1 - 46, y0 + 4, x1 - 30, y0 + 12], fill=(230, 230, 230)); d.ellipse([x0 + w // 2 - 14, y0 + 2, x0 + w // 2 + 14, y0 + 14], fill=(255, 150, 50))
    elif kind == "chart":
        d.rectangle([x0, y0, x1, y1], fill=(245, 245, 240)); d.line([x0 + 8, y0 + h - 12, x1 - 8, y0 + h - 12], fill=(150, 150, 150)); d.line([x0 + 8, y0 + 8, x0 + 30, y0 + 12, x0 + 60, y0 + 10, x0 + 95, y0 + 16, x0 + 130, y0 + 10, x0 + 165, y0 + 4], fill=RED, width=2); d.line([x0 + 8, y0 + 14, x1 - 8, y0 + 14], fill=(180, 180, 180)); d.text((x0 + 6, y0 + 16), "50,000", font=f_pin, fill=RED)
    elif kind == "data":
        d.rectangle([x0, y0, x1, y1], fill=(30, 34, 44))
        for i in range(4):
            bx = x0 + 10 + i * 44; d.rectangle([bx, y0 + 4, bx + 36, y1 - 4], fill=(60, 68, 84))
            for r in range(3): d.rectangle([bx + 4, y0 + 7 + r * 8, bx + 32, y0 + 12 + r * 8], fill=(120, 200, 120) if r != 1 else (255, 80, 60))
        d.text((x0 + w - 52, y0 + 2), "CODE RED", font=f_pin, fill=(255, 80, 60))
    elif kind == "heli":
        d.rectangle([x0, y0, x1, y1], fill=SKY); d.polygon([(x0, y1), (x0 + 60, y0 + 14), (x0 + 120, y1)], fill=(110, 130, 110)); d.polygon([(x0 + 90, y1), (x0 + 150, y0 + 18), (x1, y1)], fill=(90, 110, 95)); hx, hy = x0 + w // 2, y0 + 10; d.ellipse([hx - 16, hy, hx + 16, hy + 10], fill=(60, 70, 60)); d.line([hx + 16, hy + 4, hx + 40, hy + 2], fill=(60, 70, 60), width=2); d.line([hx - 22, hy - 2, hx + 22, hy - 2], fill=(40, 40, 40), width=2); d.line([hx, hy + 10, hx, hy + 16], fill=(60, 70, 60), width=2)
    elif kind == "market":
        d.rectangle([x0, y0, x1, y1], fill=(230, 225, 210)); d.rectangle([x0 + 14, y0 + 10, x1 - 14, y1 - 6], fill=(250, 250, 245)); d.rectangle([x0 + 14, y0 + 10, x1 - 14, y0 + 16], fill=RED); d.text((x0 + 20, y0 + 11), "SUPERMARKET", font=f_pin, fill=(255, 255, 255))
        for i in range(4): d.rectangle([x0 + 22 + i * 40, y0 + 20, x0 + 52 + i * 40, y1 - 6], fill=(150, 180, 210))
    elif kind == "desert":
        d.rectangle([x0, y0, x1, y1], fill=(240, 210, 150)); d.ellipse([x0 + w - 34, y0 + 2, x0 + w - 14, y0 + 22], fill=(255, 200, 80)); d.polygon([(x0, y1), (x0 + 50, y0 + 16), (x0 + 110, y1)], fill=(200, 160, 100)); d.polygon([(x0 + 80, y1), (x0 + 140, y0 + 20), (x1, y1)], fill=(180, 140, 85)); d.polygon([(x0 + 20, y0 + 20), (x0 + 40, y0 + 20), (x0 + 30, y0 + 12)], fill=RED); d.polygon([(x0 + 60, y0 + 22), (x0 + 80, y0 + 22), (x0 + 70, y0 + 14)], fill=RED)
    elif kind == "strike":
        d.rectangle([x0, y0, x1, y1], fill=(210, 190, 160)); d.rectangle([x0, y0 + h - 8, x1, y1], fill=(90, 90, 90)); d.rectangle([x0 + 30, y0 + 14, x0 + 90, y0 + 22], fill=(200, 60, 40)); d.rectangle([x0 + 100, y0 + 16, x0 + 140, y0 + 22], fill=(60, 60, 60)); d.ellipse([x0 + w // 2 - 12, y0 + 2, x0 + w // 2 + 12, y0 + 18], fill=(255, 140, 40)); d.ellipse([x0 + w // 2 - 6, y0 + 6, x0 + w // 2 + 6, y0 + 14], fill=(255, 210, 100))
    else:  # rocket
        d.rectangle([x0, y0, x1, y1], fill=NIGHT)
        for sx, sy in [(x0 + 20, y0 + 6), (x0 + 70, y0 + 12), (x0 + 140, y0 + 8), (x0 + 170, y0 + 16)]: d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        cx = x0 + w // 2; d.polygon([(cx, y0 + 4), (cx + 8, y0 + 14), (cx + 8, y0 + 24), (cx, y0 + 30), (cx - 8, y0 + 24), (cx - 8, y0 + 14)], fill=(240, 240, 240)); d.polygon([(cx - 8, y0 + 20), (cx - 14, y0 + 28), (cx - 8, y0 + 26)], fill=RED); d.polygon([(cx + 8, y0 + 20), (cx + 14, y0 + 28), (cx + 8, y0 + 26)], fill=RED); d.polygon([(cx - 4, y0 + 28), (cx + 4, y0 + 28), (cx, y1 - 2)], fill=(255, 160, 40))

# --- page ---
img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 4], fill=RED); d.text((20, 10), "THE WORLD ON ONE DAY", font=f_kick, fill=RED)
rt = "38 STORIES  ·  7 REGIONS  ·  13 FIELDS  ·  ALL FROM TUESDAY 24 NOVEMBER 2026"; d.text((W - 20 - f_kick.getlength(rt), 10), rt, font=f_kick, fill=INK)
d.line([20, 28, W - 20, 28], fill=INK, width=2); d.text((20, 32), "Tuesday 24 November 2026", font=f_mast, fill=INK)
d.text((20, 70), "Houthi drone hits Riyadh's tallest tower  ·  China probes Shanghai party chief  ·  Huawei guilty on 10 of 12 counts", font=f_sub, fill=RED)
REG = [("EUROPE", 7, GREEN), ("MIDDLE EAST", 8, RED), ("ASIA", 9, NAVY), ("AFRICA", 5, ORANGE), ("AMERICAS", 5, TEAL), ("WORLD / SPACE", 4, PURPLE)]
x = 20; tot = 38
for name, n, c in REG:
    wseg = int((W - 40) * n / tot); d.rectangle([x, 90, x + wseg, 108], fill=c); d.text((x + 6, 94), f"{name} {n}", font=f_reg, fill=(255, 255, 255)); x += wseg
d.text((20, 114), "THE DAY IN UTC", font=f_kick, fill=RED)
UTC = [("02:15", "NATO vows space defence"), ("08:16", "Hanoi hot-pot blast"), ("10:42", "Saudi strikes Yemen"), ("14:27", "Riyadh tower hit"), ("16:51", "Houthis 60 km from Aden"), ("18:58", "Hormuz ship attack"), ("20:41", "Huawei guilty")]
for i, (t, s) in enumerate(UTC):
    cx = 20 + i * 141; d.text((cx, 130), t, font=f_time, fill=RED); txt(d, cx, 144, s, f_lab, w=132, lh=11, maxl=2)
d.line([20, 168, W - 20, 168], fill=LGREY); d.text((20, 174), "THE DAY IN NUMBERS", font=f_kick, fill=RED)
NUM = [("11", "hurt in Riyadh"), ("9", "killed in Ukraine"), ("50,018", "Dow closes"), ("+8.99%", "Taiex record"), ("25", "killed in Yemen"), ("26", "Cikande toll")]
for i, (n, s) in enumerate(NUM):
    cx = 210 + i * 132; d.text((cx, 172), n, font=f_num, fill=INK); d.text((cx, 196), s, font=f_lab, fill=GREY)
d.line([20, 214, W - 20, 214], fill=INK, width=1)
HERO = [("riyadh", "1  RIYADH  ·  MIDDLE EAST", "CONFIRMED", "Houthi drone hits Riyadh's tallest tower again, 11 hurt", "Second strike in a week on the PIF tower. 2 Saudi, 2 Indian, 3 Nepali, 4 Egyptian hurt. 14:27 UTC. (Saudi officials)"), ("chen", "2  SHANGHAI  ·  ASIA", "OFFICIAL", "China probes Shanghai party chief Chen Jining", "Chen, 62, probed for \u201cserious violations\u201d \u2014 the 4th Politburo member to fall this year. (CCDI)"), ("huawei", "3  NEW YORK  ·  US / TECH", "CONFIRMED", "Huawei guilty on 10 of 12 counts", "Jury convicts on trade-secret theft and bank fraud; cleared of racketeering. Sentencing Sep 2027; Huawei to appeal. 20:41 UTC. (US court)")]
for i, (kind, kick, ch, head, deck) in enumerate(HERO):
    hx = 20 + i * 331; hw = 322; d.rectangle([hx, 222, hx + hw, 420], outline=INK, width=1); scene(d, hx + 1, 223, hx + hw - 1, 323, kind)
    d.text((hx + 8, 328), kick, font=f_hkick, fill=RED); cy = chip(d, hx + 8, 344, ch); d.text((cy, 345), "  " + ("Saudi officials" if i == 0 else "CCDI" if i == 1 else "US court"), font=f_lab, fill=GREY)
    txt(d, hx + 8, 360, head, f_hhead, w=hw - 16, lh=18, maxl=2); txt(d, hx + 8, 396, deck, f_hdeck, w=hw - 16, lh=12, maxl=2)
# --- cards 4-13 ---
CARDS = [("war", "4  ZAPORIZHZHIA · WAR", "REPORTED", "Russian attacks kill 9 across Ukraine in a day", "9 killed, 81 hurt; 96 drones launched, 73 downed. (Ukrainian officials)"), ("trophy", "5  CAS · AFCON", "OFFICIAL", "CAS hands Senegal back the AFCON title", "Morocco forfeit 3\u20130; Senegal win 1\u20130. (CAS)"), ("ship", "6  HORMUZ · SHIPPING", "REPORTED", "IRGC attacks container ship in Hormuz", "Navigation disabled; exclusion zone north of Khasab, Oman. 18:58 UTC. (UKMTO)"), ("chart", "7  NEW YORK · MARKETS", "CONFIRMED", "Dow closes above 50,000 for the first time", "Dow 50,018. Nasdaq \u22121.5%; Taiex +8.99% record 40,122. (Markets)"), ("data", "8  REDMOND · TECH", "REPORTED", "Microsoft declares \u2018Code Red\u2019 after historic outage", "24-hour outage 12\u201313 Nov; 1-hour recovery target, 5 workstreams, 11,000+ Teams messages. (Reuters)"), ("heli", "9  ESKISEHIR · CRASH", "REPORTED", "Turkish military helicopter crash kills 5", "AS-532 down in Eskisehir. 19:52 UTC. (Turkish officials)"), ("market", "10  CARTAGENA · HOSTAGES", "REPORTED", "Supermarket hostages: 25 held in Cartagena", "5 elderly women freed; landings halted ~45 min. 17:35 UTC. (Colombia)"), ("desert", "11  ADEN · WAR", "REPORTED", "Houthis advance within 60 km of Aden", "Houthi forces close in on Aden, Yemen. 16:51 UTC. (Wires)"), ("strike", "12  LAHJ · STRIKES", "REPORTED", "Saudi strikes kill 25, wound 6 in Yemen", "Bus and truck hit in Wadi Maabaq, Lahj. 10:42 UTC. (Yemeni officials)"), ("rocket", "13  JIUQUAN · SPACE", "OFFICIAL", "China names first foreign astronaut for Tiangong", "Shenzhou-24 crew: Tang Hongbo, Wu Yi, Muhammad Zeeshan Ali of Pakistan. (CMSA)")]
for i, (kind, kick, ch, head, deck) in enumerate(CARDS):
    r, c = divmod(i, 5); cx = 20 + c * 197; cy = 428 + r * 98; cw = 191; d.rectangle([cx, cy, cx + cw, cy + 92], outline=INK, width=1); scene(d, cx + 1, cy + 1, cx + cw - 1, cy + 31, kind)
    d.text((cx + 5, cy + 34), kick, font=f_ckick, fill=RED); txt(d, cx + 5, cy + 45, head, f_chead, w=cw - 10, lh=12, maxl=2); txt(d, cx + 5, cy + 69, deck, f_cdeck, w=cw - 10, lh=11, maxl=2); chip(d, cx + cw - 62, cy + 34, ch)
# --- map + ALSO ---
MX0, MY0, MX1, MY1 = 20, 652, 500, 852
d.text((20, 630), "THE WORLD  ·  13 STORIES PINNED", font=f_mapt, fill=INK); d.rectangle([MX0, MY0, MX1, MY1], fill=(214, 232, 240), outline=INK)
def proj(lon, lat): return (MX0 + (lon + 180) / 360 * (MX1 - MX0), MY0 + (82 - lat) / 140 * (MY1 - MY0))
for poly in CONT:
    pts = [proj(lon, lat) for lon, lat in poly]; d.polygon(pts, fill=(120, 160, 110), outline=(90, 130, 85))
PINS = [(1, 46.7, 24.7), (2, 121.5, 31.2), (3, -74.0, 40.7), (4, 35.2, 47.8), (5, -17.4, 14.7), (6, 56.3, 26.6), (7, -74.0, 40.7), (8, -122.1, 47.7), (9, 30.5, 39.8), (10, -75.5, 10.4), (11, 45.0, 12.8), (12, 44.9, 13.0), (13, 98.5, 39.7)]
OFF = {7: (9, 9), 12: (-11, 9)}
for n, lon, lat in PINS:
    px, py = proj(lon, lat); ox, oy = OFF.get(n, (0, 0)); px, py = px + ox, py + oy; d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1); d.text((px - 3, py - 5), str(n), font=f_pin, fill=(255, 255, 255))
d.text((20, 856), "Red pins = stories 1\u201313.  Riyadh 1 · Shanghai 2 · New York 3, 7 · Zaporizhzhia 4 · Dakar 5 · Hormuz 6 · Redmond 8 · Eskisehir 9 · Cartagena 10 · Aden 11 · Lahj 12 · Jiuquan 13.", font=f_lab, fill=GREY)
d.text((512, 630), "ALSO ON TUESDAY \u2014 25 MORE STORIES", font=f_mapt, fill=INK)
ALSO = ["14  Ankara \u2014 Haftar's first visit to Turkey", "15  London \u2014 UK sanctions Houthis + 4 officials", "16  Villavicencio \u2014 Car bomb injures 23", "17  Gaza \u2014 Israel kills Hamas security chief", "18  Baghdad \u2014 Iraq takes over Kurdish oilfields", "19  Gaza \u2014 Meningitis alert: 272 cases in Oct", "20  DR Congo \u2014 Missing Cessna 208, rebels claim hit", "21  Hanoi \u2014 Hot-pot blast kills at least 6", "22  Gulf of Finland \u2014 Ukraine hits ship Sparta II", "23  Kuala Lumpur \u2014 Malaysia to return migrants", "24  Ulleungdo \u2014 Russian jets enter ADIZ", "25  Dhaka \u2014 Hasina plans return 16 Dec", "26  The Hague \u2014 14 nations back ICJ Myanmar ruling", "27  Jakarta \u2014 Indonesia nominates 2 VP candidates", "28  Beijing \u2014 Official Ma sentenced to death", "29  Brussels \u2014 NATO vows defence against space threat", "30  Mexico City \u2014 US drone aided Isidro capture", "31  San Salvador \u2014 Bukele names 3 soldiers killed", "32  Ottawa \u2014 Pentagon rebukes Canada over air fleet", "33  Washington \u2014 US adds Megaspeed to trade blacklist", "34  Kyiv \u2014 Zelensky urges talks soon", "35  Ras Al Khaimah \u2014 Bus-truck crash kills 13", "36  London \u2014 England record 5,258 heat deaths", "37  Kourou \u2014 Ariane 6 lofts 36 Amazon satellites", "38  Cikande \u2014 Factory-fire toll rises to 26"]
for i, s in enumerate(ALSO):
    col, row = divmod(i, 13); ax = 512 + col * 250; ay = 652 + row * 16; d.text((ax, ay), s, font=f_also, fill=INK)
# --- date check + footer ---
d.rectangle([20, 876, W - 20, 968], outline=RED, width=2); d.text((28, 882), "DATE CHECK", font=f_kick, fill=RED)
txt(d, 28, 898, "Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov); Nvidia brings back Huang (23 Nov); EU sanctions package 22 (23 Nov); COP31 ends no deal (22 Nov); corvette Merkury sinks (22 Nov); El Chapo Isidro arrested (20 Nov); Cikande factory fire starts (21 Nov); Trump hush-money appeal ruling (23 Nov). NOT YET: Shenzhou-24 launch (25 Nov 00:18 UTC); Huawei sentencing (Sep 2027); MPR VP vote (11 Dec); Hasina returns (16 Dec).", f_dc, w=W - 56, lh=13, maxl=5)
txt(d, 20, 976, "Sources: dailysummaryof.com/world/2026-11-24 (64 sources) · Astrova News · Horizon · WSOC/AP · Reuters · UKMTO · CAS · CMSA · CCDI.  CONFIRMED = 2+ outlets · OFFICIAL = on record · REPORTED = one outlet · CLAIM = one side's claim.  Scenes are drawn illustrations, not photographs.", f_foot, w=W - 40, lh=12, maxl=3)
out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png"); os.makedirs(os.path.dirname(out), exist_ok=True); img.save(out, optimize=True); print("saved", out, img.size)
