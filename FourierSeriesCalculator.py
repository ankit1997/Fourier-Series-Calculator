try:
    import tkinter as tk # python 3
except ImportError:
    import Tkinter as tk # python 2

from calculation import *
from sympy import nan

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fourier Series Calculator")
        self.root["bg"] = 'white'

        self.calculator = Calculation(self)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.width = int(3*screen_width/5)
        self.height = int(screen_height/2)
        self.font = ('Georgia',)

        self.root.geometry('{}x{}'.format(self.width,self.height))
        self.root.resizable(width = True, height = False)

        # info Frame for displaying the formula
        self.infoFrame = tk.Frame(self.root,width = self.width/3,height = self.height,background = 'cornflowerblue')    
        self.infoFrame.place(x = 0,y = 0)

        # main Frame for user interaction
        self.mainFrame = tk.Frame(self.root,width = 2*self.width/3 - 50,height = self.height,background = 'white')
        self.mainFrame.place(x = self.width/3,y = 0)

        # set the layout
        self.setLayout()
        self.root.mainloop()
    
    def setLayout(self):
        formula = '''f(x) = a0 + Σancos(2nxπ/T) \n                  + Σbnsin(2nxπ/T)'''

        a0 = 'a0 = (1/2T)∫f(x)dx'
        an = 'an = (1/T)∫f(x)cos(nx)dx'
        bn = 'bn = (1/T)∫f(x)sin(nx)dx'

        heading = tk.Label(self.infoFrame,text = "Fourier Series",bg = "darkslateblue", fg = "white",font = self.font,padx = 78)
        heading.place(x = 10,y = 10)

		# show the formula
        formulaLabel = tk.Message(self.root,text = formula + '\n\n' + 'where\n\n' + a0 + '\n\n' + an  + '\n\n' + bn ,
                                bg = 'cornflowerblue',fg = 'white',font = self.font + (13,),width = self.width/4)
        formulaLabel.place(x = self.width/20,y = self.height/6)

        self.discInput()

    def discInput(self):
        #clear if anything
        for child in self.mainFrame.winfo_children():
            child.destroy()
        
        discontinuitiesLabel = tk.Label(self.mainFrame,text = "Enter number of discontinuities : ",bg = 'white',fg = 'black',font = ('Eras Medium ITC',15),pady = 5)
        discontinuitiesLabel.place(x = 0,y = 0)

        var = tk.IntVar()
        self.discontinuities = tk.Entry(self.mainFrame,textvariable = var,font = self.font,bg = 'gainsboro',width = 4)
        self.discontinuities.place(x = 350,y = 5)

        btn = tk.Button(self.mainFrame,text = "Submit",fg = 'white',bg = 'cornflowerblue',font = ('Eras Medium ITC',12),bd = 0,command = self.functionInput)
        btn.place(x = 475,y=3)

    def functionInput(self):
        try:
            numberOfFunctions = int(self.discontinuities.get())
            if numberOfFunctions == 0:
                return
        except ValueError:
            self.raiseError("Invalid arguement!")
            return
        functionsArray = []
        lowerLimitArray = []
        upperLimitArray = []
        for i in range(0,numberOfFunctions):
            functionLabel = tk.Label(self.mainFrame,text = "Enter function: ",font = ('Eras Medium ITC',15),
                                     pady = 3,padx = 3,bg = 'white')
            functionLabel.place(x = 0, y = 50 + i*40)

            function = tk.Entry(self.mainFrame,font = ('Eras Medium ITC',14),width = 14,bg = 'gainsboro')
            function.place(x = 160,y = 50 + i*40)
            functionsArray.append(function)
            
            lowerLimit = tk.Entry(self.mainFrame,font = ('Eras Medium ITC',14),width = 4,bg = 'gainsboro')
            lowerLimit.place(x = 350, y = 50 + i*40)
            lowerLimitArray.append(lowerLimit)
            
            label = tk.Label(self.mainFrame,text = " < x < ",font = ('Eras Medium ITC',15),padx = 5,bg='white')
            label.place(x = 403,y = 50+i*40)

            upperLimit = tk.Entry(self.mainFrame,font = ('Eras Medium ITC',14),width = 5,bg = 'gainsboro')
            upperLimit.place(x = 475, y = 50 + i*40)
            upperLimitArray.append(upperLimit)

        btn = tk.Button(self.mainFrame,text = "Submit",fg = 'white',bg = 'cornflowerblue',
                        font = ('Eras Medium ITC',12),bd = 0,
                        command = lambda a=functionsArray,b=lowerLimitArray,c=upperLimitArray: self.calculate(a,b,c))
        btn.place(x = 475,y = 100 + i*40)

    def calculate(self,a,b,c):
        a0,an,bn = self.calculator.doCalculations(a,b,c)
        flag = 0 # valid answer
        if a0==nan or an==nan or bn==nan:
            flag = 1 # invalid answer
        self.display(a0,an,bn,flag)

    def display(self,a0,an,bn,flag):
        for child in self.mainFrame.winfo_children():
            child.destroy()# optimize further

        if flag == 0:
            a0Answer = tk.Label(self.mainFrame,text = "Value of a0 : " + str(a0),bg='white',font = ('Eras Medium ITC',16))
            a0Answer.place(x = 10,y = 10)
            anAnswer = tk.Label(self.mainFrame,text = "Value of an : " + str(an),bg='white',font = ('Eras Medium ITC',16))
            anAnswer.place(x = 10,y = 60)
            bnAnswer = tk.Label(self.mainFrame,text = "Value of bn : " + str(bn),bg='white',font = ('Eras Medium ITC',16))
            bnAnswer.place(x = 10,y = 110)
    
            label = tk.Label(self.mainFrame,text = "Now use the formula given on the left side.",fg='cornflowerblue',bg='white',font = ('Eras Medium ITC',16))
            label.place(x = 10,y = 160)

        else:
            label = tk.Label(self.mainFrame,text = "Fourier Series does not exist !",bg='white',font = ('Eras Medium ITC',18))
            label.place(x = 100,y = 50)
            
        new = tk.Button(self.mainFrame,text = "Again",bg='cornflowerblue',fg='white',bd=0,font = ('Eras Medium ITC',16),command=self.discInput)
        new.place(x = 20,y = 8*self.height/10)

        EXIT = tk.Button(self.mainFrame,text = "  Exit  ",bg='cornflowerblue',fg='white',bd=0,font = ('Eras Medium ITC',16),command=lambda:exit())
        EXIT.place(x = 500,y = 8*self.height/10)
        
    def raiseError(self,message):
        window = tk.Toplevel(self.root)
        window.resizable(width = False,height = False)
        window["bg"] = 'white'
        label = tk.Message(window,text = message,fg = 'black',font = self.font + (25,),bg='white',
                           padx = 10,pady = 10)
        label.pack()
        window.after(1500,lambda: window.destroy())


    def __del__(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
