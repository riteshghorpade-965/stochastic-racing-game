import tkinter as tk
import random


class StochasticRacingGame:

    def __init__(self, root):
        self.root = root
        self.root.title("🏁 Stochastic Racing Game")
        self.root.geometry("1200x760")
        self.root.resizable(False, False)
        self.root.configure(bg="#101827")

        # Game variables
        self.score = 0
        self.turn = 1
        self.max_turns = 5
        self.game_over = False

        self.car_x = 325
        self.car_y = 520

        # Generate stochastic game data
        self.generate_game()

        self.create_interface()
        self.draw_race()
        self.draw_game_tree()

    # ==========================================================
    # STOCHASTIC GAME
    # ==========================================================

    def generate_game(self):

        # FAST route
        self.fast_outcomes = [
            (0.50, "TURBO BOOST", 10),
            (0.30, "CLEAR ROAD", 6),
            (0.20, "CRASH", -8)
        ]

        # SAFE route
        self.safe_outcomes = [
            (0.70, "SMOOTH DRIVE", 5),
            (0.30, "SLOW ROAD", 2)
        ]

        self.fast_eu = self.calculate_eu(self.fast_outcomes)
        self.safe_eu = self.calculate_eu(self.safe_outcomes)

        self.status_text = "Choose FAST or SAFE to race."

    # Expected Utility
    def calculate_eu(self, outcomes):

        total = 0

        for probability, event, utility in outcomes:
            total += probability * utility

        return total

    # ==========================================================
    # RANDOMIZE
    # ==========================================================

    def randomize_game(self):

        self.fast_outcomes = [
            (0.50, "TURBO BOOST", random.randint(7, 13)),
            (0.30, "CLEAR ROAD", random.randint(3, 8)),
            (0.20, "CRASH", random.randint(-12, -5))
        ]

        self.safe_outcomes = [
            (0.70, "SMOOTH DRIVE", random.randint(4, 7)),
            (0.30, "SLOW ROAD", random.randint(1, 4))
        ]

        self.fast_eu = self.calculate_eu(self.fast_outcomes)
        self.safe_eu = self.calculate_eu(self.safe_outcomes)

        self.status_text = "🎲 Randomized! New utilities and EU calculated."

        self.draw_game_tree()
        self.update_labels()

    # ==========================================================
    # PLAYER DECISION
    # ==========================================================

    def choose_route(self, route):

        if self.game_over:
            return

        if route == "FAST":
            outcomes = self.fast_outcomes
            move = 80
        else:
            outcomes = self.safe_outcomes
            move = 45

        # Random probability
        random_value = random.random()

        cumulative = 0

        selected_outcome = outcomes[-1]

        for probability, event, utility in outcomes:

            cumulative += probability

            if random_value <= cumulative:
                selected_outcome = (probability, event, utility)
                break

        probability, event, utility = selected_outcome

        # Add utility to score
        self.score += utility

        # Move car
        self.car_y -= move

        # Status
        self.status_text = (
            f"{route} → {event} | "
            f"Probability: {probability * 100:.0f}% | "
            f"Utility: {utility:+d}"
        )

        # Next turn
        self.turn += 1

        if self.turn > self.max_turns:

            self.game_over = True

            self.status_text += (
                f"\n🏁 RACE FINISHED! Final Score: {self.score}"
            )

        else:

            # Reset car for next turn
            self.car_y = 520

        self.draw_race()
        self.update_labels()

    # ==========================================================
    # NEW GAME
    # ==========================================================

    def new_game(self):

        self.score = 0
        self.turn = 1
        self.game_over = False

        self.car_x = 325
        self.car_y = 520

        self.generate_game()

        self.draw_race()
        self.draw_game_tree()
        self.update_labels()

    # ==========================================================
    # USER INTERFACE
    # ==========================================================

    def create_interface(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#17233a",
            height=70
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="🏁 STOCHASTIC RACING GAME",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#17233a"
        ).pack(
            side="left",
            padx=25,
            pady=15
        )

        self.score_label = tk.Label(
            header,
            text="Score: 0",
            font=("Arial", 17, "bold"),
            fg="#ffd166",
            bg="#17233a"
        )

        self.score_label.pack(
            side="right",
            padx=30
        )

        # Main area
        main = tk.Frame(
            self.root,
            bg="#101827"
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ======================================================
        # LEFT SIDE - RACE
        # ======================================================

        left = tk.Frame(
            main,
            bg="#101827"
        )

        left.pack(
            side="left",
            padx=15,
            pady=15
        )

        self.race_canvas = tk.Canvas(
            left,
            width=650,
            height=620,
            bg="#6fa34e",
            highlightthickness=0
        )

        self.race_canvas.pack()

        # ======================================================
        # RIGHT SIDE
        # ======================================================

        right = tk.Frame(
            main,
            width=490,
            bg="#17233a"
        )

        right.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=15
        )

        right.pack_propagate(False)

        tk.Label(
            right,
            text="PLAYER DECISION (MAX)",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#17233a"
        ).pack(pady=15)

        # Buttons
        button_frame = tk.Frame(
            right,
            bg="#17233a"
        )

        button_frame.pack()

        tk.Button(
            button_frame,
            text="⚡ FAST",
            command=lambda: self.choose_route("FAST"),
            font=("Arial", 12, "bold"),
            width=13,
            height=2,
            bg="#e9a23b",
            relief="flat"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Button(
            button_frame,
            text="🛡️ SAFE",
            command=lambda: self.choose_route("SAFE"),
            font=("Arial", 12, "bold"),
            width=13,
            height=2,
            bg="#66c2a5",
            relief="flat"
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            right,
            text="🎲 RANDOMIZE GAME",
            command=self.randomize_game,
            font=("Arial", 11, "bold"),
            width=30,
            height=2,
            bg="#9b7ede",
            fg="white",
            relief="flat"
        ).pack(pady=12)

        tk.Button(
            right,
            text="🔄 NEW RACE",
            command=self.new_game,
            font=("Arial", 11, "bold"),
            width=30,
            height=2,
            bg="#4f81bd",
            fg="white",
            relief="flat"
        ).pack()

        self.turn_label = tk.Label(
            right,
            text="Turn: 1 / 5",
            font=("Arial", 13, "bold"),
            fg="#8ecae6",
            bg="#17233a"
        )

        self.turn_label.pack(pady=8)

        self.status_label = tk.Label(
            right,
            text=self.status_text,
            font=("Arial", 10, "bold"),
            fg="#ffd166",
            bg="#17233a",
            wraplength=430,
            justify="center"
        )

        self.status_label.pack(pady=5)

        # Game tree title
        tk.Label(
            right,
            text="RANDOMIZED GAME TREE",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#17233a"
        ).pack(pady=(10, 5))

        self.tree_canvas = tk.Canvas(
            right,
            width=450,
            height=310,
            bg="#0c1422",
            highlightthickness=1,
            highlightbackground="#34445c"
        )

        self.tree_canvas.pack(padx=10)

    # ==========================================================
    # DRAW RACING ROAD
    # ==========================================================

    def draw_race(self):

        c = self.race_canvas

        c.delete("all")

        # Grass
        c.create_rectangle(
            0, 0,
            650, 620,
            fill="#6fa34e",
            outline=""
        )

        # Road
        c.create_polygon(
            120, 0,
            530, 0,
            590, 620,
            60, 620,
            fill="#30343b",
            outline=""
        )

        # Road borders
        c.create_line(
            120, 0,
            60, 620,
            fill="white",
            width=5
        )

        c.create_line(
            530, 0,
            590, 620,
            fill="white",
            width=5
        )

        # Center line
        for y in range(0, 620, 80):

            c.create_rectangle(
                320,
                y,
                330,
                y + 40,
                fill="white",
                outline=""
            )

        # Finish line
        for i in range(10):

            color = "white" if i % 2 == 0 else "black"

            c.create_rectangle(
                200 + i * 25,
                35,
                225 + i * 25,
                60,
                fill=color,
                outline=""
            )

        # Obstacles
        obstacles = [
            (230, 200),
            (420, 300),
            (290, 410)
        ]

        for x, y in obstacles:

            c.create_rectangle(
                x - 22,
                y - 15,
                x + 22,
                y + 15,
                fill="#d62828",
                outline="#7f1d1d",
                width=2
            )

            c.create_text(
                x,
                y,
                text="🚧",
                font=("Arial", 18)
            )

        # Car
        x = self.car_x
        y = self.car_y

        # Wheels
        c.create_oval(
            x - 35,
            y - 30,
            x - 18,
            y - 5,
            fill="black"
        )

        c.create_oval(
            x + 18,
            y - 30,
            x + 35,
            y - 5,
            fill="black"
        )

        c.create_oval(
            x - 35,
            y + 5,
            x - 18,
            y + 30,
            fill="black"
        )

        c.create_oval(
            x + 18,
            y + 5,
            x + 35,
            y + 30,
            fill="black"
        )

        # Car body
        c.create_rectangle(
            x - 28,
            y - 42,
            x + 28,
            y + 42,
            fill="#2474d2",
            outline="white",
            width=2
        )

        # Windows
        c.create_rectangle(
            x - 18,
            y - 28,
            x + 18,
            y - 5,
            fill="#bde0fe",
            outline=""
        )

        c.create_rectangle(
            x - 18,
            y + 7,
            x + 18,
            y + 29,
            fill="#bde0fe",
            outline=""
        )

        c.create_text(
            x,
            y,
            text="🏎️",
            font=("Arial", 23)
        )

        # Turn display
        c.create_text(
            325,
            590,
            text=f"TURN {min(self.turn, self.max_turns)} / {self.max_turns}",
            fill="white",
            font=("Arial", 14, "bold")
        )

    # ==========================================================
    # DRAW STOCHASTIC GAME TREE
    # ==========================================================

    def draw_game_tree(self):

        t = self.tree_canvas

        t.delete("all")

        # MAX node
        t.create_oval(
            185, 10,
            265, 50,
            fill="#4f81bd",
            outline="white",
            width=2
        )

        t.create_text(
            225,
            30,
            text="MAX",
            fill="white",
            font=("Arial", 11, "bold")
        )

        # FAST
        t.create_rectangle(
            55, 70,
            165, 105,
            fill="#e9a23b",
            outline="white"
        )

        t.create_text(
            110,
            87,
            text="⚡ FAST",
            font=("Arial", 10, "bold")
        )

        # SAFE
        t.create_rectangle(
            285, 70,
            395, 105,
            fill="#66c2a5",
            outline="white"
        )

        t.create_text(
            340,
            87,
            text="🛡️ SAFE",
            font=("Arial", 10, "bold")
        )

        # Root connections
        t.create_line(
            225, 50,
            110, 70,
            fill="white",
            width=2
        )

        t.create_line(
            225, 50,
            340, 70,
            fill="white",
            width=2
        )

        # Chance nodes
        t.create_oval(
            75, 125,
            145, 160,
            fill="#9b7ede",
            outline="white"
        )

        t.create_text(
            110,
            142,
            text="CHANCE",
            fill="white",
            font=("Arial", 8, "bold")
        )

        t.create_oval(
            305, 125,
            375, 160,
            fill="#9b7ede",
            outline="white"
        )

        t.create_text(
            340,
            142,
            text="CHANCE",
            fill="white",
            font=("Arial", 8, "bold")
        )

        t.create_line(
            110, 105,
            110, 125,
            fill="white"
        )

        t.create_line(
            340, 105,
            340, 125,
            fill="white"
        )

        # Outcome drawing function
        def draw_outcome(
            start_x,
            start_y,
            end_x,
            end_y,
            outcome
        ):

            probability, event, utility = outcome

            t.create_line(
                start_x,
                start_y,
                end_x,
                end_y,
                fill="#b8c7d9"
            )

            t.create_text(
                (start_x + end_x) // 2,
                (start_y + end_y) // 2 - 8,
                text=f"{probability * 100:.0f}%",
                fill="#ffd166",
                font=("Arial", 8, "bold")
            )

            t.create_oval(
                end_x - 23,
                end_y - 14,
                end_x + 23,
                end_y + 14,
                fill="#26384f",
                outline="#b8c7d9"
            )

            t.create_text(
                end_x,
                end_y,
                text=f"{utility:+d}",
                fill="white",
                font=("Arial", 9, "bold")
            )

            t.create_text(
                end_x,
                end_y + 24,
                text=event,
                fill="#b8c7d9",
                font=("Arial", 6)
            )

        # FAST branches
        draw_outcome(
            110, 160,
            45, 205,
            self.fast_outcomes[0]
        )

        draw_outcome(
            110, 160,
            110, 205,
            self.fast_outcomes[1]
        )

        draw_outcome(
            110, 160,
            175, 205,
            self.fast_outcomes[2]
        )

        # SAFE branches
        draw_outcome(
            340, 160,
            305, 205,
            self.safe_outcomes[0]
        )

        draw_outcome(
            340, 160,
            375, 205,
            self.safe_outcomes[1]
        )

        # EU
        t.create_text(
            110,
            270,
            text=f"EU = {self.fast_eu:.2f}",
            fill="#ffd166",
            font=("Arial", 12, "bold")
        )

        t.create_text(
            340,
            270,
            text=f"EU = {self.safe_eu:.2f}",
            fill="#ffd166",
            font=("Arial", 12, "bold")
        )

        # Formula
        t.create_text(
            225,
            295,
            text="EU = Σ (Probability × Utility)",
            fill="#8ecae6",
            font=("Arial", 9, "bold")
        )

    # ==========================================================
    # UPDATE LABELS
    # ==========================================================

    def update_labels(self):

        self.score_label.config(
            text=f"Score: {self.score:+d}"
        )

        self.turn_label.config(
            text=f"Turn: {min(self.turn, self.max_turns)} / {self.max_turns}"
        )

        self.status_label.config(
            text=self.status_text
        )


# ==============================================================
# START PROGRAM
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = StochasticRacingGame(root)

    root.mainloop()
