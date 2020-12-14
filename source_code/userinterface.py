from tkinter import *
import zoom_allocator
import database_create
import json


class Application(Frame):

    def db_command(self):
        self.Status_text.set("Updating the database...")
        root.update_idletasks()
        tabbyurl = self.Url_Entry.get()
        tournament = self.Tournament_Entry.get()
        token = self.Token_Entry.get()
        room_per_zoom = self.RPZ_Entry.get()

        if(tabbyurl[-1] == '/'):
            tabbyurl = tabbyurl[:-1]

        print(tabbyurl)

        database_create.user_input(
            tabbyurl, tournament, f'Token {token}', room_per_zoom)

        database_create.create()
        self.Status_text.set("Updated the database")

    def csv_command(self):
        zoom_allocator.round_number = self.Round_Entry.get()
        zoom_allocator.allocate()

    def createWidgets(self):
        db_frame = Frame(self)
        db_frame.pack(fill=X, padx=5, pady=10)

        input_frame = Frame(db_frame, relief=RAISED,
                            highlightbackground="black", highlightthickness=1)
        input_frame.pack(fill=X, padx=5, pady=10, side=LEFT)

        control_frame = Frame(self, relief=GROOVE)
        control_frame.pack(fill=X, padx=5, pady=10)

        self.db_Button = Button(
            db_frame, text="Update Database", command=self.db_command)
        self.db_Button.pack(side=RIGHT)

        self.csv_Button = Button(
            control_frame, text="Create Csv Files", command=self.csv_command)
        self.csv_Button.pack(side=RIGHT, pady=4, padx=5)

        Token_Frame = Frame(input_frame)
        Token_Frame.pack(fill=X, pady=4)
        self.Token_Label = Label(Token_Frame, text="Tabbycat Token")
        self.Token_Label.pack({"side": "left", "padx": "5"})
        self.Token_Entry = Entry(Token_Frame, width=50)
        self.Token_Entry.pack({"side": "right", "padx": "5"})

        Url_Frame = Frame(input_frame)
        Url_Frame.pack(fill=X, pady=4)
        self.Url_Label = Label(Url_Frame, text="Tabby Url")
        self.Url_Label.pack({"side": "left", "padx": "5"})
        self.Url_Entry = Entry(Url_Frame, width=50)
        self.Url_Entry.pack({"side": "right", "padx": "5"})

        Tournament_Frame = Frame(input_frame)
        Tournament_Frame.pack(fill=X, pady=4)
        self.Tournament_Label = Label(Tournament_Frame, text="Tournament Slug")
        self.Tournament_Label.pack({"side": "left", "padx": "5"})
        self.Tournament_Entry = Entry(Tournament_Frame)
        self.Tournament_Entry.pack({"side": "left", "padx": "5"})

        RPZ_Frame = Frame(input_frame)
        RPZ_Frame.pack(fill=X, pady=4)
        self.RPZ_Label = Label(RPZ_Frame, text="Room per Zoom Meeting")
        self.RPZ_Label.pack({"side": "left", "padx": "5"})
        self.RPZ_Entry = Entry(RPZ_Frame, width=12)
        self.RPZ_Entry.pack({"side": "left", "padx": "5"})

        Round_Frame = Frame(
            control_frame, highlightbackground="black", highlightthickness=1)
        Round_Frame.pack(fill=X)
        self.Round_Label = Label(Round_Frame, text="Round")
        self.Round_Label.pack({"side": "left", "padx": "5", "pady": "4"})
        self.Round_Entry = Entry(Round_Frame)
        self.Round_Entry.pack({"side": "right", "padx": "5", "pady": "4"})

        self.Status_Label = Label(self, textvariable=self.Status_text)
        self.Status_Label.pack(side=BOTTOM)

    def initial_text(self):
        try:
            with open("inputs.json") as f:
                inputs = json.load(f)
                self.Token_Entry.insert(INSERT, inputs["token"][6:])
                self.Url_Entry.insert(INSERT, inputs["tabbyurl"])
                self.Tournament_Entry.insert(INSERT, inputs["tournament"])
                self.RPZ_Entry.insert(INSERT, inputs["room_per_zoom"])
                print("hello1")
        except:
            pass

        self.Status_text.set("Ready")
        print("hello")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("Zoom Allocator")
        self.Status_text = StringVar()
        self.pack()
        self.createWidgets()
        self.initial_text()
        self.master.geometry("550x230")


root = Tk()
root.protocol("WM_DELETE_WINDOW", root.destroy)
app = Application(master=root)
app.mainloop()
try:
    root.destroy()
except:
    pass
