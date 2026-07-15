import tkinter as tk

class ponggame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong Game")
        self.root.resizable(False, False)

        # Game Settings
        self.width = 600
        self.height = 400
        self.ball_speed_x = 4
        self.ball_speed_y = 4
        self.paddle_speed = 20
        
        # Game State
        self.is_running = False
        self.score_left = 0
        self.score_right = 0

        # --- GUI Layout ---
        # Control Panel (Top)
        self.control_frame = tk.Frame(root, bg="gray")
        self.control_frame.pack(fill=tk.X)

        self.btn_start = tk.Button(self.control_frame, text="Start", command=self.toggle_game, width=10, font=("Arial", 12, "bold"))
        self.btn_start.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_exit = tk.Button(self.control_frame, text="Exit", command=root.quit, width=10, font=("Arial", 12, "bold"), fg="red")
        self.btn_exit.pack(side=tk.RIGHT, padx=10, pady=5)

        self.score_label = tk.Label(self.control_frame, text="0 : 0", font=("Arial", 16, "bold"), bg="gray", fg="white")
        self.score_label.pack(pady=5)

        # Game Canvas (Bottom)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Game Objects
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")
        self.paddle_left = self.canvas.create_rectangle(20, 150, 35, 250, fill="blue")
        self.paddle_right = self.canvas.create_rectangle(565, 150, 580, 250, fill="red")
        
        # Center Line
        self.canvas.create_line(self.width/2, 0, self.width/2, self.height, fill="white", dash=(5, 5))

        # Key Bindings
        self.root.bind("<w>", lambda e: self.move_paddle(self.paddle_left, -self.paddle_speed))
        self.root.bind("<s>", lambda e: self.move_paddle(self.paddle_left, self.paddle_speed))
        self.root.bind("<Up>", lambda e: self.move_paddle(self.paddle_right, -self.paddle_speed))
        self.root.bind("<Down>", lambda e: self.move_paddle(self.paddle_right, self.paddle_speed))

        # Start game loop
        self.game_loop()

    def toggle_game(self):
        """Handles pausing and resuming the game."""
        if self.is_running:
            self.is_running = False
            self.btn_start.config(text="Resume")
        else:
            self.is_running = True
            self.btn_start.config(text="Pause")

    def move_paddle(self, paddle, y_delta):
        """Moves paddles while keeping them within bounds."""
        coords = self.canvas.coords(paddle)
        if (coords[1] + y_delta >= 0) and (coords[3] + y_delta <= self.height):
            self.canvas.move(paddle, 0, y_delta)

    def reset_ball(self):
        """Resets the ball to the center and reverses direction."""
        self.canvas.coords(self.ball, 290, 190, 310, 210)
        self.ball_speed_x *= -1

    def update_score(self):
        """Updates the top GUI score display."""
        self.score_label.config(text=f"{self.score_left} : {self.score_right}")

    def game_loop(self):
        """The main animation loop."""
        if self.is_running:
            # Move the ball
            self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
            ball_coords = self.canvas.coords(self.ball)
            
            # Top and Bottom wall collision
            if ball_coords[1] <= 0 or ball_coords[3] >= self.height:
                self.ball_speed_y *= -1

            # Paddle collision logic
            paddle_l_coords = self.canvas.coords(self.paddle_left)
            paddle_r_coords = self.canvas.coords(self.paddle_right)

            # Left paddle hit
            if (ball_coords[0] <= paddle_l_coords[2] and 
                paddle_l_coords[1] <= ball_coords[3] and 
                paddle_l_coords[3] >= ball_coords[1] and 
                self.ball_speed_x < 0):
                self.ball_speed_x *= -1

            # Right paddle hit
            if (ball_coords[2] >= paddle_r_coords[0] and 
                paddle_r_coords[1] <= ball_coords[3] and 
                paddle_r_coords[3] >= ball_coords[1] and 
                self.ball_speed_x > 0):
                self.ball_speed_x *= -1

            # Scoring conditions
            if ball_coords[0] <= 0:  # Right scores
                self.score_right += 1
                self.update_score()
                self.reset_ball()

            if ball_coords[2] >= self.width:  # Left scores
                self.score_left += 1
                self.update_score()
                self.reset_ball()

        # Repeat this loop every 16ms (~60 frames per second)
        self.root.after(16, self.game_loop)
# Run the application

def main():
    print("Starting Game...")
    root = tk.Tk()
    game = ponggame(root)
    root.mainloop()

if __name__ == "__main__":
    main()