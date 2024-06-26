import customtkinter as tk
import CTkMessagebox
import random
import gtts
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image, ImageTk
from time import sleep
from CTkMessagebox import CTkMessagebox

root = tk.CTk()
root.geometry("1000x700")
root.resizable(False, False)
root.title("Spelling Bee")
root.config(bg="#22223b")

fontlabel = ("Cascadia Mono", 80, "bold")
fontbtn = ("Cascadia Mono", 40, "bold")
fontsmall = ("Cascadia Mono", 30, "bold")
prefontbtn = ("Cascadia Mono", 70, "bold")
prelabel = ("Cascadia Mono", 100, "bold")

bg = "#22223b"
tc = "#c9ada7"
fg = "#4a4e69"
hover = "#6b729c"

# the "correct!" / "not quite..." text is initialised here because it ensures duplicates of this element
# are not created when the game generates new questions, as if it were to be inside the main game's page, it would 
# be created, but there would be no way to remove this element without the user never seeing it.
correctlabel = tk.CTkLabel(root,
                           text="",
                           bg_color=bg,
                           font=fontsmall)
correctlabel.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

# gets all word from wordslist
with open("words.txt", "r") as file:
    wordslist = []
    for c in file:
        wordslist.append(c[0:len(c)-1]) # the string 
#

# generates one random word from the list of available words
def getRandom():
    global randomword
    randomword = str(wordslist[random.randint(0, len(wordslist))]).lower()
    print(randomword)
    getAudio()
#

# generates audio file for the random word
def getAudio():
    audio = gtts.gTTS(text=randomword, slow=False)
    audio.save("audio.mp3")
# plays the audio file of randomly generated word
def playAudio():
    global audio
    audio = AudioSegment.from_mp3("audio.mp3")
    play(audio)

def SpellingClear():
    scorelabel.destroy()
    audiobutton.destroy()
    useranswer.destroy()
    textbox.destroy()
    backbutton.destroy()

def PreGameClear():
    spellinglabel.destroy()
    start.destroy()
    questionbox.pack_forget()
    questionlabel.destroy()
    backbutton.destroy()

def postclear():
    welldone.destroy()
    scorelabel.destroy()
    backbutton.destroy()

def quitgame():
    if PageStatus == "spellingbee": 
        msg = CTkMessagebox(title="Are you sure you want to exit?", 
                            message="If you quit now you will lose your progress", 
                            icon="warning", 
                            option_1="Cancel", 
                            option_2="Yes")
        if msg.get() == "Yes":
            SpellingClear()
            correctlabel.configure(text="")
            homepage()
            return

    elif PageStatus == "post":
        postclear()
        homepage()

    elif PageStatus == "pre":
        PreGameClear()
        backbutton.destroy()
        homepage()

    else: 
        msg = CTkMessagebox(title="Warning!",
                            message="Are you sure you want to quit?", 
                            icon="warning",
                            option_1="Cancel", 
                            option_2="Yes")
        if msg.get() == "Yes":
            exit()

# checks the answer inputted from the user and checks if its correct
def checkans():
    global answer, score, correctlabel, questions
    answer = textbox.get().lower()
    if answer.replace(" ", "") == randomword:
        score = score + 1
        questions = questions + 1
        # print("Correct")
        # print(score)
        # print(questions)
        correctlabel.configure(text='Correct!', text_color="#09ff00")
        play(AudioSegment.from_wav("correct.wav"))
        SpellingClear()
        SpellingBee()

    else:
        # print("wrong")
        questions = questions + 1
        print(score)
        print(questions)
        correctlabel.configure(text="Not quite..", text_color="#b0b02c")
        play(AudioSegment.from_wav("incorrect.wav"))
        SpellingClear()
        SpellingBee()
 
# This whole function shows a different message after you finish a game with a different message depending on your score.
# If you get a score that is above 90%, you are shown "Amazing!!"
# If you get a score that is above 75%, you are shown "Nice Job!"
# If you get a score that is above 50%, you are shown "Nearly there.."
# If you get a score that is lower than 50%, you are shown "Better luck next time."
def post():
   global PageStatus, scorelabel, welldone, backbutton
   PageStatus = "post"
   correctlabel.configure(text="")
   backbutton = tk.CTkButton(root,
                            text="Back",
                            font=fontbtn,
                            hover=hover,
                            bg_color=bg,
                            fg_color=fg,
                            command=quitgame)
   backbutton.place(relx=0.02, rely=0.05, anchor=tk.W)
   scorelabel = tk.CTkLabel(root, 
                            text=(f"{score} / {questionslimit} correct."),
                            bg_color=bg,
                            font=fontsmall,
                            text_color="white")
   scorelabel.place(rely=0.55, relx=0.5, anchor=tk.CENTER)

   if (score) > (90 / 100 * questions):
       welldone = tk.CTkLabel(root, 
                              text="Amazing!!",
                              text_color="#11d14a",
                              bg_color=bg,
                              font=fontlabel)
       welldone.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

   elif (score) > (75 / 100 * questions): 
       welldone = tk.CTkLabel(root, 
                              text="Nice job!",
                              text_color="#5bc916",
                              bg_color=bg,
                              font=fontlabel)
       welldone.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

   elif (score) > (50 / 100 * questions):
       welldone = tk.CTkLabel(root,
                              text="Nearly there..",
                              text_color="#c4d10f",
                              bg_color=bg,
                              font=fontlabel)
       welldone.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

   else:
       welldone = tk.CTkLabel(root,
                              text="Better luck next time.",
                              text_color="#ba720d",
                              bg_color=bg,
                              font=fontbtn)
       welldone.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Spelling bee Ingame
def SpellingBee():
    global textbox, scorelabel, audiobutton, useranswer, correctlabel, questionslimit, PageStatus, backbutton
    PageStatus = "spellingbee"
    if questionslimit == None:
        PreGameClear()
        try:
            questionslimit = int(questionbox.get())
            if questionslimit > 0:
                questionbox.destroy()
            else: 
                CTkMessagebox(title="Error", message="You cannot have negative questions!", icon="cancel")
                questionslimit = None
                PreGame()
                return


        except:
            CTkMessagebox(title="Error", message="Please enter a number.", icon="cancel")
            PreGame()
            return


    if questions != questionslimit:
        getRandom()
        
        backbutton = tk.CTkButton(root,
                                text="Back",
                                font=fontbtn,
                                hover=hover,
                                bg_color=bg,
                                fg_color=fg,
                                command=quitgame)
        backbutton.place(relx=0.02, rely=0.05, anchor=tk.W)

        scorelabel = tk.CTkLabel(root,
                                    text="",
                                    bg_color = bg,
                                    text_color=tc,
                                    font=("Chilanka", 30, "bold"))
        scorelabel.place(relx= 0.858, rely=0.01)
        scorelabel.configure(text=f"Score: {score}")

        audioimage = ImageTk.PhotoImage(Image.open("audiobutton.png"))
        audiobutton = tk.CTkButton(root,
                                    image=audioimage,
                                    text="",
                                    width = 300,
                                    height = 300,
                                    bg_color=bg,
                                    fg_color=fg,
                                    hover_color=hover,
                                    command = playAudio)
        audiobutton.pack(pady=(100,80))

        textbox = tk.CTkEntry(root,
                                placeholder_text="Spell the word here..",
                                font=fontbtn,
                                width = 700,
                                height = 50,
                                corner_radius=10,
                                bg_color=bg)
        textbox.pack()

        useranswer = tk.CTkButton(root,
                                text='Check',
                                font=fontbtn,
                                bg_color=bg,
                                fg_color=fg,
                                hover_color=hover,
                                width = 200,
                                height=50,
                                command=checkans)
        useranswer.pack(pady=30)

    else:
        print("finished")
        print(f"{score} / {questionslimit}")
        post()  
#

def PreGame():
# Spelling bee pregame
    global spellinglabel, start, questionbox, questionlabel, PageStatus, backbutton

    introlabel.place_forget()
    spellingbtn.pack_forget()
    quitbtn.pack_forget()

    PageStatus="pre"

    backbutton = tk.CTkButton(root,
                              text="Back",
                              font=fontbtn,
                              hover=hover,
                              bg_color=bg,
                              fg_color=fg,
                              command=quitgame)
    backbutton.place(relx=0.02, rely=0.05, anchor=tk.W)
    

    spellinglabel = tk.CTkLabel(root,
                            text="Spelling Bee",
                            font=(prelabel),
                            bg_color=(bg),
                            text_color=tc)
    spellinglabel.pack(pady=(90,80))

    questionlabel = tk.CTkLabel(root,
                                text="How many questions?",
                                font=fontsmall,
                                bg_color=bg,
                                text_color=tc)
    questionlabel.pack(pady=(0,1))

    questionbox = tk.CTkEntry(root,
                              font=(fontbtn),
                              bg_color=(bg),
                              height=50,
                              width=100,)
    questionbox.pack(pady=10)


    start = tk.CTkButton(root,
                         text="Play",
                         width=350,
                         height=125,
                         font=prefontbtn,
                         fg_color=fg,
                         bg_color=bg,
                         hover_color=hover,
                         corner_radius=7,
                         border_width=5,
                         border_color="white",
                         command=SpellingBee)
    start.pack(pady=(30,0))
#


# Home Page
def homepage():
    global introlabel, spellingbtn, quitbtn, score, questions, PageStatus, answer, questionslimit
    score = 0
    questions = 0
    questionslimit = None
    answer = None
    PageStatus = "home"
    introlabel = tk.CTkLabel(root, 
                                text="Spelling Bee",
                                font=(fontlabel),
                                bg_color=bg,
                                text_color=tc)
    introlabel.place(relx = 0.5, rely=0.25, anchor = tk.CENTER)

    spellingbtn = tk.CTkButton(root, 
                                text="Play", 
                                width=350, 
                                height=125, 
                                font=(fontbtn),
                                fg_color=(fg),
                                hover_color=hover,
                                corner_radius=7,
                                border_width=5,
                                border_color="white",
                                bg_color=bg,
                                command=PreGame)
    spellingbtn.pack(pady=(300,0))

    quitbtn = tk.CTkButton(root, 
                                text="Quit", 
                                width=150, 
                                height=40, 
                                font=(fontbtn),
                                fg_color=fg,
                                hover_color="#de4046",
                                corner_radius=5,
                                border_width=5,
                                border_color="white",
                                bg_color=bg,
                                command=quitgame)
    quitbtn.pack(pady=(160,0))
homepage()
#

root.mainloop()