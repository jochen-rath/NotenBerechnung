from kivy.properties import  ObjectProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
import csv
import datetime
import os
import io

class MultiButton(Button):
    pass
class MenuButton(MultiButton):
    pass
class Ueberschriften(BoxLayout):
    pass

class MenuZeile(FloatLayout):
    pass

class Zeile(BoxLayout):
    def aenderName(self,name):
        self.ids.name.vorname = name[0]
        self.ids.name.nachname = name[1]
    def getNamen(self):
        return [self.ids.name.vorname,self.ids.name.nachname]
    def setzeNote(self,note):
        self.ids.note.text = str(note)
    pass

class Notenliste(BoxLayout):
#Diese Klasse erzeugt ein Widget, in dem die mundlichen Durchschnittsnoten berechnet und dargestellt werden.
    def leseConfigDatei(self,configDatei):
        app=App.get_running_app()
        with open(configDatei) as csvfile:
            # Format:  Nachname,Vorname,Posx,Poxy,Note1,Note2
            #    Klasse,Ph8e,122,0,2021.12.24,2021.12.25,...
            #    Mustermann,Max,0,234,1,6,...
            #    Musterfrau,Märthe,240,234,3,2,...
            s=csv.reader(csvfile, delimiter=',')
            klasseInDatei=False
            for i, l in enumerate(s):
                if l[0]=='Klasse':
                    klasseInDatei=True
                    if len(l)<4:
                        # Es existiert keine Position, gib sie an
                        l=l+[int(app.breite/2), app.schriftgroesse]
                    self.klasse=l[0:4]
                    if len(l)>4:
                        self.tage=l[4:]
                else:
                    # Existiert keine Position, verteile die Schueler in einem Raster auf dem Bildschirm.
                    # Berechne deren Position mit dem modulo.
                    if len(l)<4:
                        l=l+[int(app.breite*(i%5)/5),
                             (app.hoehe-app.schriftgroesse*10)*int(i/5)/5+app.schriftgroesse*5]
                    #Ist eine Klasse auf mehreren Räumen verteilt, gibt es mehrere Notendateien. Fasse diese zusammen,
                    #indem du die Noten an einem bereits existierenden Schüler anhängst.
                    elif l[0] in [x[0] for x in self.schuelerDaten] and l[1] in [x[1] for x in self.schuelerDaten]:
                        index=0
                        for i,d in enumerate(self.schuelerDaten):
                            if l[0]==d[0] and l[1]==d[1]:
                                index=i
                        self.schuelerDaten[index]=self.schuelerDaten[index]+l[4:]
                    else:
                        self.schuelerDaten.append(l)
            if not klasseInDatei:
                self.klasse=['Klasse', (app.configDatei.split('_')[1]).split('.')[0], int(app.breite/2), app.schriftgroesse]
    def berechneNoten(self,notenliste):
        noten=[int(x) for x in notenliste if x.isdigit()]
        return -1 if len(noten)<1 else round(sum(noten)/len(noten),2)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        app=App.get_running_app()
        self.schuelerWidget=[]
        self.klasse = (app.configDatei.split('_')[1]).split('.')[0]
        self.add_widget(Label(text=self.klasse,font_size=app.schriftgroesse))
        self.orientation='vertical'
        self.schuelerDaten=[]
        mehrereRaeumeSelbeKlasse=[x for x in  os.listdir(app.grundpfad) if x.startswith('Noten_')  and self.klasse in x]
        for configDatei in mehrereRaeumeSelbeKlasse:
            self.leseConfigDatei(os.path.join(app.grundpfad,configDatei))
        vornamen=[]
        for schueler in self.schuelerDaten:
            self.schuelerWidget.append(Zeile())
            self.schuelerWidget[-1].aenderName([schueler[0],schueler[1]])
            if len(schueler)>3:
                self.schuelerWidget[-1].setzeNote(self.berechneNoten(schueler[4:]))
            self.add_widget(self.schuelerWidget[-1])
        self.add_widget(MenuZeile())

class StelleMenueDar(Widget):
    def __init__(self):
        super().__init__()
        root=BoxLayout()
        root.orientation='vertical'
        app=App.get_running_app()
        l=Label(text='Übersicht',font_size=app.schriftgroesse,size_hint=[None,None],size=[app.breite, 2*app.schriftgroesse])
        root.add_widget(l)
        g=GridLayout(rows= 4,cols= 6,padding= 20,spacing= 20)
        bten=[]
        for i,file in enumerate(app.configDateien):
            klasse=(file.split('_')[1]).split('.')[0]
            bten.append(MenuButton(text=klasse))
            g.add_widget(bten[-1])
        root.add_widget(g)
        root.pos=[0,app.hoehe-self.size[1]]
        self.add_widget(root)
        exit=MultiButton(text='Exit')
        exit.pos=[0,0]
        exit.bind(on_press=lambda  x:app.stop())
        self.add_widget(exit)
        infobox=BoxLayout(orientation='vertical')
        infobox.pos=[0,exit.size[1]+infobox.size[1]]
        if os.path.isfile(os.path.join(app.grundpfad,app.infodatei)):
            with open(os.path.join(app.grundpfad,app.infodatei)) as csvfile:
                s = csv.reader(csvfile, delimiter=',')
                for zeile in s:
                    if len(zeile)>1:
                        infobox.add_widget(Label(text=zeile[0]+': '+' '.join(zeile[1:]),font_size=app.schriftgroesse))
                    else:
                        infobox.add_widget(
                            Label(text=str(zeile), font_size=app.schriftgroesse))
        infobox.pos=[0,exit.size[1]]
        infobox.center_x=app.breite/2
        self.add_widget(infobox)

class mainApp(App):
    breite=Window.size[0]
    hoehe=Window.size[1]
#Bei 800 Pixel, Schriftgröße 20, bei 1080 Pixel Schriftgröße 35. Dazwischen lineare interpolieren
#Die Felder sind Breit: Name: 5*SG, Vier Zaehler: 4*3.5*2*SG
#  -->   Breite=6*SG+4*3.5*2*SG=(5+28)*SG
#  -->
    schriftgroesse=int(breite/33)
    grundpfad='.' if platform != 'android' else os.path.join(os.getenv('EXTERNAL_STORAGE'),'sitzplanNoten')
    configDatei=''
    infodatei='infoDateiListeAusrutcher.csv'
    configDateien=[x for x in os.listdir(grundpfad) if x.startswith('Noten_') and (not 'D' in x)]
    aktuell=None
    root=None
    def entferneNotenlisteLadeMenu(self):
        self.root.remove_widget(self.aktuell)
        self.aktuell=StelleMenueDar()
        self.root.add_widget(self.aktuell)
    def entferneMenuLadeNotenliste(self,klasse):
        self.configDatei=os.path.join(self.grundpfad,[x for x in self.configDateien if (x.split('_')[1]).split('.')[0]==klasse][0])
        self.root.remove_widget(self.aktuell)
        self.aktuell=Notenliste()
        self.root.add_widget(self.aktuell)
    def build(self):
        self.configDatei=self.configDateien[0]
        self.root=BoxLayout()
        self.aktuell=StelleMenueDar()
        self.root.add_widget(self.aktuell)
        return self.root
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
