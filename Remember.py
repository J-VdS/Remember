from tkinter import *
import random, time

class remember(object):
    def __init__(self, interval):
        self.interval = interval

        #window generatie:
        self.tk = Tk()
        self.tk.resizable(0,0)
        self.tk.wm_attributes('-topmost', 1)

        self.canvas = Canvas(self.tk, width=200, height=200, bd=0, bg='#8ef2a6', \
                             highlightthickness=0)
        self.canvas.pack()
        #titel
        self.canvas.create_text(100, 5, text='Remember...', anchor=N, \
                                font=('Helvetica', 20), fill='#0000ff')
        # U/I info
        self.score = 0
        self.scoretxt = self.canvas.create_text(2, 200, anchor=SW, fill='red', \
            text='SCORE: %s' %(self.score), font=('Helvetica', 9))
        #self.lastnummer = '?'
        self.lastnummtxt = self.canvas.create_text(198, 200, anchor=SE, fill='red', \
            text='LAST: %s' %('?'), font=('Helvetica', 9))
        self.order = self.canvas.create_text(100, 200, anchor=S, text='WAIT', \
            font=('Helvetica', 9))
        

        self.nummers = []
        self.knoppen = []
        self.antwoord = []
        self.yourturn = False

        self.canvas.bind_all('<Button - 1>', self.control)

    def numgen(self):
        self.nummers.append(random.randint(1, 9))
        self.showsequence()
        self.yourturn = True
        self.canvas.itemconfig(self.order, text='GO')

    def knoptoevoegen(self, a):
        self.knoppen.append(a)
        return
    
    def showsequence(self):
        for i in self.nummers:
            self.knoppen[i-1].color(self.interval)
            self.tk.update()

    def control(self, evt):
        if self.yourturn == True:
            x = self.tk.winfo_pointerx() - self.tk.winfo_rootx()
            y = self.tk.winfo_pointery() - self.tk.winfo_rooty()
            inputs = [i.clicked(x, y) for i in self.knoppen]
            if True in inputs:
                ind = inputs.index(True)
                self.antwoord.append(ind+1)
                
                #aanpass last nummer info
                self.canvas.itemconfig(self.lastnummtxt, text='LAST: %s' \
                                       %(ind+1))
                #oplichten knop in randow kleurtje
                self.knoppen[ind].color(.25)
                
                if self.antwoord[-1] != self.nummers[len(self.antwoord)-1]:
                    self.endgame()
                    return
                
            if len(self.nummers) == len(self.antwoord):
                self.yourturn = False
                #aanpassen order
                self.canvas.itemconfig(self.order, text='WAIT')
                #aanpassen score
                self.score += 1
                self.canvas.itemconfig(self.scoretxt, text='SCORE: %s' \
                                       %(self.score))
                #volgend nummer genereren
                self.numgen()

                del self.antwoord
                self.antwoord = []
        return

    def endgame(self):
        self.yourturn = False
        #aanpassen order naar DEAD
        self.canvas.itemconfig(self.order, text='DEAD')
        self.tk.update()
        
        time.sleep(3)
        self.tk.destroy()
        
        
class knoppen(object):
    def __init__(self, info, x, y, tx):
        self.x, self.y = x, y
        (self.canvas, self.tk, self.interval) = info
        self.width = 50
        self.height = 40
        
        self.blok = self.canvas.create_rectangle(x, y, x+self.width, y+self.height, \
                                     fill= 'white')
        self.tx = self.canvas.create_text(int(x+self.width/2), \
        int(y+self.height/2), anchor=CENTER, font=('Helvetica',16),text=tx)

        self.colored = False

    def color(self, interval):
        kleur = random.choice(['#0000ff', '#ff0000', '#ff00f1', '#ff0088', \
                               '#40e0d0', '#f4a460' ])

        self.canvas.itemconfig(self.tx, fill=kleur)
        self.canvas.itemconfig(self.blok, outline=kleur)
        self.tk.update()
        time.sleep(interval)
        
        self.canvas.itemconfig(self.tx, fill='black')
        self.canvas.itemconfig(self.blok, outline='black')
        self.tk.update()
        time.sleep(interval)
        return

    def clicked(self, x, y):
        return (self.x < x < self.x+self.width)* \
               (self.y < y < self.y+self.height) 

#setup spel
x = remember(1)
info = (x.canvas, x.tk, x.interval)
#knoppengeneratie
for i in range(0,3):
    for j in range(0,3):
        x.knoptoevoegen(knoppen(info, 15+60*j, 45+50*i, str(3*i+j+1)))

info[1].update()        
time.sleep(2)
x.numgen()

while True:
    try:
        info[1].update()
        info[1].update_idletasks()
    except:
        print('used')
        break



        
        
