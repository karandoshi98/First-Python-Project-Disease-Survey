import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk
import csv as csv

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


from ml import ML
import sqlite3
import pandas as pd


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=25, weight="bold", slant="italic")
        self.wm_title("Hospital")
        self.wm_geometry("600x400")
        # the container is whee we'll stack a bunch of frames
        # on top of each other,r then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, Details, GraphOne, GraphTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.configure(background='#A9A9A9')
        label = tk.Label(self, text="SURVEY FOR DISEASES", font=controller.title_font)
        label.pack(side="top", fill="x", pady=40)

        button1 = tk.Button(self, text="CLICK, to view Graphs",
                            command=lambda: controller.show_frame("PageOne"), font=10)
        button2 = tk.Button(self, text="CLICK, to Enter your Disease",
                            command=lambda: controller.show_frame("PageTwo"), font=10)
        button3 = tk.Button(self, text="Display details for a patient",
                            command=lambda: controller.show_frame("Details"), font=10)
        button1.pack(pady=20)
        button2.pack(pady=20)
        button3.pack(pady=20)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Graph Page", font = controller.title_font)
        label.pack(side="top", fill="x", pady=40)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=20)
        button1 = tk.Button(self, text="Disease vs Age Graph",
                            command=lambda: controller.show_frame("GraphOne"))
        button1.pack(pady=15)
        button2 = tk.Button(self, text="Disease vs Average-age Graph",
                            command=lambda: controller.show_frame("GraphTwo"))
        button2.pack(pady=15)


class GraphOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Age vs Disease", font = controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("PageOne"))
        button.pack(side="bottom", pady=10)
        import sqlite3
        conn = sqlite3.connect('proj.db')
        c = conn.cursor()
        c.execute("SELECT age FROM hospital order by age")
        age2 = c.fetchall()
        c.execute("SELECT disease FROM hospital order by age")
        die2 = c.fetchall()
        age3 = []
        for i in range(len(age2)):
            age3.append(str(age2[i][0]))
        die3 = []
        for i in range(len(die2)):
            die3.append(str(die2[i][0]))
        conn.commit()
        conn.close()

        f = Figure(figsize=(10, 10), dpi=80)
        a = f.add_subplot(111)
        a.set_xlabel("Disease")
        a.set_ylabel("Age")
        width = 0.5
        bar_g = a.bar(die3, age3, width)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class GraphTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Average-age vs Disease", font = controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("PageOne"))
        button.pack(side="bottom", pady=10)
        import sqlite3
        conn = sqlite3.connect('proj.db')
        c = conn.cursor()
        c.execute("SELECT avg(age) FROM hospital group by disease order by age")
        age2 = c.fetchall()
        c.execute("SELECT disease FROM hospital group by disease order by age")
        die2 = c.fetchall()
        age3 = []
        for i in range(len(age2)):
            age3.append(str(age2[i][0]))

        die3 = []
        for i in range(len(die2)):
            die3.append(str(die2[i][0]))

        conn.commit()
        conn.close()

        f = Figure(figsize=(10, 10), dpi=80)
        a = f.add_subplot(111)
        a.set_xlabel("Disease")
        a.set_ylabel("Avg age")
        width = 0.5
        bar_g = a.bar(die3, age3, width)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Hospital", font=controller.title_font)
        label.pack(side="top", fill="x", pady=40)

        self.Label1 = tk.Label(self)
        self.Label1.place(relx=0.19, rely=0.27, height=28, width=56)
        self.Label1.configure(text="Name:")
        self.Label1.configure(width=56)

        self.Label2 = tk.Label(self)
        self.Label2.place(relx=0.19, rely=0.35, height=28, width=46)
        self.Label2.configure(text='''Age:''')
        self.Label2.configure(width=46)

        self.Label3 = tk.Label(self)
        self.Label3.place(relx=0.19, rely=0.43, height=28, width=56)
        self.Label3.configure(text='''Email:''')
        self.Label3.configure(width=56)

        self.Label4 = tk.Label(self)
        self.Label4.place(relx=0.02, rely=0.51, height=28, width=276)
        self.Label4.configure(text='''From which year you are having the disease:''')
        self.Label4.configure(width=350)

        self.Text1 = tk.Text(self)
        self.Text1.place(relx=0.6, rely=0.27, relheight=0.07, relwidth=0.30)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(width=86)


        self.Text2 = tk.Text(self)
        self.Text2.place(relx=0.6, rely=0.35, relheight=0.07, relwidth=0.30)
        self.Text2.configure(background="white")
        self.Text2.configure(font="TkTextFont")
        self.Text2.configure(selectbackground="#c4c4c4")
        self.Text2.configure(width=86)
        # Text2.configure(wrap=WORD)

        self.Text3 = tk.Text(self)
        self.Text3.place(relx=0.6, rely=0.43, relheight=0.07, relwidth=0.30)
        self.Text3.configure(background="white")
        self.Text3.configure(font="TkTextFont")
        self.Text3.configure(selectbackground="#c4c4c4")
        self.Text3.configure(width=86)
        # Text3.configure(wrap=WORD)

        self.Text4 = tk.Text(self)
        self.Text4.place(relx=0.6, rely=0.51, relheight=0.07, relwidth=0.30)
        self.Text4.configure(background="white")
        self.Text4.configure(font="TkTextFont")
        self.Text4.configure(selectbackground="#c4c4c4")
        self.Text4.configure(width=86)
        # Text4.configure(wrap=WORD)

        self.Label6 = tk.Label(self)
        self.Label6.place(relx=0.17, rely=0.59, height=28, width=76)
        self.Label6.configure(text='''Disease:''')
        self.Label6.configure(width=76)

        self.Button1 = tk.Button(self)
        self.Button1.place(relx=0.18, rely=0.80, height=28, width=70)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Submit''')
        self.Button1.configure(command=self.submit)

        self.Button2 = tk.Button(self)
        self.Button2.place(relx=0.45, rely=0.80, height=28, width=70)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(text='''Cancel''')
        self.Button2.configure(command=self.cancel)

        self.Button3 = tk.Button(self)
        self.Button3.place(relx=0.70, rely=0.80, height=28, width=70)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(text='''Back''')
        self.Button3.configure(command=lambda: controller.show_frame("StartPage"))

        self.TCombobox1 = ttk.Combobox(self)
        self.TCombobox1.place(relx=0.6, rely=0.59, relheight=0.07, relwidth=0.30)

        self.TCombobox1.configure(width=97)
        self.TCombobox1.configure(takefocus="")
        self.TCombobox1.set('Choose')
        self.TCombobox1['values'] = (
            'Stroke', 'Cancer', 'Heart Disease', 'Malaria', 'Diabetes', 'Tumor', 'Asthma', 'Diarrhea', 'Depression',
            'Flu')

    name1 = ''
    age1 = ''
    email1 = ''
    d_year1 = ''
    dropdown1 = ''
    d_type = ''

    def submit(self):
        harmfull = ['Stroke', 'Cancer', 'Heart Disease', 'Diabetes', 'Tumor']
        import sqlite3
        conn = sqlite3.connect('proj.db')
        self.name1 = self.Text1.get('1.0', tk.END)
        self.age1 = self.Text2.get('1.0', tk.END)
        self.email1 = self.Text3.get('1.0', tk.END)
        self.d_year1 = self.Text4.get('1.0', tk.END)
        self.dropdown1 = self.TCombobox1.get()

        for i in harmfull:
            if i == self.dropdown1:
                self.d_type = 'Deadly'
                break
            else:
                self.d_type = 'Not deadly'

        if len(self.name1) == 0 or len(self.age1) == 0 or len(self.email1) == 0 or len(self.d_year1) == 0 or len(self.dropdown1) == 0 or self.dropdown1 == 'Choose':
            import tkinter.messagebox
            tkinter.messagebox.showinfo('Warning', 'Please fill all the boxes')
        elif len(self.name1) != 0 and len(self.age1) != 0 and len(self.email1) != 0 and len(self.d_year1) != 0 and len(self.dropdown1) != 0 and self.dropdown1 != 'Choose':
            c = conn.cursor()
            c.execute("INSERT INTO hospital VALUES(?,?,?,?,?,?)",
                      (self.name1, self.age1, self.dropdown1, self.email1, self.d_year1, self.d_type,))

            c.execute("SELECT age,d_year,disease FROM hospital WHERE name=(?)", [self.name1])
            list1 = []
            for i in c.fetchall():
                list1.append(i)
            conn.commit()
            conn.close()

            # with open("data.csv", "r") as f:
            #     cw = csv.reader(f, delimiter = ' ')
            #     for line in cw:
            #         if line[0]==self.name1:
            #             print(', '.join(line))
            #             break

            if list1[0][2] == 'Stroke':
                t=2
            elif list1[0][2] == 'Cancer':
                t = 3
            elif list1[0][2] == 'Heart Disease':
                t = 4
            elif list1[0][2] == 'Malaria':
                t = 5
            elif list1[0][2] == 'Diabetes':
                t = 6
            elif list1[0][2] == 'Tumor':
                t = 7
            elif list1[0][2] == 'Asthma':
                t = 8
            elif list1[0][2] == 'Diarrhea':
                t = 9
            elif list1[0][2] == 'Depression':
                t = 10
            elif list1[0][2] == 'Flu':
                t = 11
            else:
                t=0
            a = list1[0][0]
            y = list1[0][1]
            t1 = t
            obj = ML()
            pred,accuracy = obj.preprocess(a, y, t1)
            print("Accuracy =",accuracy)
            import tkinter.messagebox
            if pred==0:
                tkinter.messagebox.showinfo('Thank You', 'We are sorry , Disease is DEADLY but Thank you for your response')
                self.cancel()
            elif pred==1:
                tkinter.messagebox.showinfo('Thank You', 'Disease is NOT DEADLY and Thank you for your response')
                self.cancel()

    def cancel(self):
        self.Text1.delete(1.0, tk.END)
        self.Text2.delete(1.0, tk.END)
        self.Text3.delete(1.0, tk.END)
        self.Text4.delete(1.0, tk.END)
        self.TCombobox1.set('Choose')


class Details(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(self)

        self.controller = controller
        label = tk.Label(self, text="Details", font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=30)

        self.Label1 = tk.Label(self)
        self.Label1.place(relx=0.02, rely=0.16, height=28, width=300)
        self.Label1.configure(text="Enter the name of the patient you want to find:")
        self.Label1.configure(width=56)

        self.Label2 = tk.Label(self)
        self.Label2.place(relx=0.19, rely=0.45, height=28, width=46)
        self.Label2.configure(text='''Age:''')
        self.Label2.configure(width=46)

        self.Label5 = tk.Label(self, font=10)
        self.Label5.place(relx=0.25, rely=0.32, height=40, width=300)
        self.Label5.configure(text='''Search Results:''')
        self.Label5.configure(width=100)

        self.Label3 = tk.Label(self)
        self.Label3.place(relx=0.19, rely=0.53, height=28, width=56)
        self.Label3.configure(text='''Disease:''')
        self.Label3.configure(width=56)

        self.Label4 = tk.Label(self)
        self.Label4.place(relx=0.02, rely=0.61, height=28, width=276)
        self.Label4.configure(text='''From which year patient has this disease:''')
        self.Label4.configure(width=276)

        self.Label6 = tk.Label(self)
        self.Label6.place(relx=0.17, rely=0.68, height=28, width=76)
        self.Label6.configure(text='''Email:''')
        self.Label6.configure(width=76)

        self.Text1 = tk.Text(self)
        self.Text1.place(relx=0.6, rely=0.16, relheight=0.07, relwidth=0.30)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(width=86)
        # Text1.configure(wrap=WORD)


        self.Text2 = tk.Text(self)
        self.Text2.place(relx=0.6, rely=0.45, relheight=0.07, relwidth=0.30)
        self.Text2.configure(background="white")
        self.Text2.configure(font="TkTextFont")
        self.Text2.configure(selectbackground="#c4c4c4")
        self.Text2.configure(width=86)
        # Text2.configure(wrap=WORD)

        self.Text3 = tk.Text(self)
        self.Text3.place(relx=0.6, rely=0.53, relheight=0.07, relwidth=0.30)
        self.Text3.configure(background="white")
        self.Text3.configure(font="TkTextFont")
        self.Text3.configure(selectbackground="#c4c4c4")
        self.Text3.configure(width=86)
        # Text3.configure(wrap=WORD)

        self.Text4 = tk.Text(self)
        self.Text4.place(relx=0.6, rely=0.61, relheight=0.07, relwidth=0.30)
        self.Text4.configure(background="white")
        self.Text4.configure(font="TkTextFont")
        self.Text4.configure(selectbackground="#c4c4c4")
        self.Text4.configure(width=86)

        self.Text5 = tk.Text(self)
        self.Text5.place(relx=0.6, rely=0.68, relheight=0.07, relwidth=0.30)
        self.Text5.configure(background="white")
        self.Text5.configure(font="TkTextFont")
        self.Text5.configure(selectbackground="#c4c4c4")
        self.Text5.configure(width=86)

        self.Button1 = tk.Button(self)
        self.Button1.place(relx=0.35, rely=0.26, height=28, width=70)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Submit''')
        self.Button1.configure(command=self.submit)

        self.Button1 = tk.Button(self)
        self.Button1.place(relx=0.55, rely=0.26, height=28, width=90)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Clear Search''')
        self.Button1.configure(command=self.clear)

    def submit(self):

        import sqlite3
        conn = sqlite3.connect('proj.db')
        c = conn.cursor()
        self.name1 = self.Text1.get('1.0', tk.END)
        c.execute("SELECT age,Disease,Email,d_year FROM hospital WHERE name=(?)", [self.name1])
        list1 = []
        for i in c.fetchall():
            list1.append(i)

        self.Text2.delete('1.0', tk.END)
        self.Text3.delete('1.0', tk.END)
        self.Text4.delete('1.0', tk.END)
        self.Text5.delete('1.0', tk.END)

        self.Text2.insert('1.0', list1[0][0])
        self.Text3.insert('1.0', list1[0][1])
        self.Text4.insert('1.0', list1[0][3])
        self.Text5.insert('1.0', list1[0][2])



        conn.commit()
        conn.close()

    def clear(self):
        self.Text1.delete('1.0', tk.END)
        self.Text2.delete('1.0', tk.END)
        self.Text3.delete('1.0', tk.END)
        self.Text4.delete('1.0', tk.END)
        self.Text5.delete('1.0', tk.END)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
