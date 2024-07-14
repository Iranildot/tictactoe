# IMPORTING LIBRARIES
from tkinter import *
from customtkinter import *
from PIL import Image
import random
from functools import partial
import json

# CREATING A TIMER
class Timer:  
    def __init__(self) -> None:
        self.time = 0
        self.started = False
        self.restarted = True
    
    # TO UPDATE THE TIME
    def update_time(self) -> None:
        if self.started:
            self.time += 1
            minutes, seconds = divmod(self.time, 60)
            self.time_label.configure(text=f"{minutes:02}:{seconds:02}")
            self.time_label.after(1000, self.update_time)

    # TO START THE TIMER
    def start_timer(self) -> None:
        if self.restarted:
            # IF THE SETTINGS WINDOW IS OPENED
            if self.settings_window != None:
                self.settings_window.destroy()
                
            self.started = True
            self.restarted = False
            
            # WHEN THE COMPUTER IS THE FIRST PLAYER
            if "Computer" in self.data["players"][self.current_player] and self.remaining_moves != "":
                computer_play = self.computer_move()
                if computer_play != (-1, -1):
                    self.move(coordinates=computer_play)
                else:
                    self.move(number=self.random_move())
            
            # PUT THE FIRST PLAYER ONTO SCREEN
            self.type_of_game_label.configure(fg_color="#88CC88", text_color="#222222")
            self.time_label.configure(fg_color="#88CC88", text_color="#222222")
  
            self.update_time()

    # TO PAUSE THE TIMER
    def pause_timer(self) -> None:
        if self.started:
            self.started = False
            self.type_of_game_label.configure(fg_color="#555555", text_color="#FFFFFF")
            self.time_label.configure(fg_color="#555555", text_color="#FFFFFF")
            self.current_player_label.configure(fg_color="#88CC88", text_color="#222222")

    # TO RESET THE TIMER
    def reset_timer(self) -> None:
        self.started = False
        self.restarted = True
        self.time = 0
        self.time_label.configure(text="00:00")
        self.type_of_game_label.configure(fg_color="#555555", text_color="#FFFFFF")
        self.time_label.configure(fg_color="#555555", text_color="#FFFFFF")
        self.current_player_label.configure(fg_color="#555555", text_color="#FFFFFF")

class Game:
    def __init__(self) -> None:
        # TO STORE THE PLAYERS' MOVES
        self.board_list = [
                            [5, 5, 5],
                            [5, 5, 5],
                            [5, 5, 5]
                          ]
        
        self.current_player = 0
        self.moves_made = ""
        self.remaining_moves = "012345678"
        self.winner = None
    
    def number_coordinates(self, number=None, coordinates=None) -> tuple:  
        # CONVERTING NUMBER TO COORDINATES      
        if number != None:
            j = number % 3
            i = (number - j) // 3
            
            return (number, i, j)
        
        # CONVERTING COORDINATES TO NUMBER
        elif coordinates != None:
            i, j = coordinates
            number = i*3 + j
            return (number, i, j)
    
    # NEXT PLAYER
    def next_player(self) -> int:
        # UPDATE THE CURRENT PLAYER ONTO SCREEN       
        self.current_player = 0 if self.current_player == 1 else 1
        self.current_player_label.configure(text=self.data["players"][self.current_player])
    
    # MAKE A RANDOM MOVE DEPENDING OF THE REMAINING SPACES
    def random_move(self) -> int:
        return int(self.remaining_moves[random.randint(0, len(self.remaining_moves) - 1)])
    
    # RESET THE GAME
    def reset_game_variables(self) -> None:
        self.board_list = [
                            [5, 5, 5],
                            [5, 5, 5],
                            [5, 5, 5]
                          ]
        
        self.moves_made = ""
        self.remaining_moves = "012345678"
        self.current_player = 0
        self.winner = None
    
    def computer_move(self) -> tuple:
        # TO MAKE THE COMPUTER DECISIONS MORE FLUID LIKE A HUMAN
        random_numbers = [1, 2, 3, 4]
        random.shuffle(random_numbers)
        
        # 5 WHEN ONE MOVE LEFT FOR PLAYER 1 TO WIN
        # 7 WHEN ONE MOVE LEFT FOR PLAYER 2 TO WIN
        results = [5, 7]
        if self.data["difficulty"] == "MEDIUM":
            results = [[5, 7][random.randint(0, 1)]]
        elif self.data["difficulty"] == "EASY":
            return (-1, -1)
        
        for index in random_numbers:
            # LINES [0, 0], [1, 0], [2, 0]
            #       [0, 1], [1, 1], [2, 1]
            #       [0, 2], [1, 2], [2, 2]
            if index == 1:
                for i in range(3):
                    result = self.board_list[i][0] + self.board_list[i][1] + self.board_list[i][2]
                    if result in results:
                        if self.board_list[i][0] == 5:
                            return (i, 0)
                        if self.board_list[i][1] == 5:
                            return (i, 1)
                        if self.board_list[i][2] == 5:
                            return (i, 2)

            # LINES [0, 0], [0, 1], [0, 2]
            #       [1, 0], [1, 1], [1, 2]
            #       [2, 0], [2, 1], [2, 2]
            elif index == 2:
                for j in range(3):
                    result = self.board_list[0][j] + self.board_list[1][j] + self.board_list[2][j]
                    if result in results:
                        if self.board_list[0][j] == 5:
                            return (0, j)
                        if self.board_list[1][j] == 5:
                            return (1, j)
                        if self.board_list[2][j] == 5:
                            return (2, j)
            
            # LINES [0, 0]
            #       [1, 1]
            #       [2, 2]
            elif index == 3:
                result = self.board_list[0][0] + self.board_list[1][1] + self.board_list[2][2]
                if result in results:
                    if self.board_list[0][0] == 5:
                        return (0, 0)
                    if self.board_list[1][1] == 5:
                        return (1, 1)
                    if self.board_list[2][2] == 5:
                        return (2, 2)
            
            # LINES [0, 2]
            #       [1, 1]
            #       [2, 0]
            elif index == 4:
                result = self.board_list[0][2] + self.board_list[1][1] + self.board_list[2][0]
                if result in results:
                    if self.board_list[0][2] == 5:
                        return (0, 2)
                    if self.board_list[1][1] == 5:
                        return (1, 1)
                    if self.board_list[2][0] == 5:
                            return (2, 0)
        
        # TO MAKE A RANDOM MOVE
        return (-1, -1)
    
    # WHEN THERE IS A WINNER IN THE END SHOW THE WIN TRAIL
    def show_trail(self, coordinates):
         for coordinate in coordinates:
             i, j = coordinate
             self.board_buttons[i][j].configure(fg_color="#88CC88", hover_color="#88CC88", text_color="#292929")
    
    def update_history_memory(self):
        if "Computer" in self.data["players"][0] or "Computer" in self.data["players"][1]: 
            dificulty = self.data["difficulty"]
        else:
            dificulty = ""
            
        if self.winner == "TIE":
            sprite = ""
        else:
            sprite = self.data["sprites"][self.current_player]
            if self.scores_window:
                if self.scores_window.winfo_exists():
                    self.data["scores"][self.current_player] += 1
                    self.update_scores()
            
        self.data["history"].append([
                                        self.winner,
                                        sprite,
                                        self.data["players"][0] + " vs " + self.data["players"][1],
                                        self.time_label._text,
                                        dificulty
                                    ])
        
        # SAVING DATA
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False)
                    
    # MAKE A MOVE
    def move(self, number=None, coordinates=None) -> None:
        if self.started:
            
            # GET THE NUMBER AND COORDINATES
            number, i, j = self.number_coordinates(number, coordinates)
            
            # CHECK THE BOARD LIST TO SEE IF THERE NO MOVE THERE
            if self.board_list[i][j] == 5:
                
                # PUT THE MOVE ONTO SCREEN
                self.show_move(number, coordinates=(i, j))
                
                # UPDATE THE PLAYS MADE VARIABLE AND REMAINING
                self.moves_made += str(number)
                self.remaining_moves = self.remaining_moves.replace(str(number), "")
                
                # APPENDING THE CURRENT PLAYER TO THE BOARD THAT CHECK THE WINNER
                self.board_list[i][j] = self.current_player
                
                # CHECKING IF THERE IS A WINNER
                self.check_winner()
                
                # GO TO THE NEXT PLAYER IF NO ONES WINS
                if self.started:
                    self.next_player()
                
                # WHEN IT IS THE COMPUTER TURN
                if "Computer" in self.data["players"][self.current_player] and self.remaining_moves != "":
                    computer_play = self.computer_move()
                    if computer_play != (-1, -1):
                        self.move(coordinates=computer_play)
                    else:
                        self.move(number=self.random_move())
    
    # TO CHECK IF THERE IS WINNER
    def check_winner(self) -> None:
        if self.started:
            self.winner = self.data["players"][self.current_player]
            
            # LINES [0, 0], [1, 0], [2, 0]
            #       [0, 1], [1, 1], [2, 1]
            #       [0, 2], [1, 2], [2, 2]
            for i in range(3):
                result = self.board_list[i][0] + self.board_list[i][1] + self.board_list[i][2]
                if result == 0 or result == 3:
                    self.show_trail(coordinates=((i, 0), (i, 1), (i, 2)))
                    self.update_history_memory()
                    self.pause_timer()
                    return 
                
            # LINES [0, 0], [0, 1], [0, 2]
            #       [1, 0], [1, 1], [1, 2]
            #       [2, 0], [2, 1], [2, 2]
            for j in range(3):
                result = self.board_list[0][j] + self.board_list[1][j] + self.board_list[2][j]
                if result == 0 or result == 3:
                    self.show_trail(coordinates=((0, j), (1, j), (2, j)))
                    self.update_history_memory()
                    self.pause_timer()
                    return
            
            # LINES [0, 0]
            #       [1, 1]
            #       [2, 2]
            result = self.board_list[0][0] + self.board_list[1][1] + self.board_list[2][2]
            if result == 0 or result == 3:
                self.show_trail(coordinates=((0, 0), (1, 1), (2, 2)))
                self.update_history_memory()
                self.pause_timer()
                return
            
            # LINES [0, 2],
            #       [1, 1],
            #       [2, 0],
            result = self.board_list[0][2] + self.board_list[1][1] + self.board_list[2][0]
            if result == 0 or result == 3:
                self.show_trail(coordinates=((0, 2), (1, 1), (2, 0)))
                self.update_history_memory()
                self.pause_timer()
                return
            
            # A TIE
            if self.remaining_moves == "":
                self.current_player_label.configure(text="TIE")
                self.winner = "TIE"
                self.update_history_memory()
                self.pause_timer()
                return
        
# CREATING THE WINDOW
class App(CTk, Game, Timer):
    def __init__(self) -> None:
        CTk.__init__(self)
        Game.__init__(self)
        Timer.__init__(self)
        
        # CREATING THE DATA DICTIONARY
        self.data = {
            "players": ["Player 1", "Player 2"],
            "sprites": ["X", "O"],
            "history": [],  
            "difficulty": "EASY",
            "scores": [0, 0],
            "theme": 0      
        }
        
        # TRYING TO IMPORT THE SAVED GAME INFORMATION
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except:
            pass
        
        # DECLEARING WIDGET VARIABLES
        self.settings_window = None
        self.current_player_label = None
        self.scores_window = None
        self.history_window = None
        self.reset_window = None
        self.data["scores"] = [0, 0]
        self.score_1 = None
        self.score_2 = None
        self.scores_player_1 = None
        self.scores_player_2 = None
        
        # EDITTING ROOT WINDOW SETTINGS
        self.title("TicTacToe")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.geometry("600x600+100+100")
        set_widget_scaling(1.8)
        self.iconbitmap("./icons/tag.ico")
        self.resizable(False, False)
        
        # CREATING THE INTERFACE
        self.interface()
    
    # RESET THE SCORES ON SCOREBOARD
    def reset_scores(self):
        self.data["scores"] = [0, 0]
        self.score_1.configure(text="0")
        self.score_2.configure(text="0")
    
    # UPDATE THE SCORES ON SCOREBOARD
    def update_scores(self):
        self.score_1.configure(text=self.data["scores"][0])
        self.score_2.configure(text=self.data["scores"][1])
    
    # CREATE THE SCORES WINDOW
    def scores(self):
        if self.scores_window:
            self.scores_window.destroy()
            
        # WINDOW SETTINGS
        self.scores_window = CTkToplevel(self, fg_color=("#292929", "#FFFFFF")[self.data["theme"]])
        self.scores_window.iconbitmap("./icons/tag.ico")
        self.settings_window.attributes("-topmost", False)
        self.scores_window.attributes("-topmost", True)
        self.scores_window.geometry("680x130+200+200")
        self.scores_window.title("Scores")
        self.scores_window.rowconfigure(0, weight=1)
        self.scores_window.columnconfigure(0, weight=1)
        self.scores_window.resizable(False, False)
        
        # SCORES FRAME
        self.scores_frame = CTkFrame(self.scores_window, fg_color=("#333333", "#DDDDDD")[self.data["theme"]])
        self.scores_frame.grid(padx=10, pady=10)
        
        # SCORES LABEL
        self.scores_player_1 = CTkLabel(self.scores_frame, text=self.data["players"][0], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=80)
        self.scores_player_1.grid(row=0, column=0, padx=(10, 0), pady=10)
        self.score_1 = CTkLabel(self.scores_frame, text=self.data["scores"][0], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=45)
        self.score_1.grid(row=0, column=1, padx=4)
        self.score_2 = CTkLabel(self.scores_frame, text=self.data["scores"][1], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=45)
        self.score_2.grid(row=0, column=2, padx=4)
        self.scores_player_2 = CTkLabel(self.scores_frame, text=self.data["players"][1], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=80)
        self.scores_player_2.grid(row=0, column=3, padx=(0, 10))
    
        # RESET SCORES BUTTON
        CTkButton(self.scores_frame,
                  text="",
                  image=CTkImage(light_image=Image.open("./icons/refresh.png")),
                  fg_color="#448844",
                  hover_color="#335533",
                  text_color="#FFFFFF",
                  width=30,
                  command=self.reset_scores).grid(row=0, column=5, padx=10, sticky=EW)
            
    def history(self):
        if self.history_window:
            self.history_window.destroy()
            
        # WINDOW SETTINGS
        self.history_window = CTkToplevel(self.settings_window, fg_color=("#292929", "#FFFFFF")[self.data["theme"]])
        self.history_window.iconbitmap("./icons/tag.ico")
        self.settings_window.attributes("-topmost", False)
        self.history_window.attributes("-topmost", True)
        self.history_window.geometry("910x400+200+200")
        self.history_window.title("History")
        self.history_window.rowconfigure(0, weight=1)
        self.history_window.columnconfigure(0, weight=1)
        
        # CREATING A FRAME
        self.history_frame = CTkScrollableFrame(self.history_window, fg_color=("#333333", "#DDDDDD")[self.data["theme"]])
        self.history_frame.rowconfigure(0, weight=1)
        self.history_frame.columnconfigure(0, weight=1)
        self.history_frame.grid(padx=5, pady=20, sticky="EW")
        
        # AUX FRAME TO SHOW HISTORY DATA
        aux_frame = CTkFrame(self.history_frame, fg_color="transparent")
        aux_frame.grid()
        
        history_length = len(self.data["history"]) - 1
        
        for index in range(history_length, -1, -1):
            CTkLabel(aux_frame, text=self.data["history"][index][0], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=100).grid(row=history_length - index, column=0, padx=(0, 2), pady=2)
            CTkLabel(aux_frame, text=self.data["history"][index][1], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=60).grid(row=history_length - index, column=1, padx=2, pady=2)
            CTkLabel(aux_frame, text=self.data["history"][index][2], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=70).grid(row=history_length - index, column=2, padx=2, pady=2)
            CTkLabel(aux_frame, text=self.data["history"][index][3], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=70).grid(row=history_length - index, column=3, padx=(2, 0), pady=2)
            CTkLabel(aux_frame, text=self.data["history"][index][4], fg_color="#448844", text_color="#FFFFFF", corner_radius=10, width=70).grid(row=history_length - index, column=4, padx=(2, 0), pady=2)
            
    def change_theme(self):
            
        # LIGHT THEME
        if self.data["theme"] == 0:
            self.data["theme"] = 1
            self.main_frame.configure(bg_color="#FFFFFF", fg_color="#DDDDDD")
            self.secondary_frame.configure(bg_color="#FFFFFF", fg_color="#DDDDDD")
            self.header_frame.configure(fg_color="#DDDDDD")
            self.board_main_frame.configure(fg_color="#DDDDDD")
            self.board_secondary_frame.configure(fg_color="#DDDDDD")
            self.footer_frame.configure(fg_color="#DDDDDD")
            self.settings_window.configure(fg_color="#FFFFFF")
            self.settings_frame.configure(fg_color="#FFFFFF")
            self.theme_button.configure(text="", fg_color="#BBBBBB", hover_color="#888888", image=CTkImage(light_image=Image.open("./icons/light_mode.png")))
            # IF THERE IS A RESET WINDOW OPENED
            if self.reset_window:
                if self.reset_window.winfo_exists():
                    self.reset_window.configure(fg_color="#FFFFFF", text_color="#222222")
                    self.reset_label.configure(text_color="#222222")
            # IF THERE IS A HISTORY WINDOW OPENED
            if self.history_window:
                if self.history_window.winfo_exists():
                    self.history_window.configure(fg_color="#FFFFFF")
                    self.history_frame.configure(fg_color="#DDDDDD")
            # IF THERE IS A SCORES WINDOW OPENED
            if self.scores_window:
                if self.scores_window.winfo_exists():
                    self.scores_window.configure(fg_color="#FFFFFF")
                    self.scores_frame.configure(fg_color="#DDDDDD")
            
            # SAVING DATA
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False)
        
        # DARK THEME
        else:
            self.data["theme"] = 0
            self.main_frame.configure(bg_color="#222222", fg_color="#292929")
            self.secondary_frame.configure(fg_color="#292929")
            self.header_frame.configure(fg_color="#292929")
            self.board_main_frame.configure(fg_color="#292929")
            self.board_secondary_frame.configure(fg_color="#292929")
            self.footer_frame.configure(fg_color="#292929")
            self.settings_window.configure(fg_color="#292929")
            self.settings_frame.configure(fg_color="#292929")
            self.theme_button.configure(text="", fg_color="#111111", hover_color="#444444", image=CTkImage(light_image=Image.open("./icons/dark_mode.png")))
            # IF THERE IS A RESET WINDOW OPENED
            if self.reset_window:
                if self.reset_window.winfo_exists():
                    self.reset_window.configure(fg_color="#292929")
                    self.reset_label.configure(text_color="#FFFFFF")
            # IF THERE IS A HISTORY WINDOW OPENED
            if self.history_window:
                if self.history_window.winfo_exists():
                    self.history_window.configure(fg_color="#292929")
                    self.history_frame.configure(fg_color="#333333")
            # IF THERE IS A SCORES WINDOW OPENED
            if self.scores_window:
                if self.scores_window.winfo_exists():
                    self.scores_window.configure(fg_color="#292929")
                    self.scores_frame.configure(fg_color="#333333")
                    
            # SAVING DATA
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False)
    
    # SHOW THE MOVE ONTO SCREEN
    def show_move(self, event, number=None, coordinates=None):
        if self.started:
            number, i, j = self.number_coordinates(number, coordinates)
            self.board_buttons[i][j].configure(text=self.data["sprites"][self.current_player])
    
    # CLEAN THE BOARD (RESET)
    def reset_game_gui(self):            
        self.reset_game_variables()
        
        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j].configure(text="", fg_color="#448844", hover_color="#335533", text_color="#FFFFFF")
        
        self.reset_timer()
        self.current_player_label.configure(text=self.data["players"][0])
    
    # LET THE USER CHOOSE THE GAME DIFFICULTY
    def select_difficulty(self, event):
        
        self.data["difficulty"] = self.difficulty_segmented.get()
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False)
    
    # SELECT THE SPRITES
    def select_sprites(self, event):
        
        self.data["sprites"] = self.type_of_sprite_segmented.get().split(" vs ")
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False)
    
    # WHEN THE TYPE OF GAME IS SELECTED
    def combobox_selected(self, event) -> None:
        
        self.type_of_game_label.configure(text=self.type_of_game_combobox.get())
        self.data["players"] = self.type_of_game_label._text.split(" vs ")
        self.current_player_label.configure(text=self.data["players"][0])
        
        if self.scores_window:
            if self.scores_window.winfo_exists():
                self.data["scores"] = [0, 0]
                self.scores_player_1.configure(text=self.data["players"][0])
                self.score_1.configure(text="0")
                self.score_2.configure(text="0")
                self.scores_player_2.configure(text=self.data["players"][1])
        
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False)
    
    # WINDOW THE LET THE USER DELETE ALL OF THE GAME DATA
    def reset(self):
        def confirm():            
            # CLEANING VOLATILE MEMORY
            self.data = {
                            "players": ["Player 1", "Player 2"],
                            "sprites": ["X", "O"],
                            "history": [],  
                            "difficulty": "EASY",
                            "scores": [0, 0],
                            "theme": 1       
                        }
            
            # CLEANING PERMANENT MEMORY
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False)
            
            # PUTTING ONTO SETTINGS WINDOW THE CURRENT TYPE OF GAME
            self.type_of_game_label.configure(text=self.data["players"][0] + " vs " + self.data["players"][1])
            
            if self.history_window:
                self.history_window.destroy()
                self.history_window = None
            
            if self.scores_window:
                self.scores_window.destroy()
                self.scores_window = None
            
            self.settings_window.destroy()
            self.reset_window.destroy()
            self.settings()
            self.change_theme()
        
        # CREATING THE TOPWINDOW
        self.reset_window = CTkToplevel(self.settings_window, fg_color=("#292929", "#FFFFFF")[self.data["theme"]])
        self.reset_window.attributes("-topmost", True)
        self.reset_window.geometry("+300+300")
        self.reset_window.resizable(False, False)
        self.reset_window.title("Reset")
        self.settings_window.attributes("-topmost", False)
        
        
        # CREATING THE TEXT ALERT
        self.reset_label = CTkLabel(self.reset_window, text_color=("#FFFFFF", "#222222")[self.data["theme"]], text=f"Do you want to reset the game data?")
        self.reset_label.grid(columnspan=2, padx=30, pady=(20, 10))
        
        # CONFIRM BUTTON
        CTkButton(self.reset_window,
                  text="Confirm",
                  fg_color="#448844",
                  hover_color="#335533",
                  text_color="#FFFFFF",
                  width=100,
                  image=CTkImage(light_image=Image.open("./icons/check.png")),
                  command=confirm).grid(padx=2, pady=(0, 20), sticky=E)  
        
        # CANCEL BUTTON    
        CTkButton(self.reset_window,
                  text="Cancel",
                  fg_color="#448844",
                  hover_color="#335533",
                  text_color="#FFFFFF",
                  width=100,
                  image=CTkImage(light_image=Image.open("./icons/cancel.png")),
                  command=lambda: self.reset_window.destroy()).grid(padx=2, pady=(0, 20), row=1, column=1, sticky=W)    
        
    
    # CREATING THE SETTINGS WINDOW
    def settings(self) -> None:
        if self.settings_window != None:
            self.settings_window.destroy()
            
        if not self.started:
            # CREATING THE SETTINGS WINDOW
            self.settings_window = CTkToplevel(self, fg_color=("#292929", "#FFFFFF")[self.data["theme"]])
            self.settings_window.attributes("-topmost", True)
            self.settings_window.geometry("+200+200")
            self.settings_window.title("Settings")
            self.settings_window.resizable(False, False)
            
            # CREATING A FRAME
            self.settings_frame = CTkFrame(self.settings_window, fg_color=("#292929", "#FFFFFF")[self.data["theme"]])
            self.settings_frame.grid(padx=30, pady=30)
            
            # TYPE OF GAME
            self.type_of_game_combobox = CTkComboBox(self.settings_frame,
                                                     values=["Player 1 vs Player 2",
                                                             "Player 1 vs Computer 2",
                                                             "Computer 1 vs Player 2"],
                                                     button_color="#448844",
                                                     border_color="#448844",
                                                     width=200,
                                                     state="readonly",
                                                     command=self.combobox_selected)
            self.type_of_game_combobox.set(self.type_of_game_label._text)
            self.type_of_game_combobox.grid(pady=(0, 6), sticky=EW)
            
            # GAME DIFFICULTY
            self.difficulty_segmented = CTkSegmentedButton(self.settings_frame, 
                                                               values=["EASY", "MEDIUM", "HARD"],
                                                               selected_color="#335533",
                                                               selected_hover_color="#335533",
                                                               unselected_hover_color="#335533",
                                                               unselected_color="#448844",
                                                               fg_color="#448844",
                                                               text_color="#FFFFFF",
                                                               command=self.select_difficulty)
            self.difficulty_segmented.set(self.data["difficulty"])
            self.difficulty_segmented.grid(pady=6, sticky=EW)
            
            # TYPE OF SPRITE
            self.type_of_sprite_segmented = CTkSegmentedButton(self.settings_frame, 
                                                               values=["X vs O", "O vs X"],
                                                               selected_color="#335533",
                                                               selected_hover_color="#335533",
                                                               unselected_hover_color="#335533",
                                                               unselected_color="#448844",
                                                               fg_color="#448844",
                                                               text_color="#FFFFFF",
                                                               command=self.select_sprites)
            self.type_of_sprite_segmented.set(self.data["sprites"][0] + " vs " +self.data["sprites"][1])
            self.type_of_sprite_segmented.grid(pady=6, sticky=EW)

            aux_frame = CTkFrame(self.settings_frame, fg_color="transparent")
            aux_frame.grid(pady=6)
            
            # HISTORY
            CTkButton(aux_frame,
                      text="",
                      image=CTkImage(light_image=Image.open("./icons/history.png")),
                      fg_color="#448844",
                      hover_color="#335533",
                      text_color="#FFFFFF",
                      width=60,
                      command=self.history).grid(sticky=EW)
            
            # SCORES
            CTkButton(aux_frame,
                      text="",
                      image=CTkImage(light_image=Image.open("./icons/scoreboard.png")),
                      fg_color="#448844",
                      hover_color="#335533",
                      text_color="#FFFFFF",
                      width=60,
                      command=self.scores).grid(row=0, column=1, padx=10, sticky=EW)
            
            # THEME
            self.theme_button = CTkButton(aux_frame,
                                          text="",
                                          image=(CTkImage(light_image=Image.open("./icons/dark_mode.png")),
                                                 CTkImage(light_image=Image.open("./icons/light_mode.png")))[self.data["theme"]],
                                          fg_color=("#111111", "#BBBBBB")[self.data["theme"]],
                                          hover_color=("#444444", "#888888")[self.data["theme"]],
                                          width=60,
                                          command=self.change_theme)
            self.theme_button.grid(row=0, column=2, sticky=EW)
            
            # RESET AI
            CTkButton(self.settings_frame,
                      text="RESET",
                      image=CTkImage(light_image=Image.open("./icons/reset.png")),
                      fg_color="#DD2222",
                      hover_color="#AA1111",
                      width=20,
                      text_color="#FFFFFF",
                      command=self.reset).grid(pady=(30, 0), sticky=EW)

    
    # ORGANIZING THE INTERFACE
    def interface(self) -> None:
        
        # CREATING THE MAIN FRAME
        self.main_frame = CTkFrame(self, bg_color=("#222222", "#FFFFFF")[self.data["theme"]], fg_color=("#292929", "#DDDDDD")[self.data["theme"]], corner_radius=500)
        self.main_frame.grid(sticky=NSEW)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        # CREATING A SECONDARY WINDOW
        self.secondary_frame = CTkFrame(self.main_frame, fg_color=("#292929", "#DDDDDD")[self.data["theme"]])
        self.secondary_frame.grid()
        self.secondary_frame.rowconfigure(0, weight=1)
        self.secondary_frame.columnconfigure(0, weight=1)
        
        # CREATING THE HEADER FRAME
        self.header_frame = CTkFrame(self.secondary_frame, fg_color=("#292929", "#DDDDDD")[self.data["theme"]], corner_radius=20)
        self.header_frame.rowconfigure(0, weight=1)   
        self.header_frame.columnconfigure(0, weight=1)     
        self.header_frame.grid(ipady=2, sticky=EW)
        
        # CREATING THE HEADER ELEMENTS
        # TYPE OF GAME
        self.type_of_game_label = CTkLabel(self.header_frame, 
                                           text=self.data["players"][0] + " vs " + self.data["players"][1],
                                           font=("Helvetica", 12),
                                           fg_color="#555555",
                                           text_color="#FFFFFF",
                                           corner_radius=20,
                                           width=160)
        self.type_of_game_label.grid(padx=1, sticky=EW)
        
        # SETTINGS BUTTON
        self.settings_button = CTkButton(self.header_frame,
                                         text="",
                                         image=CTkImage(light_image=Image.open("./icons/settings.png")),
                                         font=("Helvetica", 12),
                                         fg_color="#448844",
                                         hover_color="#335533",
                                         text_color="#FFFFFF",
                                         width=30,
                                         corner_radius=5,
                                         command=self.settings)
        self.settings_button.grid(row=0, column=1, padx=2, sticky=EW)

        
        # CREATING THE BOARD MAIN FRAME
        self.board_main_frame = CTkFrame(self.secondary_frame, fg_color=("#292929", "#DDDDDD")[self.data["theme"]], corner_radius=0)
        self.board_main_frame.rowconfigure(0, weight=1)
        self.board_main_frame.columnconfigure(0, weight=1)
        self.board_main_frame.grid(ipady=20)
        
        self.board_secondary_frame = CTkFrame(self.board_main_frame, fg_color=("#292929", "#DDDDDD")[self.data["theme"]], corner_radius=0)
        self.board_secondary_frame.grid()
        
        # LIST TO STORE BOARD BUTTONS
        self.board_buttons = [
                                [None, None, None],
                                [None, None, None],
                                [None, None, None]
                             ]
        
        # CREATING BOARD BUTTONS
        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j] = CTkButton(self.board_secondary_frame,
                                                     font=("Helvetica", 22),
                                                     fg_color="#448844",
                                                     hover_color="#335533",
                                                     text="",
                                                     text_color="#FFFFFF",
                                                     height=45,
                                                     width=45,
                                                     command=partial(self.move, coordinates=(i, j)))
                self.board_buttons[i][j].grid(row=i, column=j, padx=1, pady=1)
        
        # CREATING THE FOOTER FRAME
        self.footer_frame = CTkFrame(self.secondary_frame, fg_color=("#292929", "#DDDDDD")[self.data["theme"]], corner_radius=0)
        self.footer_frame.rowconfigure(0, weight=1)   
        self.footer_frame.columnconfigure(0, weight=1)    
        self.footer_frame.grid(sticky=EW)
        
        # CREATING FOOTER ELEMENTS
        # PLAYER TURN
        self.current_player_label = CTkLabel(self.footer_frame,
                                             text=self.data["players"][0],
                                             font=("Helvetica", 12),
                                             fg_color="#555555",
                                             text_color="#FFFFFF",
                                             corner_radius=20)
        self.current_player_label.grid(padx=1, sticky=EW)
        
        # TIME OF GAME
        self.time_label = CTkLabel(self.footer_frame,
                                   text="00:00",
                                   font=("Helvetica", 12),
                                   fg_color="#555555",
                                   text_color="#FFFFFF",
                                   corner_radius=20)
        self.time_label.grid(row=0, column=1, padx=1)
        
        # REESTART BUTTON
        self.restart_button = CTkButton(self.footer_frame,
                                        text="",
                                        image=CTkImage(light_image=Image.open("./icons/refresh.png")),
                                        font=("Helvetica", 12),
                                        fg_color="#448844",
                                        hover_color="#335533",
                                        text_color="#FFFFFF",
                                        width=30,
                                        corner_radius=5,
                                        command=self.reset_game_gui)
        self.restart_button.grid(row=0, column=2, padx=1)
        
        # START BUTTON
        self.start_button = CTkButton(self.footer_frame,
                                      text="START",
                                      font=("Helvetica", 12),
                                      fg_color="#448844",
                                      hover_color="#335533",
                                      width=30,
                                      corner_radius=20,
                                      command=self.start_timer)
        self.start_button.grid(row=1, column=0, padx=1, pady=2, columnspan=3, sticky=EW)

# STARTING THE APP
if __name__ == "__main__":
    app = App()
    app.mainloop()