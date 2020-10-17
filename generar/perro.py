from PIL import Image, ImageDraw, ImageFont
import os

def draw_text(img, draw, pos, texto, font=None, fill=None,
              halo=True, shadow=True) :
    if shadow :
        #offset = int(font.size*0.06)
        offset = int((font.size**0.5)*0.55)
        draw.text((pos[0]+offset, pos[1]+offset), texto, font=font, fill=(0,0,0))
    draw.text(pos, texto, font=font, fill=fill)

def generate_banner(datos, prmode=False, blacksquares=True,
                    custombg=None, darkenbg=True,
                    customcolor=None, customcolor2=None,
                    font="font.ttc", fontcolor=(255,255,255), shadow=True,
                    icon_sizes=None) :
    game = datos["game"]
    players = datos["players"]

    path = os.path.realpath(__file__)
    path= os.path.abspath(os.path.join(path, os.pardir))
    template = os.path.join(path, "template")
    fonttc = os.path.join(path, font)

    # Constantes
    portraits = os.path.join(path, "assets", game, "portraits")
    icons = os.path.join(path, "assets", game, "icons")
    SIZE = (1423,800)

    BIG = (483, 483)
    MED = (257, 257)
    SMA = (192, 192)

    POS = [(53, 135), (553, 135), (832, 135), (1110, 135),
           (553, 441), (760, 441), (968, 441), (1176, 441)]

    SIZETWI = [(483, 39), (257, 29), (257, 29), (257, 29),
               (192, 26), (192, 26), (192, 26), (192, 26)]

    POSTWI = [(52, 624), (552, 398), (831, 398), (1109, 398),
              (552, 637), (759, 637), (967, 637), (1175, 637)]

    POSTXT = [(53, 45), (53, 730), (875, 50), (1075, 725)]

    # La que tal
    c = Image.new('RGBA', SIZE, (0, 0, 0))

    # Fondo
    if custombg :
        f = Image.open(custombg, mode="r")
        ancho, largo = f.size
        a,b = int(ancho*SIZE[1]/largo), int(largo*SIZE[0]/ancho)
        if a < SIZE[0] :
            ancho, largo = SIZE[0], b
        else :
            ancho, largo = a, SIZE[1]
        f = f.resize((ancho, largo), resample=Image.ANTIALIAS)
        c.paste(f, ( int((SIZE[0]-ancho)/2), int((SIZE[1]-largo)/2) ) )
        if darkenbg :
            f = Image.new('RGBA', SIZE, (0, 0, 0, 255))
            c = Image.blend(c, f, 0.75)
    else :
        a  = Image.open(os.path.join(path, "assets", game, "bg.png"))
        c.paste(a, (0,0), mask=a)

    c = c.convert('RGB')

    # Pa escribir
    draw = ImageDraw.Draw(c)

    # Ciclo de portraits
    for i in range(8) :
        if i == 0 : size = BIG
        elif i < 4 : size = MED
        else : size = SMA

        if blacksquares :
            shape = [POS[i], (POS[i][0]+size[0], POS[i][1]+size[1])]
            draw.rectangle(shape, fill=(0,0,0))

        char = players[i]["char"]
        ruta = os.path.join(portraits, char[0])
        ruta = os.path.join(ruta, str(char[1])+".png")
        d = Image.open(ruta).convert("RGBA").resize(size, resample=Image.ANTIALIAS)
        
        # Intento de sombra
        if shadow :
            if customcolor : shadowcolor = customcolor
            else : shadowcolor = (255, 40, 56, 255)

            # offset de la sombra respecto al portrait
            shadowpos = int(size[0]*0.03)

            cuadrao = (  POS[i][0]+shadowpos,
                         POS[i][1]+shadowpos,
                         POS[i][0]+size[0],
                         POS[i][1]+size[1]
                      )
            cortao = (0, 0, size[0]-shadowpos, size[1]-shadowpos)
            dd =  d.crop(cortao)
            lasombra = Image.new('RGBA', cortao[2:], shadowcolor)

            c.paste(lasombra, cuadrao, mask=dd)
        c.paste(d, POS[i], mask=d)

    # Partes del template
    a  = Image.open(os.path.join(template,"marco.png"))
    if customcolor :
        y = Image.new('RGB', SIZE, customcolor)
        c.paste(y, (0,0), mask=a)
    else :
        c.paste(a, (0,0), mask=a)

    a  = Image.open(os.path.join(template,"polo.png"))
    if customcolor2 :
        y = Image.new('RGB', SIZE, customcolor2)
        c.paste(y, (0,0), mask=a)
    else :
        c.paste(a, (0,0), mask=a)

    if prmode :
        a = Image.open(os.path.join(template,"numerospr.png"))
    else :
        a = Image.open(os.path.join(template,"numeros.png"))
    c.paste(a, (0,0), mask=a)
    #c = Image.alpha_composite(a,c)

    # Textos de arriba y abajo
    fuente = ImageFont.truetype(fonttc, 30)
    draw_text(c, draw, POSTXT[0], datos["toptext"], font=fuente, fill=fontcolor, shadow=True)
    draw_text(c, draw, POSTXT[1], datos["bottomtext"], font=fuente, fill=fontcolor, shadow=False)

    fuente = ImageFont.truetype(fonttc, 25)
    urlmarg = (40-len(datos["url"]))*6
    draw_text(c, draw, (POSTXT[2][0]+urlmarg,POSTXT[2][1]), datos["url"], font=fuente, fill=fontcolor, shadow=False)
    draw_text(c, draw, POSTXT[3], "Design by:  @Elenriqu3\nGenerator by: @Riokaru", font=fuente, fill=fontcolor, shadow=True)

    # Ciclo de nombres
    pajarito = Image.open(os.path.join(template,"pajarito.png"))
    for i in range(8) :
        if i == 0 : size = BIG
        elif i < 4 : size = MED
        else : size = SMA
        if players[i]["twitter"] :
            # Cajita para twitter handle
            if customcolor :
                colorcito = customcolor
            else :
                colorcito = (255, 40, 56, 255)
            draw.rectangle([POSTWI[i],
                            (POSTWI[i][0]+SIZETWI[i][0],
                             (POSTWI[i][1]+SIZETWI[i][1]))],
                           fill=colorcito
                           )
            # Pajarito de Twitter
            if pajarito.size[1] != SIZETWI[i][1] :
                psize = ((pajarito.size[0]*SIZETWI[i][1])//pajarito.size[1],
                         SIZETWI[i][1])
                pajarito = pajarito.resize(psize, resample=Image.ANTIALIAS)
            c.paste(pajarito,
                    (int(POSTWI[i][0]+SIZETWI[i][0]*0.02), POSTWI[i][1]),
                    mask=pajarito)

            lon = len(players[i]["twitter"])
            sizef = (27*SIZETWI[i][1])//SIZETWI[0][1]
            tmarg = (6*SIZETWI[i][1])//SIZETWI[0][1]
            lmarg = (SIZETWI[i][0]-0.5*sizef*lon+pajarito.size[0])//2

            font = ImageFont.truetype(fonttc, sizef)
            draw_text(c, draw, (POSTWI[i][0]+lmarg, POSTWI[i][1]+tmarg),
                      players[i]["twitter"], font=font, fill=fontcolor, shadow=True)
        sizefont = int(size[0]*0.26)
        texto = players[i]["tag"].replace(". ", ".").replace(" | ", "|")
        if len(texto) > 7 :
            sizefont = int(sizefont*7/len(texto))
        font = ImageFont.truetype(fonttc, sizefont)
        draw_text(c, draw, (POS[i][0] + (size[0]-0.5*sizefont*len(texto))//2,
                   POS[i][1]+int(size[0]*0.995)-sizefont),
                   texto, font=font, fill=fontcolor)

        # extras
        s_off = 0
        for char in players[i]['secondaries'] :
            try :
                ruta_i = os.path.join(icons, char[0])
                ruta_i = os.path.join(ruta_i, str(char[1])+".png")
                ic = Image.open(ruta_i)
                if size != BIG :
                    if icon_sizes : i_size = icon_sizes[1]
                    else : i_size = 32
                    ic = ic.resize((i_size, i_size),resample=Image.ANTIALIAS)
                    if size == MED :
                        rmarg = 8
                    else :
                        rmarg = 6
                else :
                    if icon_sizes : i_size = icon_sizes[0]
                    else : i_size = 64
                    ic = ic.resize((i_size, i_size),resample=Image.ANTIALIAS)
                    rmarg = 14
                c.paste(ic, (POS[i][0]+size[0]-i_size-rmarg, POS[i][1]+s_off*(i_size+4)+rmarg), mask=ic)
                s_off += 1
            except :
                print("not found: "+str(ruta_i))
    return c

if __name__ == "__main__":
    # datos y configuración

    custombg = "bgusb.jpg"
    customcolor = (255, 201, 14)
    fontcolor = (255,255,255)
    shadow = True

    """
    texto = ["Morrocoyo", "Morrocoyoo","Morrocoyooo", "Morrocoyoooo",
             "Morrocoyooooo", "Morrocoyoooooo", "Morrocoyooooooo",
             "Morrocoyoooooooo"]
    texto = ["$Scruzz" for i in range(8)]
    texto = ["Morrocoyo", "Garu", "Vexx", "Kellios",
             "CarvaGrease", "Luigic7", "Lalter", "CartezSoul"]
    texto = ["$Cruz", "SexCruz", "XXXCruz", "Scruz",
             "CCruz", "ZCruz", "KCruz", "QKCruz"]
    personajes = [("Banjo & Kazooie", 0),
                  ("Incineroar", 2),
                  ("Terry", 1),
                  ("Piranha Plant", 0),
                  ("Dark Samus", 2),
                  ("Dr Mario", 4),
                  ("Captain Falcon", 4),
                  ("Yoshi", 1)]
    """

    """
    texto = ["morrocoYo", "GARU", "Pancakes", "VeXx",
             "BTO", "Vunioq", "Nandok", "Kellios"]
    personajes = [("Robin", 0),
                  ("Joker", 0),
                  ("Inkling", 5),
                  ("Inkling", 2),
                  ("Mr Game & Watch", 0),
                  ("Samus", 0),
                  ("Sonic", 1),
                  ("Terry", 0)]
    twitter = ["@DanielRimeris", "@GARU_Sw", "@movpancakes", "@RisingVexx",
               "@HoyerBTO", "@Vunioq", "@Nandok_95", "@CarlosDQC"]
    pockets = [[("Bowser", 5)], [("Falco", 5), ("Fox", 3)], [("Mega Man", 1)], [("Marth", 2)],
               [], [], [], []]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Show Me your Moves - Ultimate Singles - Top 8",
             "bottomtext" : "22 de Febrero de 2020 - Caracas, Venezuela - 89 participantes",
             "url" : "facebook.com/groups/smashvenezuela",
             }
    """
    

    """
    texto = ["CartezSoul", "Riokaru", "Luigic7", "Reyn",
             "3rdStrike", "SCruz", "Deathmouth", "Yuky-Pak"]
    twitter = ["@SilvxBexts", "@Riokaru", "@LuigiDiMartino", None,
               "@altuveguitar", None, "@BoseJoaoGamer", "@9msfts"]
    personajes = [("Pikachu", 2),
                  ("Mewtwo", 2),
                  ("King Dedede", 1),
                  ("Corrin", 0),
                  ("Ken", 3),
                  ("Banjo & Kazooie", 0),
                  ("Joker", 0),
                  ("Mario", 0)]

    datos = {"players" : players,
             "toptext" : "Saltynejas 6 - Ultimate Singles - Top 8",
             "bottomtext" : "14 de Febrero de 2020 - Universidad Simon Bolivar - 19 participantes"}

    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]
    """

    """
    texto = ["1stStrike", "2ndStrike", "3rdStrike", "4thStrike",
             "5thStrike", "6thStrike", "7thStrike", "8thStrike"]
    personajes = [("Ken", i) for i in range(8)]
    twitter = ["altuveguitar" for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Conyazo3 Tournament - Street Fighter 3rd Strike - Top 8",
             "bottomtext" : "3 de Marzo de 2033 - Caracas, Memezuela - 33 participantes"}
    """
    """
    texto = [s[:-1] for s in ["Min "*(i+1) for i in range(8)]]
    personajes = [("Min Min", i) for i in range(8)]
    twitter = ["MinMin0"+str(i+1) for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i]} for i in range(8)]
    datos = {"players" : players,
             "toptext" : "Min Min Min Min Min Min Min Min",
             "bottomtext" : "Min Min Min Min Min Min Min Min",
             "url" : "http://riokaru.pythonanywhere.com/",
             }
    """

    """
    texto = ["Absa", "Clairen", "Elliana", "Etalus",
             "Forsburn", "Kragg", "Maypul", "Orcane"]
    personajes = [(texto[i], i) for i in range(7)] + [("Orcane",8)]
    twitter = ["@danfornace" for i in range(8)]
    pockets = [[] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "@danfornace I made this graphic generator for RoA ",
             "bottomtext" : "Please notice me @danfornace",
             "url" : "riokaru.pythonanywhere.com",
             "game" : "roa"
             }
    """
    
    """
    texto = ["Afi and Galu", "Ashani", "Ezzie", "Kidd",
             "Raymer", "Urdah", "Weishan", "Zhurong"]
    personajes = [(texto[i], 0) for i in range(8)]
    twitter = ["@RushdownRevolt" for i in range(8)]
    pockets = [[(texto[(i+1)%8],0), (texto[(i+2)%8],0)] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "Top text goes here",
             "bottomtext" : "Bottom text goes here",
             "url" : "riokaru.pythonanywhere.com",
             "game" : "rr"
             }
    cc1 = (56,75,203)
    cc2 = (64, 235, 143)
    """

    """
    texto = ["Player "+str(i) for i in range(1,9)]
    #p = ["Banjo & Kazooie", "Bayonetta", "Bowser", "Bowser Jr", "Byleth", "Captain Falcon", "Chrom", "Cloud"]
    p = ["Samus", "Sheik", "Shulk", "Simon", "Snake", "Sonic", "Steve", "Terry"]
    personajes = [(p[i], i) for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "",
             "bottomtext" : "",
             "url" : "riokaru.pythonanywhere.com",
             "game" : "ssbu"
             }
    """

    #"""
    texto = ["Player "+str(i) for i in range(1,9)]
    #p = ["Banjo & Kazooie", "Bayonetta", "Bowser", "Bowser Jr", "Byleth", "Captain Falcon", "Chrom", "Cloud"]
    p = ["Samus", "Sheik", "Shulk", "Simon", "Snake", "Sonic", "Steve", "Terry"]
    import random
    c = ['Beowulf', 'Big Band', 'Cerebella', 'Double', 'Eliza', 'Filia', 'Fukua', 'Ms Fortune', 'Painwheel', 'Parasoul', 'Peacock', 'Robo Fortune', 'Squigly', 'Valentine']
    personajes = [(random.choice(c), random.randint(0,26)) for i in range(8)]
    twitter = ["player"+str(i) for i in range(1,9)]
    pockets = [[(random.choice(c), 0), (random.choice(c), 0)] for i in range(8)]
    players = [{"tag" : texto[i],
              "char" : personajes[i],
              "twitter" : twitter[i],
              "secondaries" :  pockets[i] } for i in range(8)]

    datos = {"players" : players,
             "toptext" : "",
             "bottomtext" : "Please help me I haven't slept in 4 days",
             "url" : "riokaru.pythonanywhere.com",
             "game" : "sg"
             }
    cc1 = (215, 62, 62)
    cc2 = (203, 198, 186)
    #"""

    import time
    t1 = time.time()
    #img = generate_banner(datos, customcolor="#00bbfa", customcolor2="#001736")# customcolor="#287346", customcolor2="#ede07c")
    img = generate_banner(datos, icon_sizes=(80,50), shadow=True, prmode=False, blacksquares=False,
                          customcolor=cc1, customcolor2=cc2)
    t2 = time.time()
    print(t2-t1)
    img.show()
    img.save("sample.png")

    input()
