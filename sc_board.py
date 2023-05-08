import tkinter as tk
from tkinter import font
import time
               
title_label_widget = None
team1_label_widget = None
team2_label_widget = None
team1_score_label_widget = None
team2_score_label_widget = None
game_time_label_widget = None
attack_time_label_widget = None
attack_time_label_2_widget = None
vs_label_widget = None
result_label_widget = None
game_time_label_2_widget = None


def increase_score(score_var, label):
    score_var.set(str(int(score_var.get()) + 1))
    update_result_label()

def decrease_score(score_var, label):
    score_var.set(str(int(score_var.get()) - 1))
    update_result_label()

def update_result_label():
    if "result_label" in globals():
        result_label.config(text=f"{team1_score.get()}   :   {team2_score.get()}")
        # attack_game_time_label_2.config(text=f"{attack_time_entry.get()}")  # 추가된 부분

def countdown(count, attack_count):
    global paused, attack_game_time_label_2
    if count >= 0 and not paused:
        if attack_count == 0:
            print("Attack time!")
            
        mins, secs = divmod(count, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        game_time_entry.delete(0, 'end')
        game_time_entry.insert(0, time_format)
        game_time_label_2.config(text=f"{time_format}")
        print("경기시간 : ", count)
        print("어택잔여시간 : ", attack_count)

        
        # 공격시간 카운트 다운 변경
        if attack_count > 0:
            attack_mins, attack_secs = divmod(attack_count, 60)
            attack_time_format = '{:02d}:{:02d}'.format(attack_mins, attack_secs)
            attack_game_time_label_2.config(text=f"{attack_time_format}")
            attack_time_entry.delete(0, 'end')
            attack_time_entry.insert(0, attack_time_format)        
            second_window.after(1000, countdown, count-1, attack_count-1)

        else:
            attack_game_time_label_2.config(text="00:00")
            attack_time_entry.delete(0, 'end')
            attack_time_entry.insert(0, '00:00')
            second_window.after(1000, countdown, count-1, attack_count)

    elif count < 0:
        game_time_entry.delete(0, 'end')
        game_time_entry.insert(0, '00:00')
        game_time_label_2.config(text="00:00")
       
        
        
def destroy_second_window():
    global second_window, paused
    second_window.destroy()
    del second_window
    paused = False

def show_result():
    global second_window, game_time_label_2, result_label, competition_label, team1_name_label, team2_name_label,vs_label, attack_game_time_label_2, game_ended_label  # 변경된 부분

    if "second_window" in globals() and second_window.winfo_exists():
        second_window.lift()
        return

    second_window = tk.Toplevel(app)
    second_window.geometry("1450x650-500+140")
    second_window.title("SCOREBOARD")
    second_window.protocol("WM_DELETE_WINDOW", destroy_second_window)

    competition_label = tk.Label(second_window, text=title_entry.get(), font=title_font_large)
    competition_label.pack(pady=10)
    
    name_frame = tk.Frame(second_window)
    name_frame.pack(pady=10)

    team1_name_frame = tk.Canvas(name_frame, width=750, height=115)
    team1_name_frame.pack(side="left")

    team1_name_label = tk.Label(team1_name_frame, text=team1_entry.get()[:5], font=team_font_large, fg="blue")
    team1_name_label.place(relx=0.5, rely=0.5, anchor="center")
    
    team2_name_frame = tk.Canvas(name_frame, width=750, height=115)
    team2_name_frame.pack(side="right")

    team2_name_label = tk.Label(team2_name_frame, text=team2_entry.get()[:5], font=team_font_large, fg="red")
    team2_name_label.place(relx=0.5, rely=0.5, anchor="center")
    
    vs_frame = tk.Canvas(name_frame, width=200, height=95)
    vs_frame.pack(side="bottom")
    
    vs_label = tk.Label(name_frame, text="vs", font=team_font_large)
    vs_label.place(relx=0.5, rely=0.5, anchor="center")

    result_label = tk.Label(second_window, text=f"{team1_score.get()}   :   {team2_score.get()}", font=score_font_large)
    result_label.pack(pady=10)

    game_time_label_2 = tk.Label(second_window, text=game_time_entry.get(), font=time_font_large)
    game_time_label_2.pack(side="left", pady=10)
    
    attack_game_time_label_2 = tk.Label(second_window, text=attack_time_entry.get(), font=attack_font)
    attack_game_time_label_2.pack(side="right", pady=10)
    

    
    
def start_game():
    global paused, attack_count
    paused = False
    game_time = int(game_time_entry.get().split(':')[0]) * 60 + int(game_time_entry.get().split(':')[1])
    attack_count = int(attack_time_entry.get().split(':')[0]) * 60 + int(attack_time_entry.get().split(':')[1])
    countdown(game_time, attack_count)
    
# 공수전환 관련 코드
def reset_attack_time(event=None):
    global attack_count, paused
    attack_count = int(attack_time_entry.get().split(':')[0]) * 60 + int(attack_time_entry.get().split(':')[1])
    print("이놈이야 : ", attack_count)
    if not paused:
        countdown(int(game_time_entry.get().split(':')[0]) * 60 + int(game_time_entry.get().split(':')[1]), attack_count)
        print("이놈이야2 : ", attack_count)
    else:
        paused = False
        attack_count = int(attack_time_entry.get().split(':')[0]) * 60 + int(attack_time_entry.get().split(':')[1])
        countdown(int(game_time_entry.get().split(':')[0]) * 60 + int(game_time_entry.get().split(':')[1]), attack_count)
        if attack_count < 20:
            attack_count = 20
            countdown(int(game_time_entry.get().split(':')[0]) * 60 + int(game_time_entry.get().split(':')[1]), attack_count)


        print("이놈이야3 : ", attack_count)
        paused = True


def toggle_pause(event=None):
    global paused, count
    paused = not paused
    if not paused:
        count = int(game_time_entry.get().split(':')[0]) * 60 + int(game_time_entry.get().split(':')[1])
        attack_count = int(attack_time_entry.get().split(':')[0]) * 60 + int(attack_time_entry.get().split(':')[1])
        if "count" in globals():
            countdown(count, attack_count)
        else:
            countdown(count, attack_count)
        game_time_entry.config(state="disabled")
    else:
        game_time_entry.config(state="normal")
        
def apply_changes():
    if "second_window" in globals():
        update_info()
        if not second_window.winfo_exists():
            show_result()
    else:
        show_result()

def update_info():
    if "competition_label" in globals():
        competition_label.config(text=title_entry.get())
        team1_name_label.config(text=team1_entry.get()[:5])
        team2_name_label.config(text=team2_entry.get()[:5])



app = tk.Tk()
app.title("ScoreBorad Input")
app.geometry("1200x550-500+140")
app.resizable(True, True)

title_font = font.Font(size=40)
team_font = font.Font(size=40)
score_font = font.Font(size=40)
custom_font = font.Font(size=25)

title_font_large = font.Font(size=75, weight='bold')
team_font_large = font.Font(size=100, weight='bold')
score_font_large = font.Font(size=210, weight='bold')
time_font_large = font.Font(size=130, weight='bold')
attack_font = font.Font(size=80, weight='bold')


title_label = tk.Label(app, text="TITLE", font=title_font)
title_label.grid(row=0, column=1, sticky='e')

title_entry = tk.Entry(app, width=30, font=title_font)
title_entry.grid(row=0, column=2, columnspan=2, sticky='w')

team1_label = tk.Label(app, text="BLUE", font=team_font, fg="blue")
team1_label.grid(row=1, column=1, sticky='e')

team1_entry = tk.Entry(app, width=12, font=team_font)
team1_entry.grid(row=1, column=2, sticky='w')

team2_label = tk.Label(app, text="RED:", font=team_font, fg="red")
team2_label.grid(row=1, column=3, sticky='e')

team2_entry = tk.Entry(app, width=12, font=team_font)
team2_entry.grid(row=1, column=4, sticky='w')

team1_score_label = tk.Label(app, text="Point", font=score_font)
team1_score_label.grid(row=2, column=1, sticky='e')

team1_score = tk.StringVar()
team1_score.set("0")
team1_score_entry = tk.Entry(app, width=2, textvariable=team1_score, font=score_font, justify='right')
team1_score_entry.grid(row=2, column=2, sticky='w')

team1_increase_button = tk.Button(app, text="▲", command=lambda: increase_score(team1_score, result_label), font=custom_font)
team1_increase_button.grid(row=2, column=2, sticky='e')

team1_decrease_button = tk.Button(app, text="▼", command=lambda: decrease_score(team1_score, result_label), font=custom_font)
team1_decrease_button.grid(row=3, column=2, sticky='e')

team2_score_label = tk.Label(app, text="Point", font=score_font)
team2_score_label.grid(row=2, column=3, sticky='e')

team2_score = tk.StringVar()
team2_score.set("0")
team2_score_entry = tk.Entry(app, width=2, textvariable=team2_score, font=score_font, justify='right')
team2_score_entry.grid(row=2, column=4, sticky='w')

team2_increase_button = tk.Button(app, text="▲", command=lambda: increase_score(team2_score, result_label), font=custom_font)
team2_increase_button.grid(row=2, column=4, sticky='e')

team2_decrease_button = tk.Button(app, text="▼", command=lambda: decrease_score(team2_score, result_label), font=custom_font)
team2_decrease_button.grid(row=3, column=4, sticky='e')

game_time_label = tk.Label(app, text="Game_Time", font=score_font)
game_time_label.grid(row=4, column=1, sticky='e')

game_time_entry = tk.Entry(app, width=5, font=score_font)
game_time_entry.insert(0, "03:00")
game_time_entry.grid(row=4, column=2, sticky='w')

result_button = tk.Button(app, text="Apply", command=apply_changes, font=custom_font)
result_button.grid(row=5, column=2, sticky='w')


start_button = tk.Button(app, text="START", command=start_game, font=custom_font)
start_button.grid(row=5, column=3, sticky='w')


# 추가/변경되는 부분
attack_time_label = tk.Label(app, text="Att_Time", font=custom_font)
attack_time_label.grid(row=4, column=3, sticky='e')  # 추가

attack_time_entry = tk.Entry(app, width=5, font=score_font)
attack_time_entry.insert(0, "00:20")  # 변경
attack_time_entry.grid(row=4, column=4, sticky='w')  # 변경
apply_changes()

pause_button = tk.Button(app, text="Pause", command=toggle_pause, font=custom_font)
pause_button.grid(row=5, column=4, sticky='w')

switch_button = tk.Button(app, text="Switching", command=reset_attack_time)
switch_button.grid(row=5, column=5, sticky='w')

def toggle_input():
    if edit_var.get():
        title_entry.config(state="normal")
        team1_entry.config(state="normal")
        team2_entry.config(state="normal")
        game_time_entry.config(state="normal")
    else:
        title_entry.config(state="readonly")
        team1_entry.config(state="readonly")
        team2_entry.config(state="readonly")
        game_time_entry.config(state="readonly")

edit_var = tk.BooleanVar()
edit_var.set(False)

edit_checkbutton = tk.Checkbutton(app, text="Modify", variable=edit_var, command=toggle_input)
edit_checkbutton.grid(row=6, column=2, sticky='w')

toggle_input()

def apply_changes():
    if "second_window" in globals():
        competition_label.config(text=title_entry.get())
        team1_name_label.config(text=team1_entry.get()[:5])
        team2_name_label.config(text=team2_entry.get()[:5])
        result_label.config(text=f"{team1_score.get()}   :   {team2_score.get()}")
        attack_game_time_label_2.config(text=f"{attack_time_entry.get()}")
    else:
        show_result()
        
def update_font_sizes():
    global title_label_widget, team1_label_widget, team2_label_widget, team1_score_label_widget, team2_score_label_widget, game_time_label_widget, attack_time_label_widget, attack_time_label_2_widget, result_label_widget, game_time_label_2_widget

    # 창의 크기에 따라 폰트 크기를 조절하는 코드를 작성합니다.
    width, height = app.winfo_width(), app.winfo_height()
    second_width, second_height = second_window.winfo_width(), second_window.winfo_height()
    new_font_size = int(min(width, height) / 20)
    second_font_size = int(min(second_width, second_height)/100)

    title_font.configure(size=new_font_size)
    team_font.configure(size=new_font_size)
    score_font.configure(size=new_font_size)
    custom_font.configure(size=int(new_font_size * 0.8))
    print("새폰트 크기 : ", new_font_size)
    title_font_large.configure(size=second_font_size*8)
    team_font_large.configure(size=second_font_size*11)
    score_font_large.configure(size=second_font_size*28)
    time_font_large.configure(size=second_font_size*15)
    attack_font.configure(size=second_font_size*9)
    print("새폰트 크기 2 : ", second_font_size)
    
    

    # 각 위젯에 새로운 폰트 크기를 적용합니다.
    if title_label_widget:
        title_label_widget.configure(font=title_font)
    if team1_label_widget:
        team1_label_widget.configure(font=team_font)
    if team2_label_widget:
        team2_label_widget.configure(font=team_font)
    if team1_score_label_widget:
        team1_score_label_widget.configure(font=score_font)
    if team2_score_label_widget:
        team2_score_label_widget.configure(font=score_font)
    if game_time_label_widget:
        game_time_label_widget.configure(font=score_font)
    if attack_time_label_widget:
        attack_time_label_widget.configure(font=attack_font)
    if attack_time_label_2_widget:
        attack_time_label_2_widget.configure(font=attack_font)
    if vs_label_widget:
        vs_label_widget.configure(font=title_font_large)       
    if result_label_widget:
        result_label_widget.configure(font=time_font_large)        
    if game_time_label_2_widget:
        game_time_label_2_widget.configure(font=score_font_large)         
       
      
     
        
app.bind('<Configure>', lambda event: update_font_sizes())           
second_window.bind('<Configure>', lambda event: update_font_sizes())
   
def on_focus_out(event):
    game_time_entry.config(state="readonly")
    
app.bind("<FocusOut>", on_focus_out)

def on_motion(event):
    game_time_entry.config(state="normal")
    
app.bind("<Motion>", on_motion)

app.bind('<space>', lambda event: toggle_pause())

app.mainloop()