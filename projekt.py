from tkinter import *
from random import randrange
import tkinter.messagebox
import time
import sys


class ConnectFour:
    def __init__(self, parent):

        self.labels = [] #lista wszystkich pol
        self.turn_counter = 0 #liczba ruchow ogolem
        self.win_status = 0 #0 jak trwa gra, 1 jak ktos wygral albo remis

        self.empty_image = PhotoImage(file = "assets/empty.gif")
        self.blue_image = PhotoImage(file = "assets/blue.gif")
        self.red_image = PhotoImage(file = "assets/red.gif")

        #rozmiary pol
        self.height = 100
        self.width = 100

        for i in range(42):
            self.labels.append(Label(parent,
                                     image = self.empty_image,
                                     bg = "white",
                                     width = self.width,
                                     height = self.height,
                                     ))

        #ustawianie pol
        piece_index = 0 #kazde pole ma swoj unikatowy identyfikator
        for c in range(7): #pole sa numerowane od lewej do prawej
            for r in range(6,0,-1): #i od dolu do gory
                self.labels[piece_index].grid(row = r,
                                              column = c,
                                              padx = 0,
                                              pady = 0,
                                              sticky = S)
                self.labels[piece_index].bind("<Button-1>", lambda event, coords = (r,c): self.column_click(event, coords))
                 #wspolrzedne kazdego pola jest przekazywane do column_click
                piece_index += 1

    def column_click(self, event, coords):
        print("tura: ", game.turn_counter + 1, " kolumna: ", coords[1])
        if game.win_status == 0:
            columns[coords[1]].drop_piece(coords[1])
        else:
            print("Gra jest juz skonczona")

    #aktualizacja
    def redraw(self, c_ord, r_ord, piece_state):

        self.c_ord = c_ord
        self.r_ord = r_ord
        self.piece_state = piece_state

        piece_index = r_ord + 6 * c_ord
        #kalkuluje unikalny identyfikator pola

        if self.piece_state == 1:
            self.labels[piece_index].configure(image = self.blue_image)
        elif self.piece_state == -1:
            self.labels[piece_index].configure(image = self.red_image)


    #sprawdza wszystkie pozycje czy jest wygrana
    def check_win(self):
        # for i in range(len(columns)):
        #     print(columns[i].column)

        #pionowe pozycje
        self.blue_vertical = [1, 1, 1, 1]
        self.red_vertical = [-1, -1, -1, -1]

        for i in range(len(columns)):
            if any(self.blue_vertical == columns[i].column[j:j+4] for j in range(3)): #niebieskie
                blue_win.display_win_message("niebieski")
            if any(self.red_vertical == columns[i].column[j:j+4] for j in range(3)): #czerwone
                red_win.display_win_message("czerwony")

        #poziome pozycje
        for i in range(4): #wysatrczy sprawdzic tylko 4 kolumny
            for j in range(6): #csprawdza 6 wiersze kazdej kolumny

                subtotal = columns[i].column[j] + columns[i+1].column[j] + columns[i+2].column[j] + columns[i+3].column[j]
                if subtotal == 4: #niebieskie poziomy
                    blue_win.display_win_message("niebieski")
                if subtotal == -4: #czerwone poziomy
                    red_win.display_win_message("czerwony")

        #ukosy
        for i in range(4): #sprawdza pierwsze 4 kolumny
            for j in range(3):
                subtotal = columns[i].column[j] + columns[i+1].column[j+1] + columns[i+2].column[j+2] + columns[i+3].column[j+3]
                if subtotal == 4:
                    blue_win.display_win_message("niebieski")
                if subtotal == -4:
                    red_win.display_win_message("czerwony")

            for j in range(3, 6):
                subtotal = columns[i].column[j] + columns[i+1].column[j-1] + columns[i+2].column[j-2] + columns[i+3].column[j-3]
                if subtotal == 4:
                    blue_win.display_win_message("niebieski")
                if subtotal == -4:
                    red_win.display_win_message("czerwony")

        #sprawdzanie czy plansza jest zapelniona
        board_full = 1
        for i in range(7):
            for j in range(6):
                board_full *= columns[i].column[j]
        #print(board_full)
        if board_full != 0:
            tie_win.display_win_message("remis")


class Win_message:
    def __init__(self, root, team):

        self.root = root
        self.team = team
        self.frame_status = 0
        self.total_frame_num = 21 #niewazne
        self.frame_delay = 30 #to tez

        self.grid_total_frame_num = 9
        self.grid_multiplier = 3
        #tez niewazne juz
        self.current_height = -0.1
        self.final_height = 0.32
        self.increment_height = 0.02


        #przycisk do resetowania
        self.refresh_image = PhotoImage(file = "assets/refresh.gif")
        self.refresh_button = Label(image = self.refresh_image, bg = "#FFFFFF")
        self.refresh_button.place(relx = 0, rely = 0)
        self.refresh_button.bind("<Button-1>", lambda event: self.again())



    #ustawia obrazek kazdemu poolu
    def load_frames(self):

        self.frames = []

        for i in range(self.total_frame_num):

            self.frames.append(PhotoImage(file = self.team, format = "gif -index " + str(i)))



    def display_win_message(self, kto_wygral):
        self.kto_wygral = kto_wygral
        answer = tkinter.messagebox.askquestion("WYGRAL "+self.kto_wygral, "Czy chcesz zaczac od nowa?")

        if answer == 'yes':
            self.again()
        else:
            self.quit_game()



    def again(self):
        #RESET
        for i in range(0,42):
            game.labels[i].grid_forget()
        game.__init__(root)
        blue_win.__init__(root, "blue")
        red_win.__init__(root, "red")
        for i in range(7):
            columns[i].__init__()

    def quit_game(self):
        root.destroy()
        sys.exit()


class Memory:
    def __init__(self):

        #ustawia defaultowo 0 wszyskim polom
        self.column = [0 for i in range(6)]

    def drop_piece(self, c_ord):

        self.c_ord = c_ord

        for i in range(len(self.column)):
            if self.column[i] == 0: #sprawdza czy pole jest puste
                if game.turn_counter % 2 == 0: #tutaj ustawia albo czerwone albo niebieskie
                    self.column[i] = 1
                else:
                    self.column[i] = -1

                self.r_ord = i
                self.piece_state = self.column[i]


                game.turn_counter += 1

                #rysuje pokolorowane pola na danych koordynatach
                game.redraw(self.c_ord, self.r_ord, self.piece_state)

                game.check_win()

                break
            elif self.column[5] != 0:
                print("kolumna pelna")
                break



if __name__ == "__main__":
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.geometry("728x624")

    root.title("Cztery w rzedzie")
    game = ConnectFour(root)
    blue_win = Win_message(root, 'assets/bluewin.gif')
    red_win = Win_message(root, 'assets/redwin.gif')
    tie_win = Win_message(root, 'assets/tiewin.gif')
    blue_win.load_frames()
    red_win.load_frames()
    tie_win.load_frames()
    columns = []


    for i in range(7):
        columns.append(Memory())
    root.mainloop()
