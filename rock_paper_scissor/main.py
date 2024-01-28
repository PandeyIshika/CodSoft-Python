import tkinter as tk
from PIL import Image, ImageTk
from random import randint

class RockPaperScissorsApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Rock Paper Scissors Game")
        self.geometry("857x425")

        self.frames = {}
        for F in (StartPage, GamePage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#3498db")
        tk.Label(self, text="Rock Paper Scissors Game", font=("Helvetica", 24), bg="#3498db", fg="white").pack(pady=20)
        tk.Label(self, text="Instructions:", font=("Helvetica", 14), bg="#3498db", fg="white").pack(pady=10)
        tk.Label(self, text="1. Click on 'Start Game' to begin playing.", font=("Helvetica", 12), bg="#3498db", fg="white").pack()
        tk.Label(self, text="2. Choose between Rock, Paper, or Scissors.", font=("Helvetica", 12), bg="#3498db", fg="white").pack()
        tk.Label(self, text="3. Click on the corresponding button to make your choice.", font=("Helvetica", 12), bg="#3498db", fg="white").pack()
        tk.Label(self, text="4. The game consists of multiple rounds. The first player to win 3 rounds is the overall winner.", font=("Helvetica", 12), bg="#3498db", fg="white").pack()
        
        tk.Button(self, text="Start Game", font=("Helvetica", 14), command=lambda: master.show_frame(GamePage), bg="#2ecc71", fg="white").pack(pady=20)
        tk.Button(self, text="Exit", font=("Helvetica", 14), command=self.quit, bg="#e74c3c", fg="white").pack(pady=20)

class GamePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#3498db")

        self.rock_img = ImageTk.PhotoImage(Image.open("rock_paper_scissor\Rock-User.png"))
        self.paper_img = ImageTk.PhotoImage(Image.open("rock_paper_scissor\Paper-User.png"))
        self.scissor_img = ImageTk.PhotoImage(Image.open("rock_paper_scissor\Scissor-User.png"))
        self.rock_img_comp = ImageTk.PhotoImage(Image.open("rock_paper_scissor\Rock.png"))
        self.paper_img_comp = ImageTk.PhotoImage(Image.open("rock_paper_scissor\Paper.png"))
        self.scissor_img_comp = ImageTk.PhotoImage(Image.open("rock_paper_scissor\Scissor.png"))

        self.user_label = tk.Label(self, image=self.scissor_img, bg="#3498db")
        self.comp_label = tk.Label(self, image=self.scissor_img_comp, bg="#3498db")
        self.comp_label.grid(row=1, column=0)
        self.user_label.grid(row=1, column=4)

        self.player_score = 0
        self.computer_score = 0

        self.playerScore = tk.Label(self, text=self.player_score, font=("Helvetica", 14), bg="#3498db", fg="white")
        self.computerScore = tk.Label(self, text=self.computer_score, font=("Helvetica", 14), bg="#3498db", fg="white")

        self.computerScore.grid(row=1, column=1)
        self.playerScore.grid(row=1, column=3)

        self.user_indicator = tk.Label(self, font=("Helvetica", 14), text="USER", bg="#3498db", fg="white")
        self.comp_indicator = tk.Label(self, font=("Helvetica", 14), text="COMPUTER", bg="#3498db", fg="white")
        self.user_indicator.grid(row=0, column=3)
        self.comp_indicator.grid(row=0, column=1)

        self.msg = tk.Label(self, font=("Helvetica", 14), bg="#3498db", fg="white")
        self.msg.grid(row=3, column=2, pady=20)

        self.rock_button = tk.Button(self, width=20, height=2, text="ROCK", bg="#FF3E4D", fg="white", command=lambda: self.update_choice("rock"))
        self.rock_button.grid(row=2, column=1)

        self.paper_button = tk.Button(self, width=20, height=2, text="PAPER", bg="#FAD02E", fg="white", command=lambda: self.update_choice("paper"))
        self.paper_button.grid(row=2, column=2)

        self.scissor_button = tk.Button(self, width=20, height=2, text="SCISSOR", bg="#0ABDE3", fg="white", command=lambda: self.update_choice("scissor"))
        self.scissor_button.grid(row=2, column=3)

        self.play_again_button = tk.Button(self, text="Play Again", font=("Helvetica", 14), command=self.reset_game, state=tk.DISABLED, bg="#3498db", fg="white")
        self.play_again_button.grid(row=4, column=1, pady=25, sticky="news")

        self.exit_button = tk.Button(self, text="Exit", font=("Helvetica", 14), command=self.quit, bg="#e74c3c", fg="white")
        self.exit_button.grid(row=4, column=3, pady=25, sticky="news")

    def update_message(self, x):
        self.msg['text'] = x

    def update_user_score(self):
        self.player_score += 1
        self.playerScore["text"] = str(self.player_score)

    def update_comp_score(self):
        self.computer_score += 1
        self.computerScore["text"] = str(self.computer_score)

    def check_win(self, player, computer):
        if player == computer:
            self.update_message("It's a tie!!!")
        elif player == "rock":
            if computer == "paper":
                self.update_message("You lose")
                self.update_comp_score()
            else:
                self.update_message("You Win")
                self.update_user_score()
        elif player == "paper":
            if computer == "scissor":
                self.update_message("You lose")
                self.update_comp_score()
            else:
                self.update_message("You Win")
                self.update_user_score()
        elif player == "scissor":
            if computer == "rock":
                self.update_message("You lose")
                self.update_comp_score()
            else:
                self.update_message("You Win")
                self.update_user_score()
        else:
            pass

    def update_choice(self, x):
        
        comp_choice = ["rock", "paper", "scissor"][randint(0, 2)]
        if comp_choice == "rock":
            self.comp_label.configure(image=self.rock_img_comp)
        elif comp_choice == "paper":
            self.comp_label.configure(image=self.paper_img_comp)
        else:
            self.comp_label.configure(image=self.scissor_img_comp)

        if x == "rock":
            self.user_label.configure(image=self.rock_img)
        elif x == "paper":
            self.user_label.configure(image=self.paper_img)
        else:
            self.user_label.configure(image=self.scissor_img)

        self.check_win(x, comp_choice)
        self.check_game_over()

    def check_game_over(self):
        if self.player_score == 3 or self.computer_score == 3:
            if self.player_score > self.computer_score:
                self.update_message("Game Over!\n You Win!")
            else:
                self.update_message("Game Over!\n Computer Wins!")

            self.rock_button.config(state=tk.DISABLED)
            self.paper_button.config(state=tk.DISABLED)
            self.scissor_button.config(state=tk.DISABLED)
            self.play_again_button.config(state=tk.NORMAL)
            self.exit_button.config(state=tk.NORMAL)

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.round_num = 0
        self.playerScore["text"] = str(self.player_score)
        self.computerScore["text"] = str(self.computer_score)
        self.update_message("")
        self.comp_label.configure(image=self.scissor_img_comp)
        self.user_label.configure(image=self.scissor_img)
        self.rock_button.config(state=tk.NORMAL)
        self.paper_button.config(state=tk.NORMAL)
        self.scissor_button.config(state=tk.NORMAL)
        self.play_again_button.config(state=tk.DISABLED)
        self.exit_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()
