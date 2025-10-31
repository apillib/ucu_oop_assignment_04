from tkinter import * 
from tkinter.ttk import Button,Label,Entry, Style 
from tkinter import END 

class LoanCalculator(Toplevel): 

    def __init__(self, on_close_callback):
        Toplevel.__init__(self)
        self.on_close_callback = on_close_callback
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.initUI() 

    def initUI(self): 
        self.title("Loan Calculator") 
        self.geometry("300x300") 
        self.style = Style() 
        self.style.theme_use("default")  # default

        xpos = 40 
        ypos = 30 
        xpos2 = xpos+100 
        l1 = Label(self, text="Amount", foreground = "#ff0000", background = "light blue", font = "Arial 9")  # Arial 12 bold italic 
        l1.place(x=xpos, y=ypos) 
        self.txtAmount = Entry(self) 
        self.txtAmount.place(x=xpos2, y = ypos, width=70) 
 
        ypos += 30
        l2 = Label(self, text="Rate(%)", foreground = "#ff0000", background = "light blue", font = "Arial 9")  # Arial 12 bold italic 
        l2.place(x=xpos, y=ypos) 
        self.txtRate = Entry(self) 
        self.txtRate.place(x=xpos2, y = ypos) 

        ypos += 30 
        l3 = Label(self, text="Duration(months)", foreground = "#ff0000", background = "light blue", font = "Arial 9")  # Arial 12 bold italic 
        l3.place(x=xpos, y=ypos) 
        self.txtDuration = Entry(self) 
        self.txtDuration.place(x=xpos2, y = ypos) 

        ypos += 30 
        l4 = Label(self, text="Monthly Payment", foreground = "#ff0000", background = "yellow", font = "Arial 9")  # Arial 12 bold italic 
        l4.place(x=xpos, y=ypos) 
        self.txtMonthlyPayment = Entry(self) 
        self.txtMonthlyPayment.configure(state="readonly") 
        self.txtMonthlyPayment.place(x=xpos2, y = ypos) 

        ypos += 30 
        l5 = Label(self, text="Total Payments", foreground = "#ff0000", background = "yellow", font = "Arial 9")  # Arial 12 bold italic 
        l5.place(x=xpos, y=ypos) 
        self.txtTotalPayment = Entry(self); 
        self.txtTotalPayment.configure(state="readonly") 
        self.txtTotalPayment.place(x=xpos2, y = ypos) 

        ypos += 30 
        style = Style()
        style.configure("Exit.TButton", foreground="red", background="white")

        #T.Checkbutton for checkboxes 
        style.configure("MainButton.TButton", foreground="yellow", background="red") 

        calcButton = Button(self, text="Calculate", command=self.calcButtonClick) 
        calcButton.configure(style="MainButton.TButton") 
        calcButton.place(x=xpos2, y=ypos)

        clearButton = Button(self, text="Clear", command=self.clearFields)
        clearButton.place(x=xpos2+80, y=ypos)

        saveButton = Button(self, text="Save Details", command=self.saveValues)
        self.saveDetails = False
        saveButton.place(x=xpos, y=ypos)

        #exitButton = Button(self, text="Close", command=self.destroy)
        #exitButton.configure(style="Exit.TButton") 
        #exitButton.place(x=xpos, y=ypos) 
 
    # set values
    def setValues(self, amount, rate, duration):
        self.txtAmount.configure(state="normal")
        self.txtAmount.delete(0, END)
        self.txtAmount.insert(0,amount)

        self.txtDuration.configure(state="normal")
        self.txtDuration.delete(0, END)
        self.txtDuration.insert(0,duration)

        self.txtRate.configure(state="normal")
        self.txtRate.delete(0, END)
        self.txtRate.insert(0,rate)
        
    def calcButtonClick(self): 
        amt = float(self.txtAmount.get()) 
        rate = float(self.txtRate.get()) 
        dur = float(self.txtDuration.get()) 
        monthlyPayment = amt * (rate / 1200.0) * ((rate / 1200 + 1)** dur) / (((rate / 1200 + 1)** dur) - 1) 
        totalPayment = amt * ((1 + rate / 1200) ** dur); 

        self.txtMonthlyPayment.configure(state="normal")  # has to be turned back to normal otherwise, data is not modified 
        self.txtMonthlyPayment.delete(0,END)
        self.txtMonthlyPayment.insert(0,format(monthlyPayment, "0.2f")) 
        self.txtMonthlyPayment.configure(state="readonly") 

        self.txtTotalPayment.configure(state="normal") 
        self.txtTotalPayment.delete(0,END) 
        self.txtTotalPayment.insert(0,format(totalPayment, "0.2f")) 
        self.txtTotalPayment.configure(state="readonly")

    def isSaveDetails(self):
        return self.saveDetails

    def saveValues(self):
        self.saveDetails = True
        self.on_close()

    def on_close(self):
        self.on_close_callback()

    def getSavedDetails(self):
        savedDetails = {
            "Amount" : float(self.txtAmount.get()),
            "Rate" : float(self.txtRate.get()),
            "Duration" : float(self.txtDuration.get()),
            "MonthlyPayment" : float(self.txtMonthlyPayment.get()),
            "TotalPayment" : float(self.txtTotalPayment.get())
        }
        return savedDetails

    def clearFields(self):
        for field in [self.txtAmount, self.txtRate, self.txtDuration,
                    self.txtMonthlyPayment, self.txtTotalPayment]:
            field.configure(state="normal")
            field.delete(0, END)
            if field in [self.txtMonthlyPayment, self.txtTotalPayment]:
                field.configure(state="readonly")
