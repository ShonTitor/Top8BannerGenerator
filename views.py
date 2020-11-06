import os, base64, re
from io import BytesIO
from django.shortcuts import render, HttpResponse, loader
from .forms import makeform, SmashggForm
from .generar.perro import generate_banner
from .generar.getsets import event_data, challonge_data

def hestia(request, game, FormClass,
           hasextra=True, color_guide=None, icon_sizes=None):
    if hasextra : has_extra = "true"
    else : has_extra = "false"
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        form2 = SmashggForm(request.POST, request.FILES)
        v1 = form.is_valid()
        v2 = form2.is_valid()

        if v2 :
            event = request.POST["event"]
            match = re.search("https://smash.gg/tournament/[^/]+/event/[^/]+", request.POST["event"])
            if match :
                datos = event_data(event[17:match.end()])
            else :
                match = re.search("https://challonge.com/[^/]+", request.POST["event"])
                datos = challonge_data(event[22:match.end()])
            init_data = {}

            init_data["ttext"] = datos["toptext"]
            init_data["btext"] = datos["bottomtext"]
            init_data["url"] = datos["url"]

            for i in range(8) :
                try :
                    init_data["name"+str(i+1)] = datos["players"][i]["tag"]
                    init_data["twitter"+str(i+1)] = datos["players"][i]["twitter"]
                    init_data["char"+str(i+1)] = datos["players"][i]["char"][0]
                except :
                    pass
            
            context = { "hasextra" : has_extra,
                        "form" : FormClass(initial=init_data),
                        "form2" : SmashggForm(),
                        "off" : 2,
                        "color_guide" : color_guide,
                        "game" : game,
                        "result" : None
                      }
            return render(request, 'index.html' , context)
        if v1 :
            if request.POST["lcolor1"] == "#ff281a" :
                c1 = None
            else :
                c1 = request.POST["lcolor1"]
            if request.POST["lcolor2"] == "#ffb60c" :
                c2 = None
            else :
                c2 = request.POST["lcolor2"]
            if "background" not in request.FILES :
                bg = None
            else :
                bg = request.FILES["background"]

            # toggles
            try :                
                request.POST["darken_bg"]
                darkbg = True
            except : darkbg = False

            try :                
                request.POST["charshadow"]
                cshadow = True
            except : cshadow = False

            try :                
                request.POST["prmode"]
                pr = True
            except : pr = False

            try :       
                request.POST["blacksquares"]
                blacksq = True
            except : blacksq = False

            names = []
            twitter = []
            chars = []
            seconds = [[] for i in range(8)]
            for i in range(1,9) :
                names.append(request.POST["name"+str(i)])
                if request.POST["twitter"+str(i)] == "" :
                    twitter.append(None)
                else :
                    twitter.append(request.POST["twitter"+str(i)])
                chars.append( (request.POST["char"+str(i)],
                               request.POST["color"+str(i)])
                            )
                if hasextra :
                    for k in range(1,3) :
                        if request.POST["extra"+str(i)+str(k)] == "None" :
                            continue
                        else :
                            seconds[i-1].append((request.POST["extra"+str(i)+str(k)],
                                               request.POST["extra_color"+str(i)+str(k)]))
                
            players = [{"tag" : names[j],
                        "char" : chars[j],
                        "twitter" : twitter[j],
                        "secondaries" : seconds[j]
                            }
                       for j in range(8)]
            datos = { "players" : players,
                        "toptext" : request.POST["ttext"],
                        "bottomtext" : request.POST["btext"],
                        "url" : request.POST["url"],
                        "game" : game,
                    }

            fuente = request.POST["fontt"]
            if fuente == "auto" : fuente = None
            
            img = generate_banner(datos,
                                  customcolor= c1,
                                  customcolor2=c2,
                                  custombg=bg,
                                  darkenbg=darkbg,
                                  shadow=cshadow,
                                  prmode=pr,
                                  blacksquares=blacksq,
                                  icon_sizes=icon_sizes,
                                  font=fuente,
                                  fontcolor1=request.POST["fcolor1"],
                                  fontscolor1=request.POST["fscolor1"],
                                  fontcolor2=request.POST["fcolor2"],
                                  fontscolor2=request.POST["fscolor2"],
                                    )
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img = base64.b64encode(buffered.getvalue())
            img = str(img)[2:-1]
            #context = { "img" : img }
            #return render(request, 'gg.html' , context)
            context = { "hasextra" : has_extra,
                        "form" : FormClass(initial=request.POST),
                        "form2" : SmashggForm(),
                        "off" : 2,
                        "color_guide" : color_guide,
                        "game" : game,
                        "result" : img
                      }
            return render(request, 'index.html' , context)

        else :
            context = {
               "hasextra" : has_extra,
               "color_guide" : color_guide,
               "game" : game,
               "result" : None
               }
            if "event" in request.POST :
                form = FormClass()
                context["off"] = 1
            else :
                form2 = SmashggForm()
                context["off"] = 2

            context["form"] = form
            context["form2"] = form2
    
            return render(request, 'index.html' , context)
            
            
    else :
        form = FormClass()
        form2 = SmashggForm()
    context = {
               "form" : form,
               "form2" : form2,
               "off" : 2,
               "hasextra" : has_extra,
               "color_guide" : color_guide,
               "game" : game,
               "result" : None
               }
    return render(request, 'index.html' , context)

def index(request) :
    FormClass = makeform()
    sample = "https://i.imgur.com/V1KwDFu.png"
    c_guide = "https://www.ssbwiki.com/Alternate_costume_(SSBU)"
    return hestia(request, "ssbu", FormClass, color_guide=c_guide)

def roa(request) :
    c = ["Random", "Absa", "Clairen", "Elliana", "Etalus",
         "Forsburn", "Kragg", "Maypul", "Orcane",
         "Ori and Sein", "Ranno", "Shovel Knight",
         "Sylvanos", "Wrastor", "Zetterburn"]
    FormClass = makeform(chars=c, numerito=21, numerito_extra=1)
    sample = "https://i.imgur.com/rPmXNDr.png"
    return hestia(request, "roa", FormClass, sample)

def sg(request) :
    c = ['Beowulf', 'Big Band', 'Cerebella', 'Double', 'Eliza',
         'Filia', 'Fukua', 'Ms Fortune', 'Painwheel', 'Parasoul',
         'Peacock', 'Robo Fortune', 'Squigly', 'Valentine']
    FormClass = makeform(chars=c, numerito=30, numerito_extra=1)
    c_guide = "https://wiki.gbl.gg/w/Skullgirls"
    return hestia(request, "sg", FormClass, color_guide=c_guide)

def rr(request) :
    c = ["Afi and Galu", "Ashani", "Ezzie", "Kidd",
         "Raymer", "Urdah", "Weishan", "Zhurong"]
    FormClass = makeform(chars=c, numerito=1, numerito_extra=1)
    return hestia(request, "rr", FormClass, icon_sizes=(80,50))

def melee(request) :
    c = ['Bowser', 'Captain Falcon', 'Donkey Kong', 'Dr Mario', 'Falco',
         'Fox', 'Ganondorf', 'Ice Climbers', 'Jigglypuff', 'Kirby', 'Link',
         'Luigi', 'Mario', 'Marth', 'Mewtwo', 'Mr Game & Watch', 'Ness',
         'Peach', 'Pichu', 'Pikachu', 'Roy', 'Samus', 'Sheik', 'Yoshi',
         'Young Link', 'Zelda']
    FormClass = makeform(chars=c, numerito=6)
    c_guide = "https://www.ssbwiki.com/Alternate_costume_(SSBM)"
    return hestia(request, "melee", FormClass, sample, icon_sizes=(48,24))

def ggxx(request) :
    c = ['A.B.A', 'Anji Mito', 'Axl Low', 'Baiken', 'Bridget', 'Chipp Zanuff',
         'Dizzy', 'Eddie', 'Faust', 'I-No', 'Jam Kuradoberi', 'Johnny',
         'Justice', 'Kliff Undersn', 'Ky Kiske', 'May', 'Millia Rage',
         'Order-Sol', 'Potemkin', 'Robo-Ky', 'Slayer', 'Sol Badguy',
         'Testament', 'Venom', 'Zappa']
    FormClass = makeform(chars=c, numerito=22, hasextra=False)
    c_guide = "https://www.dustloop.com/wiki/index.php?title=Guilty_Gear_XX_Accent_Core_Plus_R"
    return hestia(request, "ggxx", FormClass, sample, color_guide=c_guide, hasextra=False)

def uni(request) :
    c = ['Akatsuki', 'Byakuya', 'Carmine', 'Chaos', 'Eltnum', 'Enkidu',
         'Gordeau', 'Hilda', 'Hyde', 'Linne', 'Londrekia', 'Merkava',
         'Mika', 'Nanase', 'Orie', 'Phonon', 'Seth', 'Vatista', 'Wagner',
         'Waldstein', 'Yuzuriha']
    FormClass = makeform(chars=c, numerito=42, numerito_extra=1,
                         color1="#32145a", color2="#c814ff")
    c_guide = "https://wiki.gbl.gg/w/Under_Night_In-Birth/UNICLR"
    return hestia(request, "uni", FormClass, color_guide=c_guide)
