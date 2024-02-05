import pygame
from tkinter import Tk, filedialog, Label, Button, Entry, messagebox
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
PADDING = 5

class PuzzleGame:
    def __init__(self):
        self.tk_root = Tk()
        self.tk_root.title("Image Puzzle Setup")

        self.image_path = None
        self.puzzle_size = None
        self.puzzle_pieces = None
        self.selected_piece_index = None
        self.first_selected_piece_index = None
        # Add a goal_state attribute to store the original state of the puzzle
        self.goal_state = None

        # Labels and Entry widgets for puzzle size
        Label(self.tk_root, text="Rows:").grid(row=0, column=0)
        Label(self.tk_root, text="Columns:").grid(row=1, column=0)

        self.entry_rows = Entry(self.tk_root)
        self.entry_columns = Entry(self.tk_root)
        self.entry_rows.grid(row=0, column=1)
        self.entry_columns.grid(row=1, column=1)

        # Button to start the game
        Button(self.tk_root, text="Start", command=self.start_button_click).grid(row=2, columnspan=2, pady=10)

        # Button to shuffle the puzzle
        Button(self.tk_root, text="Shuffle", command=self.shuffle_button_click).grid(row=3, columnspan=2)

        # Button to rotate pieces 90 degrees to the right
        Button(self.tk_root, text="Rotate 90 Right", command=self.rotate_right).grid(row=4, column=0, pady=10)

        # Button to rotate pieces 90 degrees to the left
        Button(self.tk_root, text="Rotate 90 Left", command=self.rotate_left).grid(row=4, column=1, pady=10)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Image Puzzle")

        # Pygame clock for controlling the frame rate
        self.clock = pygame.time.Clock()

    def rotate_right(self):
        # Create a new list to hold the rotated pieces
        rotated_pieces = [None] * len(self.puzzle_pieces)
        
        # Iterate over the original puzzle pieces and calculate their new positions
        for i in range(len(self.puzzle_pieces)):
            x = i % self.puzzle_size[1] # Original column index
            y = i // self.puzzle_size[1] # Original row index
            
            # Calculate the new index for the piece after rotation
            new_x = (self.puzzle_size[0] - 1) - y # New column index (flipped horizontally)
            new_y = x # New row index (same vertically)
            new_index = new_y * self.puzzle_size[0] + new_x
            
            # Place the piece at the new position in the rotated_pieces list
            rotated_pieces[new_index] = self.puzzle_pieces[i]
        
        # Update the puzzle pieces with the rotated pieces
        self.puzzle_pieces = rotated_pieces
        self.draw_puzzle()

    def rotate_left(self):
        # Transpose the puzzle pieces to rotate the board 90 degrees counterclockwise
        self.puzzle_pieces = [self.puzzle_pieces[j * self.puzzle_size[1] + i] for i in range(self.puzzle_size[1]) for j in range(self.puzzle_size[0])]
        # Reverse the order of the rows
        self.puzzle_pieces = [self.puzzle_pieces[i:i + self.puzzle_size[1]] for i in range(0, len(self.puzzle_pieces), self.puzzle_size[1])][::-1]
        self.puzzle_pieces = [item for sublist in self.puzzle_pieces for item in sublist] # Flatten the list
        self.draw_puzzle()

    def shuffle_button_click(self):
        # Shuffle the puzzle pieces
        random.shuffle(self.puzzle_pieces)
        # Redraw the puzzle
        self.draw_puzzle()

    def start_button_click(self):
        # Get image path and puzzle size from user
        self.image_path = self.get_image_path()
        self.puzzle_size = (int(self.entry_rows.get()), int(self.entry_columns.get()))

        # Load and divide the image
        self.puzzle_pieces = self.load_and_divide_image(self.image_path, self.puzzle_size)

        self.original_puzzle_pieces = list(self.puzzle_pieces)
        self.goal_state = list(self.puzzle_pieces)
        # Draw the initial puzzle
        self.draw_puzzle()


    def draw_puzzle(self):
        # Draw the puzzle on the screen
        self.screen.fill((255, 255, 255)) # White background
        self.draw_puzzle_pieces()

        # Calculate and render the minimum switches text
        min_switches = self.calculate_minimum_switches()
        font = pygame.font.Font(None, 36)
        text = font.render("Minimum Switches: {}".format(min_switches), True, (255, 255, 255))
        self.screen.blit(text, (10, 10)) # Adjust the position as needed

        pygame.display.flip()

    def calculate_minimum_switches(self):
        # Count the number of pieces that are not in their original positions
        misplaced_pieces = sum(1 for i in range(len(self.puzzle_pieces)) if self.puzzle_pieces[i] != self.goal_state[i])
        
        # Divide the number of misplaced pieces by 2 to estimate the minimum number of switches
        min_switches = misplaced_pieces // 2
        
        return min_switches

    def draw_puzzle_pieces(self):
        piece_width = SCREEN_WIDTH // self.puzzle_size[1]
        piece_height = SCREEN_HEIGHT // self.puzzle_size[0]

        for index, piece_surface in enumerate(self.puzzle_pieces):
            row = index // self.puzzle_size[1]
            col = index % self.puzzle_size[1]
            self.screen.blit(piece_surface, (col * piece_width, row * piece_height))


    def load_and_divide_image(self, image_path, puzzle_size):
        # Placeholder: Load and divide the image
        original_image = pygame.image.load(image_path)
        piece_width = original_image.get_width() // puzzle_size[1]
        piece_height = original_image.get_height() // puzzle_size[0]

        puzzle_pieces = []

        for row in range(puzzle_size[0]):
            for col in range(puzzle_size[1]):
                piece_rect = pygame.Rect(col * piece_width, row * piece_height, piece_width, piece_height)
                piece_surface = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)
                piece_surface.blit(original_image, (0, 0), piece_rect)
                puzzle_pieces.append(piece_surface)

        return puzzle_pieces

    def get_image_path(self):
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        # return file_path
        return "C:/Users/hariv/Pictures/ramen.jpg"

    def run(self):
        running = True

        # Start the Tkinter GUI event loop
        self.tk_root.after(100, self.check_gui_events)
        self.tk_root.mainloop()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.handle_mouse_click(x, y)
            self.clock.tick(30) # Adjust the frame rate if needed

            # Draw the puzzle
            self.draw_puzzle()

        pygame.quit()

    def handle_mouse_click(self, x, y):
        piece_width = SCREEN_WIDTH // self.puzzle_size[1]
        piece_height = SCREEN_HEIGHT // self.puzzle_size[0]

        for row in range(self.puzzle_size[0]):
            for col in range(self.puzzle_size[1]):
                if (col * piece_width <= x < (col + 1) * piece_width and
                    row * piece_height <= y < (row + 1) * piece_height):
                    piece_index = row * self.puzzle_size[1] + col
                    if self.first_selected_piece_index is None:
                        self.first_selected_piece_index = piece_index
                    else:
                        self.selected_piece_index = piece_index
                        self.swap_pieces()
                        self.check_win_condition()
                        self.first_selected_piece_index = None
                        self.selected_piece_index = None
                    break

    def swap_pieces(self):
        # Swap the positions of the two selected pieces
        self.puzzle_pieces[self.first_selected_piece_index], self.puzzle_pieces[self.selected_piece_index] = \
            self.puzzle_pieces[self.selected_piece_index], self.puzzle_pieces[self.first_selected_piece_index]

    def show_winning_message(self):
        messagebox.showinfo("Congratulations!", "You have completed the puzzle!")

    def check_win_condition(self):
        # Check if the puzzle is solved
        if self.puzzle_pieces == self.original_puzzle_pieces:
            print("You win!")
            self.show_winning_message()
    
    def check_gui_events(self):
        # This method will be called periodically by the Tkinter after method
        # to check for any GUI events
        self.tk_root.update_idletasks()
        self.tk_root.update()

        # Process Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.tk_root.quit() # Terminate the Tkinter mainloop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.handle_mouse_click(x, y)

        # Schedule the next call
        self.tk_root.after(100, self.check_gui_events)

if __name__ == "__main__":
    game = PuzzleGame()
    game.run()
