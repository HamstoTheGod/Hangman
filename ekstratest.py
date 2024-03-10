##DETTE ER KODEN DU BRUGER TIL C AFSLUTNINGSPROJEKTET "HANGMAN"

import nltk
from nltk.corpus import words
from nltk.corpus import wordnet
import arcade
import random

nltk.download('words')
nltk.download('wordnet')

class vindue(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)

        self.levels_obj = levels()
        self.spillerinterface_obj = spillerinterface(self.levels_obj, 5)
        self.input_text = ''
        self.liv = 5
        self.startliv = self.liv
        self.input_text_ift_coop = ''
        self.listeAfMennesket = [(285, 530, 20, arcade.color.BLACK, 5)]

    def setup(self):
        self.spillerinterface_obj.hangmantekst()

    def on_draw(self):
        arcade.start_render()
        ## Her Tegner jeg galgen
        arcade.draw_line(150,350,150,600,arcade.color.BLACK,10)
        arcade.draw_line(135, 600, 300, 600, arcade.color.BLACK, 10)
        arcade.draw_line(150, 550, 200, 600, arcade.color.BLACK, 10)
        arcade.draw_line(285, 600, 285, 550, arcade.color.BLACK, 5)
        #
        arcade.draw_text("Guess a letter:", 100, 100, arcade.color.BLACK, 20)
        arcade.draw_text(self.input_text, 300, 100, arcade.color.BLACK, 12)
        arcade.draw_text(" ".join(self.spillerinterface_obj.ordlængde), 300, 300, arcade.color.BLACK, 20)
        arcade.draw_text(self.levels_obj.visuelesynonymer, 100, 150, arcade.color.BLACK, 10)
        arcade.draw_text(self.levels_obj.tilfældigt_ord, 400, 150, arcade.color.BLACK, 30)
        for i in self.listeAfMennesket:
            arcade.draw_circle_outline(*i)

        if self.input_text_ift_coop == self.levels_obj.tilfældigt_ord or "".join(self.spillerinterface_obj.ordlængde) == self.levels_obj.tilfældigt_ord:
            arcade.draw_text(f"TILLYKKE DU HAR VUNNDDETTTT HANGMAN!!! ORDET VAR {self.levels_obj.tilfældigt_ord}", 0,500, arcade.color.BLACK, 10)
            self.spillerinterface_obj.ordlængde= self.levels_obj.tilfældigt_ord
        if self.liv <= 0:
            arcade.draw_text(self.levels_obj.visuelesynonymer, 100, 150, arcade.color.BLACK, 100)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:

            if len(self.input_text) > 1:
                self.input_text_ift_coop = self.input_text.upper()
            if len(self.input_text) == 1:
                self.input_text_ift_coop = self.input_text.upper()

            if self.input_text_ift_coop not in self.levels_obj.tilfældigt_ord:
                print("Forket gæt")
                self.liv -= 1
                print(f"liv tilbage {self.liv}")
            for i, bogstav in enumerate(self.levels_obj.tilfældigt_ord):
                if bogstav == self.input_text_ift_coop:
                    print(f"dit gæt {bogstav}")
                    self.spillerinterface_obj.ordlængde[i] = self.input_text_ift_coop

            self.input_text = ""  # Reset input text after Enter is pressed


        elif key == arcade.key.BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            # vi tryer siden hvis vi ikke tryer kan det generere en error hvis karakteren er fra numpaten (måske også handre steder der var bare der jeg lagde mærke til det)
            try:
                self.input_text += chr(key)
            except:
                pass
            return self.input_text_ift_coop




    def update(self, delta_time):
        pass

class levels:
    def __init__(self):
        self.ordliste = words.words()
        self.tilfældigt_ord = ""
        self.synonyms = []

    def hent_tilfældigt_ord(self, ordlevel):
        self.__init__()
        while len(self.tilfældigt_ord) != ordlevel or len(set(self.synonyms)) < 8 or len(set(self.synonyms)) > 12:
            self.tilfældigt_ord = random.choice(self.ordliste).upper()
            self.synonyms = []
            for syn in wordnet.synsets(self.tilfældigt_ord):
                for i in syn.lemmas():
                    self.synonyms.append(i.name().upper())
                self.synonyms = [i for i in self.synonyms if i != self.tilfældigt_ord]

        self.visuelesynonymer = f"{self.synonyms[0]} {self.synonyms[1]} {self.synonyms[2]} {self.synonyms[3]} {self.synonyms[4]}"
        return self.tilfældigt_ord, self.synonyms, self.visuelesynonymer



class spillerinterface:
    def __init__(self, levels_objekt, liv):
        self.levels_obj = levels_objekt
        self.levels_obj.hent_tilfældigt_ord(6)
        self.liv = liv
        self.ordlængde = list()

    def hangmantekst(self):
        self.levels_obj.hent_tilfældigt_ord(6)
        self.ordlængde = list("_" * len(self.levels_obj.tilfældigt_ord))
        self.bogstaverBrugt = list()

        print(set(self.levels_obj.synonyms))
        print("".join(self.ordlængde))

def main():
    window = vindue(640, 640, "HANGMAN")
    window.setup()
    arcade.run()

main()
