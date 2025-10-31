from tkinter.ttk import Frame, Button,Label,Entry, Style 
from tkinter import BOTH,END, messagebox, ttk
from StudentIDDlg import StudentIDDlg
from LoanCalculator import LoanCalculator
from FeedBackDlg import FeedBackDlg
from PIL import Image
import matplotlib.pyplot as plt
from tkinter import Menu, BOTH,END,NONE, messagebox, filedialog, Label
import json
import pprint

class MyFrame(Frame): 

    def __init__(self, parent): 
        Frame.__init__(self, parent)   
        ttk.Style().theme_use("clam") 
        self.parent = parent 
        self.LCD = None #loan Calculator Object
        self.FBD = None   #Feedback Dlg object
        self.loanDetails = {}
        self.initUI()
         
    def initUI(self): 
        self.parent.title("Student Loan Processor") 
        self.style = Style() 
        self.style.theme_use("default")   
        self.pack(fill=BOTH, expand=1) 
        #-------------------------------------------- 

        #--------------------create menus------------ 
        menuBar = Menu(self.parent)
        mnuFile = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="File", menu=mnuFile)
        mnuFile.add_command(label="Open", command=self.load_json)
        mnuFile.add_command(label="Save", command=self.mnuSaveFileClick)
        mnuFile.add_separator()
        mnuFile.add_command(label="Exit", command=self.exitButtonClick)
 
        mnuCustomers = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Loan Processing", menu=mnuCustomers)
        mnuCustomers.add_command(label="Loan Calculator", command=self.loanCalcButtonClick)
        mnuCustomers.add_separator()
        mnuCustomers.add_command(label="Provide Feedback", command=self.mnuShowFeedbackClick)

        self.parent.config(menu=menuBar) 
        #--------------------------------------------

        xpos = 30 
        ypos = 40 
        xpos2 = xpos + 90 

        #------------styling---------------------------------- 
        style = Style() 
        style.configure("Exit.TButton", foreground="red", background="white")    
        style.configure("MainButton.TButton", foreground="yellow", background="red") 
        
        #----------------------------------------------------- 
        testButton = Button(self, text="Get StudentID", command=self.btnGetStudentIDClick) 
        testButton.configure(style="MainButton.TButton") 
        testButton.place(x=xpos, y=ypos) 

        self.txtID = Entry(self, text="", foreground = "#ff0000", background = "light blue", font = "Arial 9")  # Arial 12 bold italic 
        self.txtID.place(x=xpos2, y=ypos)
        self.txtID.configure(state="readonly") 

        ypos += 30
        self.btnLoanCalc = Button(self, text="Loan Calculator", command=self.loanCalcButtonClick) 
        self.btnLoanCalc.configure(style="Exit.TButton") 
        self.btnLoanCalc.place(x=xpos, y=ypos) 

        #ypos += 30
        #ypos += 30 
        #exitButton = Button(self, text="Exit", command=self.exitButtonClick) 
        #exitButton.configure(style="Exit.TButton") 
        #exitButton.place(x=xpos, y=ypos)
        #self.after()

    def update_frame(self):
        self.btnLoanCalc.place_forget()

        # display the saved details
        self.loanString = Label(self, text=pprint.pformat(self.loanDetails, indent=2), font=("Arial", 12), bg="lightblue")
        self.loanString.pack(pady=10)  
        self.loanString.place(x=30, y=120)

        self.resetButton = Button(self, text="Reset", command=self.resetCalculator)
        self.resetButton.place(x=30, y=80)

    def resetCalculator(self):
        self.btnLoanCalc.place(x=30, y=80)
        self.resetButton.place_forget()

        self.loanDetails = {}
        self.loanString.place_forget()

        if (self.LCD is None):
            self.LCD.saveDetails = False 
        else:
            self.LCD.saveDetails = False 
 
    def exitButtonClick(self): 
        if (messagebox.askokcancel("OK to close?","Close application?")): 
            self.parent.destroy 
            exit()  # needed to close the main frame 

    def btnGetStudentIDClick(self):
        dlg = StudentIDDlg("your ID", "Student ID", "Please Enter your Student ID:") 

        #show modal dialog and collect student ID 
        dlg.grab_set()  #events only go to the modal dialog 
        self.wait_window(dlg) 

        self.txtID.configure(state="normal") 
        self.txtID.delete(0,END) 
        self.txtID.insert(0,dlg.getID()) 
        self.txtID.configure(state="readonly") 
        print(dlg.getID())

    def loanCalcButtonClick(self):
        if (self.LCD is None): 
            self.LCD = LoanCalculator(self.on_LCD_close)
        else:
            if (self.LCD.winfo_exists()):
                self.LCD.focus()
            else:
                self.LCD = LoanCalculator(self.on_LCD_close)

    def mnuOpenFileClick(self): 
        options = opts = {} 
        opts['initialdir'] = 'd:\\PythonRM' 
        opts['filetypes'] = [('all files', '.*'), ('jpeg files', '.jpg')] 
        fname = filedialog.askopenfilename(**options) # file in read mode
        img = Image.open(fname)
        plt.imshow(img)
 
    def mnuSaveFileClick(self): 
        print("OK")

        file_path = filedialog.asksaveasfilename(defaultextension=".json", 
                                             filetypes=[("JSON files", "*.json")])
        
        if file_path:
            with open(file_path, 'w') as json_file:
                json.dump(self.loanDetails, json_file, indent=4)
            print(f"Data saved to {file_path}")

    def mnuShowFeedbackClick(self):
        if (self.FBD is None):
            self.FBD = FeedBackDlg()
        else:
            if (self.FBD.winfo_exists()):
                self.LCD.focus() 
            else:
                self.FBD = FeedBackDlg()

    def load_json(self):
        # Open a file dialog to select a JSON file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                print("Data got")
                print(data)
                id = data['Student_ID']
                print("ID: ", id)
                self.txtID.configure(state="normal") 
                self.txtID.delete(0, END) #deletes the current value
                self.txtID.insert(0, id)
                self.txtID.configure(state="readonly") 
                print("ID set right")
                self.loanCalcButtonClick()
                self.LCD.setValues(data['Amount'],data['Rate'],data['Duration'])
            
    def on_LCD_close(self):
        print("Checking the savedDetails???? --- ", self.LCD.isSaveDetails())
        if (self.LCD and self.LCD.isSaveDetails()):
            print("Details savedL ")
            self.loanDetails = self.LCD.getSavedDetails()
            self.loanDetails['Student_ID'] = int(self.txtID.get())
            print(self.LCD.getSavedDetails())
            # close the dialog
            self.LCD.destroy()
            self.update_frame()
        else:
            print('Nothing saved')
            self.LCD.destroy()