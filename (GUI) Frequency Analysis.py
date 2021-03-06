"""
Alex Scorza September 2018
http://www.randomtextgenerator.com/
https://www.blindtextgenerator.com/lorem-ipsum
Made for the cipher challenge but feel free to use all you lovely people.
This program decrypts substitution ciphers by finding the frequencies of letters.
You can switch words once it's done and search for words.
It returns the answer keeping punctuation, spaces and which letters are capitals.
One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me?" he thought. It wasn't a dream. His room, a proper human room although a little too small, lay peacefully between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather. Drops 
Vcf hvkcwcg, mbfc Gkfgvk Eihei mvlf dkvh nkvastfy ykfihe, bf dvacy bwheftd nkicedvkhfy wc bwe sfy wcnv i bvkkwstf qfkhwc. Bf tip vc bwe ikhvak-twlf sizl, icy wd bf twdnfy bwe bfiy i twnntf bf zvaty eff bwe skvmc sfttp, etwgbntp yvhfy icy ywqwyfy sp ikzbfe wcnv enwdd efznwvce. Nbf sfyywcg mie bikytp istf nv zvqfk wn icy effhfy kfiyp nv etwyf vdd icp hvhfcn. Bwe hicp tfge, jwnwdattp nbwc zvhjikfy mwnb nbf ewrf vd nbf kfen vd bwh, miqfy isvan bftjtfeetp ie bf tvvlfy. "Mbin'e bijjfcfy nv hf?" bf nbvagbn. Wn miec'n i ykfih. Bwe kvvh, i jkvjfk bahic kvvh itnbvagb i twnntf nvv ehitt, tip jfizfdattp sfnmffc wne dvak dihwtwik mitte. I zvttfznwvc vd nfxnwtf eihjtfe tip ejkfiy van vc nbf nistf - Eihei mie i nkiqfttwcg eitfehic - icy isvqf wn nbfkf bacg i jwznakf nbin bf biy kfzfcntp zan van vd ic wttaenkinfy higirwcf icy bvaefy wc i cwzf, gwtyfy dkihf. Wn ebvmfy i tiyp dwnnfy van mwnb i dak bin icy dak svi mbv ein ajkwgbn, kiwewcg i bfiqp dak hadd nbin zvqfkfy nbf mbvtf vd bfk tvmfk ikh nvmikye nbf qwfmfk. Gkfgvk nbfc nakcfy nv tvvl van nbf mwcyvm in nbf yatt mfinbfk. Ykvje
a b c d e f g h i j k l m n o p q r s t u v w x y z
"""

import tkinter as tk
import tkinter.scrolledtext as tkst
from _tkinter import TclError
import re
from warnings import warn
import random
import os
import itertools
import timeit

os.chdir(os.path.dirname(__file__))

# Change these depending on state
WIP = True
NEW_RELEASE = False


title = "Frequency Analysis"
if WIP:
    title += " (FEATURE CURRENTLY BEING ADDED - WILL NOT WORK PROPERLY)"
if NEW_RELEASE:
    title += " (FEATURE HAS JUST BEEN ADDED - MAY BE BUGGY STILL)"

font = ("Consolas", 10)
bg = "white"
style = {"bg": bg, "font": font}
lb_colours = ("#ffffff", "#82f595")
err_colour = "#f21d1d"

alphabet = "abcdefghijklmnopqrstuvwxyz" # Doesn't need to be a tuple
mono = "etaoinshrdlcumwfgypbvkjxqz" # Doesn't need to be a tuple
##alphabet=mono[:]
di = ("th", "he", "an", "in", "er", "on", "re", "ed", "nd", "ha", "at", "en")
tri = ("the", "and", "tha", "ent", "ion", "tio", "for", "nce", "has", "nce", "tis", "oft", "men")

co_nums = ("mono", "di", "tri")

# changed = list(alphabet)  # Has to swap letters, must me mutable, this is default if no letters are entered
letter = lambda x: re.match(r"^[a-zA-z]$", x) is not  None  #  Is letter
keep = lambda arr1, arr2: "".join([x for x in arr1 if x in arr2])
order_changed = lambda: None

def fact(n):
    sum_ = 1
    for i in range(1, n + 1):
        sum_ *= i
    return sum_


def p(n):
    if n < 8:
        return str(fact(n))
    n = fact(n)
    digit1 = str(abs(n))[0]
    result = digit1 + "e" + str(len(str(abs(n))))
    if n < 0:
        result = "-" + result
    return result


def index_all(array, element):
    indexes = []
    for i in range(len(array)):
        if array[i] == element:
            indexes.append(i)
    return indexes

def add_spaces(num):
    num = str(num) + "%"
    num = " " * (5 - len(num)) + num
    return num


def order_rating(array):
    score = 0
    for i in range(len(array)-1):
        cmp1 = array[i]
        cmp2 = array[(i + 1) % len(array)]
        if cmp1 != cmp2:
            if cmp1 > cmp2:
                score -= 1
            else:
                score += 1
##            print(cmp1, cmp2)
    return int(100 * score / (len(array) - 1))


def remove_duplicates(string):
    new = ""
    for letter in string:
        if letter not in new:
            new += letter
    return new


def regex_pos(find, string, mode): # 'find' can be string or regexp. mode=0: string, 1: regexp
    if find  ==  "":
        return []
    else:
        if mode == 0:
            return [(x, x+len(find)) for x in range(len(string)) if string[x:x+len(find)] == find] # Index string positions
        else:
            return [x.span() for x in re.compile(find).finditer(string)]
            # Index positions were regexp matches - span() is start() and end() in a tuple


def get(scrolled_text):
        return scrolled_text.get("1.0", "end")


def is_regex(string): # If vaild regexp
    try:
        re.match(string, "Any Old String")
        return True
    except:
        return False


def find_pos(line_list, regex, mode): # line_list example: ("hello there", "howdy parter")
    result=[]
    for line_num in range(len(line_list)):
        for letter_pos in regex_pos(regex, line_list[line_num], mode): # example of letter_pos: (3, 6), starting and finishing index
            result +=  (("{}.{}".format(line_num+1, letter_pos[0]), "{}.{}".format(line_num+1, letter_pos[1])), )
    return tuple(result)


def replace_letters(uncertain_count, new_letters, original_text, this_permutation):
        new_text = list(original_text)
        for x in range(uncertain_count):
            for index in indexes_to_edit[new_letters[x]]:
                new_text[index] = this_permutation[x]
        return "".join(new_text)


def set_to_letter(string):
    if string == "":
        return "" # Else, next line will cause error
    string=string[-1] # When you type another letter, set to last for ease of use
    if string[0].lower() not in alphabet:
        string="" # Only allowed if letter
    return string.lower()


def order_dict(dictionary):
##    print("dict:", dictionary)
    # order_dict({'he': 2, 'el': 1, 'll': 1, 'lo': 1, 'ot': 1, 'th': 1, 'er': 1, 're': 1, 'ef': 1, 'fr': 1, 'ri': 1, 'ie': 1, 'en': 1, 'nd': 1})
    new=[]
    for x in range(len(dictionary)):
        hi=max(tuple(dictionary.values()))
        for k, v in dictionary.items():
            if v == hi:
                new.append(k)
                del dictionary[k]
                break
    return new


def amount(string, group_size=1): # Dictionary with numbers of each letter
##    tally=[0]*len(var_value) # [0, 0, 0, 0, 0, 0...]
    string=keep(string.lower(), alphabet)
    iterable=[string[i:i+group_size] for i in range(1+len(string)-group_size)]
##    print("iterable:", iterable)
    amounts={}
    for el in iterable:
##        if el.lower() in var_value:
##            tally[var_value.index(el.lower())] +=  1
            if el in amounts.keys():
                amounts[el] +=  1
            else:
                amounts[el]=1
    return amounts            


def simplify_text(string):
    return remove_duplicates(keep(string.lower(), alphabet))

def _assign(arr, group_size=1): # Dictionary with each letter's frequency
    new=[""]*26
    for i in range(26):
        hi=arr.index(max(arr)) # position of highest number
        new[hi]=mono[i] # Set highest to highest remaining in most frequent letters
        arr[hi]=-1 # Won't be reused but deleting will reduce list lenght and cause index error
    return new


def _assign(arr, group_size=1):
    selected_var=co_nums[group_size-1]
    var_value=globals()[selected_var]
    ordered=order_dict(arr)
##    print("ordered:", ordered)
    overlay=[" "]*26
    for x in range(len(var_value[:len(ordered)])):
        for letter, i in zip(ordered[x], range(len(ordered[x]))):
##            print(var_value[x])
##            print(letter, var_value[x])
##            print(new_changed[alphabet.index(letter)], mono[x])
            
            selected_val=var_value[x][i]
##            print(selected_val)
            if letter not in overlay:
                overlay[alphabet.index(letter)], overlay[alphabet.index(selected_val)]=selected_val, letter
                print(overlay)
##            new_changed[alphabet.index(selected_val)]=letter
##    print("new changed", new_changed)
##    remaining_letters=[letter for letter in alphabet if letter not in new_changed]
####    print("remaining:", remaining_letters)
##    for letter in alphabet[len(new_changed):]:
##        if letter not in new_changed:
##            new_changed.append(letter)
##        else:
##            new_changed.append(remaining_letters.pop(0))
####    print("filled, len:", new_changed, len(new_changed))
##    print("new changed 2:", new_changed)

    new_changed=changed[:]
    for i in range(len(alphabet)):
        if overlay[i] != " ":
            new_changed[i]=overlay[i]
##    print(overlay)
    set1=set(alphabet)
    set2=set(new_changed)
##    print(alphabet, len(set1), changed, len(set2), set1 == set2, set2 - set1)
    return new_changed


def assign(arr, group_size=1):
    group_size = 1
    selected_var = co_nums[group_size-1]
    var_value = globals()[selected_var]
    ordered = order_dict(arr)
    new_changed  =[" "]*26
    for i in range(len(ordered)):
        index=alphabet.index(ordered[i]) # Position of most frequent letters in text
        new_changed[index] = mono[i]
    for i in range(len(new_changed)):
        if new_changed[i] == " ":
            if alphabet[i] in new_changed:
                pass
            else:
                new_changed[i]=alphabet[i]
    remaining_alphabet = [letter for letter in alphabet if not letter in new_changed]
    for letter in (remaining_alphabet):
        new_changed[new_changed.index(" ")] = letter # Index gives first position
    return new_changed


def numberify(search):
    """Allows you to find if one word can be enciphered to another with substitution.
    This makes a word into a tuple of integers - if a letter has not appeared, 
    it adds its position to numbers. Else, the position of the first
    appearance of that letter: "morning" -> "0 1 2 3 4 3 6" - 'n' appears twice"""
    search=keep(search.lower(), alphabet)
    numbers=[] # Answer
    done=[] # Leters that have already appeared
    for x in range(len(search)):
        if search[x] in done:
            numbers +=  [done.index(search[x])]
        else:
            numbers +=  [x]
        done.append(search[x])
    return " ".join(map(str, numbers))

def is_action(func):
    def decorated(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.actions.action()
    return decorated

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg=bg)
        self.title(title)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


        self.changed = list(alphabet)  # Has to swap letters, must me mutable, this is default if no letters are entered

        self.enter = tkst.ScrolledText(width=70, height=13, **style) # 12 + 12 + (button height * 2)=26
        self.enter.grid(row=0, column=0, columnspan=3, sticky="EW")
        self.answer = tkst.ScrolledText(width=70, height=13, state="disabled", **style)
        self.answer.grid(row=2, column=0, columnspan=3, sticky="EW")
##        self.answer.bind("<Key>", lambda event: "break")

        self.enter_select_popup = tk.Menu(self, tearoff=0)
        self.enter_select_popup.add_command(label="Find possible words", command=self.find_from_entry_selection)
        self.answer_select_popup = tk.Menu(self, tearoff=0)
        self.answer_select_popup.add_command(label="Find possible words", command=self.find_from_answer_selection)
        self.enter.bind("<Button-3>", lambda event: self.create_popup(event, self.enter_select_popup))
        self.answer.bind("<Button-3>", lambda event: self.create_popup(event, self.answer_select_popup))

        self.buttons_frame = tk.Frame(self, bg=bg)
        self.buttons_frame.grid(row=1, column=0, columnspan=3, sticky="EW")

        btn_width = 35
        btn_height = 1
        #make_command=lambda size: lambda: self.set_change(get(self.enter), size)
        self.decrypt_c = tk.Button(self.buttons_frame, text="Decrypt Using Current", width=btn_width, height=btn_height, command=self.decrypt_current, **style)
        self.decrypt_c.grid(row=0, column=0, sticky="EW")
        self.decrypt = tk.Button(self.buttons_frame, text="Monographs", width=btn_width, height=btn_height, command=lambda: self.set_change(get(self.enter)), **style)
        self.reset_btn = tk.Button(self.buttons_frame, text="Reset Conversions", command=self.reset_changed, **style)
        self.reset_btn.grid(row=1, column=0, sticky="EW")
        self.shuffle_btn = tk.Button(self.buttons_frame, text="Shuffle Randomly", command=self.shuffle, **style)
        self.shuffle_btn.grid(row=2, column=0, sticky="EW")
        self.normalise_btn = tk.Button(self.buttons_frame, text="Normalise Text", command=self.normalise, **style)
        self.normalise_btn.grid(row=1, column=1, sticky="EW")
        self.decrypt.grid(row=0, column=1, sticky="EW")
##        self.find=tk.Button(self.buttons_frame, text="Digraphs", **style, width=btn_width, height=btn_height, command=make_command(2))
##        self.find.grid(row=1, column=0, sticky="EW")
##        self.find=tk.Button(self.buttons_frame, text="Trigraphs", **style, width=btn_width, height=btn_height, command=make_command(3))
##        self.find.grid(row=1, column=1, sticky="EW")
##        tk.Message(text="""Made by Alex Scorza. This project is my own work, but feel free to use and modify it!""", 
##                   **style, justify="center", fg="# 464647", width=200
##                   ).grid(row=4, column=0, rowspan=3)
        self.misc_frame = tk.Frame(bg=bg)
        self.misc_frame.grid(row=4, column=0, rowspan=3)
        tk.Label(self.misc_frame, text="Order rating (-100 to 100):", justify="center", **style).grid(row=0, column=0)
        self.order_lbl = tk.Label(self.misc_frame, text=" 100%", **style)
        self.order_lbl.grid(row=0, column=1)
        tk.Label(self.misc_frame, text="Errors:", justify="right", **style).grid(row=1, column=0, columnspan=2)
        self.error_log = tk.Text(self.misc_frame, width=30, height=2, font=font, bg="#EFEFEF", state="disabled", fg="#c90000")
        self.error_log.grid(row=2, column=0, columnspan=2)

        
        self.switch_frame = tk.Frame(bg=bg)
        self.switch_frame.grid(row=4, column=1)
        tk.Label(self.switch_frame, text="Enter two letters below to switch them", **style).grid(row=0, column=0, columnspan=2, sticky="EW")
        self.mark_as_correct = tk.BooleanVar(self, value=True)
        tk.Checkbutton(self.switch_frame, text="Mark second letter as correct?", variable=self.mark_as_correct, **style).grid(row=1, column=0, columnspan=2)
        self.letter_var1 = tk.StringVar(self)
        self.letter_var2 = tk.StringVar(self)
        self.letter_var1.trace("w", self.check_letter1)
        self.letter_var2.trace("w", self.check_letter2)
        self.letter_entry1 = tk.Entry(self.switch_frame, textvariable=self.letter_var1, width=2, justify="center", **style)
        self.letter_entry1.grid(row=2, column=0)
        self.letter_entry1.bind("<Return>", self.return_letter1)
        self.letter_entry2 = tk.Entry(self.switch_frame, textvariable=self.letter_var2, width=2, justify="center", **style)
        self.letter_entry2.grid(row=2, column=1)
        self.letter_entry2.bind("<Return>", self.return_letter2)
        self.switch_btn = tk.Button(self.switch_frame, text="Switch", state="disabled", command=self.switch_entered, **style)
        self.switch_btn.grid(row=3, column=0, columnspan=2)

        
        self.conversions_column_frame = tk.Frame(self, bg=bg)
        self.conversions_column_frame.grid(row=0, column=3, rowspan=3, sticky="NS")

        self.converts = tk.Listbox(self.conversions_column_frame, width=10, height=26, font=font, bg=lb_colours[0], selectmode="multiple")
        self.converts.grid(row=0, column=0, sticky="NS")
        self.converts.bind("<<ListboxSelect>>", self.on_conversion_select)
        self.converts.bind("<FocusOut>", lambda event: self.converts.selection_clear(0, "end"))
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Toggle Marking", command=self.toggle_marked)
        self.popup_menu.add_command(label="Select All", command=self.select_all)
        self.popup_menu.add_command(label="Deselect All", command=lambda: self.converts.selection_clear(0, "end"))
        self.popup_menu.add_command(label="Toggle Selection", command=self.select_inverse)
        self.converts.bind("<Button-3>", lambda event: self.create_popup(event, self.popup_menu))
        self.marked = [0]*26

        tk.Message(self.conversions_column_frame, text="Highlight above in textboxes?", width=100, **style).grid(row=1, column=0)
        self.highlight_text = tk.BooleanVar(self, value=True)
        self.highlight_text_cbtn = tk.Checkbutton(self.conversions_column_frame, variable=self.highlight_text, **style)
        self.highlight_text_cbtn.grid(row=2, column=0)


        possible_words_frame=tk.Frame(bg=bg)
        possible_words_frame.grid(row=0, column=4, rowspan=3, sticky="N")

        tk.Label(possible_words_frame, text="Enter a word: ", **style
                 ).grid(row=0, column=0, sticky="NEW", columnspan=2)
        
        search_possible_subframe=tk.Frame(possible_words_frame, bg=bg)
        search_possible_subframe.grid(row=1, column=0, pady=10)
        self.word_search=tk.StringVar(search_possible_subframe)
        word_entry=tk.Entry(search_possible_subframe, width=12, textvariable=self.word_search, bg=bg, font=(font, 13))
        word_entry.bind("<Return>", self.list_possible)
        word_entry.grid(row=0, column=0, sticky="W")
        tk.Button(search_possible_subframe, text="→", width=2, command=self.list_possible, **style
                  ).grid(row=0, column=1, sticky="NES")
        self.saved_word_entered = ""
        self.saved_string_selected = ""

        possible_subframe = tk.Frame(possible_words_frame, bg=bg)
        possible_subframe.grid(row=2, column=0, sticky="NS")
        self.possible_values = tk.Variable(self)
        self.possible = tk.Listbox(possible_subframe, height=15, listvariable=self.possible_values)
        self.possible.grid(row=0, column=0)
        self.scrollbar = tk.Scrollbar(possible_subframe, command=self.possible.yview)
        self.scrollbar.grid(row=0, column=1, sticky="NSW")
        self.possible.config(yscrollcommand=self.scrollbar.set)
        self.possible.bind("<<ListboxSelect>>", lambda event: self.on_possible_select(event))

        search_type_subframe = tk.Frame(possible_words_frame, bg=bg)
        search_type_subframe.grid(row=3, column=0)
        self.search_type = tk.StringVar(self, value=0)
        rbtn_text=("Search each word", "Search plain text")
        for i in range(len(rbtn_text)):
            tk.Radiobutton(search_type_subframe, value=i, text=rbtn_text[i], variable=self.search_type, **style
                           ).grid(row=i, column=0, sticky="W")
        self.apply_certain = tk.Button(possible_words_frame, text="Apply To Certain", state="disabled", command=self.apply_certain, **style)
        self.apply_certain.grid(row=4, column=0)
        self.permutations_lbl = tk.Label(possible_words_frame, **style)
        self.show_permutations()
        self.permutations_lbl.grid(row=5, column=0)
        self.brute_force_btn = tk.Button(possible_words_frame, text="Begin Brute Force", command=self.find_all_permutations, **style)
        self.brute_force_btn.grid(row=6, column=0)
        
        self.set_letters(self.conversions(), self.converts)

        find_frame = tk.Frame(self, bg=bg)
        self.word_option = tk.BooleanVar(find_frame, value=0) # Needs to be accessible in self.match_finder
        word_options = ("Enter a string to match", "Enter a regexp to match")
        instruct = tk.Label(find_frame, text=word_options[0], **style)
        instruct.grid(row=0, column=0, columnspan=2)
        tk.Checkbutton(find_frame, text="Use regular expressions?", variable=self.word_option, command=lambda: [instruct.config(text=word_options[self.word_option.get()], **style), self.match_finder()]).grid(row=5, column=0, columnspan=2)
        self.to_find=tk.StringVar(self)
        self.ctrlf=tk.Entry(find_frame, textvariable=self.to_find, width=20, **style)
        self.ctrlf.grid(row=1, column=0, columnspan=2, sticky="W", padx=30)
        tk.Button(find_frame, text="→", command=self.match_finder, width=2, **style).grid(row=1, column=0, columnspan=2, sticky="E")
        self.match_num=tk.Label(find_frame, text="Matches: 0", **style)
        self.match_num.grid(row=3, column=0, columnspan=2)
        self.find_in=tk.IntVar(self, value=0) # 0=entry, 1=answer, 'self': accessible in class
        tk.Radiobutton(find_frame, text="In Entry", variable=self.find_in, value=0, command=self.match_finder, **style).grid(row=4, column=0)
        tk.Radiobutton(find_frame, text="In Answer", variable=self.find_in, value=1, command=self.match_finder, **style).grid(row=4, column=1)        
        find_frame.grid(row=4, column=3, columnspan=2)


        self.initiate_test()
        
##        self.actions = ActionStack(self)
##        self.bind("<Control-z>", lambda event: self.actions.undo())
##        self.bind("<Control-y>", lambda event: self.actions.redo)

        self.update_idletasks()
##        self.minsize(self.winfo_height(), self.winfo_width())
        
        self.mainloop()

    def initiate_test(self):
##        self.word_search.set("hello")
##        self.word_search.set("ab")
##        self.enter.insert("end", "abc")
##        self.possible.insert("end", "".join(reversed(alphabet)))
##        self.marked = [0] * 3 + [1] * 23
##        self.update_marked()
        return

    def show_permutations(self):
        self.permutations_lbl.config(text="Permutations:" + p(self.marked.count(0)))
    
    def switch_entered(self):
        self.switch(self.letter_var1.get(), self.letter_var2.get())

    def conversions(self):
        return [alphabet[x] + " -> " + self.changed[x] for x in range(26)] # Call to update whenever

    def encipher(self, text, key=None):
        if key is None:
            key = self.changed
        answer = ""
        for el in text:
            if el in alphabet:
                answer +=  key[alphabet.index(el)]
            elif el in alphabet.upper():
                answer +=  key[alphabet.index(el.lower())].upper()
            else:
                answer +=  el
        return answer

    def decipher(self, text):
        answer = ""
        for el in text:
            if el in alphabet:
                answer +=  alphabet[self.changed.index(el)]
            elif el in alphabet.upper():
                answer +=  alphabet[self.changed.index(el.lower())].upper()
            else:
                answer +=  el
        return answer


    def set_btn_state(self, btn, state):
        btn.config(state=state)

    def apply_certain(self):
##        index = self.possible.curselection()[0]
##        selected_word = self.possible_values.get()[index].lower()
##        print("Word:", selected_word)
        for letter in self.saved_string_selected:
            print(letter, end=" ")
            self.set_mark(alphabet.index(letter), 1)
        self.update_marked()

    def normalise(self):
        entered_text = self.enter.get("1.0", "end")
        self.set_text(keep(entered_text.upper(), alphabet.upper()), self.enter)

    def find_all_permutations(self):
        def contains(word, string):
            if self.search_type.get() == "0":
                string = keep(string.lower(), alphabet).split(" ")
                return word in string
            else:
                return word in string
                
        word = self.word_search.get()
        uncertain_indexes, new_letters = self.find_uncertain_letters()
        print(uncertain_indexes, new_letters, sep="\n")
        index_permutations = tuple(itertools.permutations(uncertain_indexes))
        letter_permutations = tuple(itertools.permutations(new_letters))
        print(index_permutations, letter_permutations, sep="\n")
        original_text = self.encipher(keep(get(self.enter).lower(), " " + alphabet))
        indexes_to_edit = {}
        for letter in new_letters:
            indexes_to_edit[letter] = index_all(original_text, letter)
        print("Indexes to edit:", indexes_to_edit)
        print("Original:", original_text)
        uncertain_count = self.marked.count(0)
        matches = set()
        for i in range(1, fact(uncertain_count)): # First permutation same as orignal
            new_text = list(original_text)
            for x in range(uncertain_count):
                for index in indexes_to_edit[new_letters[x]]:
                    new_text[index] = letter_permutations[i][x]
            new_text = "".join(new_text)
            if contains(word, new_text):
                to_add = list(alphabet)
                this_index_permutation = index_permutations[i]
                for index in range(uncertain_count):
                    to_add[uncertain_indexes[index]] = alphabet[this_index_permutation[index]]
                to_add = "".join(to_add)
                matches.add(to_add)
        print(tuple(sorted(matches)))
        self.set_letters([alphabet] + list(sorted(matches)), self.possible)
        self.saved_word_entered = alphabet
        self.word_search.set(alphabet)
    
    def shuffle(self):  
        uncertain_indexes, new_letters = self.find_uncertain_letters()
        random.shuffle(new_letters)
        self.set_new_uncertain(uncertain_indexes, new_letters)

    
    def find_uncertain_letters(self):
        uncertain_indexes = [i for i in range(26) if self.marked[i] == 0]
        new_letters = [self.changed[i] for i in uncertain_indexes]

        return (uncertain_indexes, new_letters)

    def set_new_uncertain(self, uncertain_indexes, new_letters):
        for i in range(len(uncertain_indexes)):
            self.changed[uncertain_indexes[i]] = new_letters[i]
        self.update_all()

        #self.actions.action()

    
    def update_all(self):
        self.update_conversions()
        self.decrypt_current()
        self.set_order_lbl()


    def update_conversions(self):
        self.set_letters(self.conversions(), self.converts)
        self.update_marked()

    
    def update_marked(self):
        # print("Updating to", self.marked)
        for i in range(len(alphabet)):
            self.converts.itemconfig(i, bg=lb_colours[self.marked[i]])
        self.show_permutations()
        self.highlight_text_widgets()


    def select_inverse(self):
        selection=self.converts.curselection()
        self.converts.selection_set(0, "end")
        for item in selection:
            self.converts.selection_clear(item)


    def list_possible(self, event=None):
        self.set_btn_state(self.apply_certain, "disabled")
        string_entered=self.word_search.get()
        matches=self.find_matches(get(self.enter), string_entered)
##        print(matches)
##        print(self.marked)
        invalid_matches=[]
        marked_letters=[alphabet[i] for i in range(len(alphabet)) if self.marked[i] == 1]
        for i in range(len(matches)):
            for x in range(len(matches[i])):
                letter=matches[i][x]
##                print(marked_letters)
                if letter in marked_letters:
##                    print("Marked Letter")
##                    print(letter)
                    expected_letter=self.changed[alphabet.index(letter)].lower()
                    actual_letter=string_entered[x].lower()
                    
##                    print(letter, "in self.marked")
                    if expected_letter != actual_letter:
                        invalid_matches.append(i)
                        break
##        print(invalid_matches)
        no_dup_matches = []
        for el in matches:
            if not el in no_dup_matches:
                no_dup_matches.append(el)
        self.set_letters(no_dup_matches, self.possible)
        for i in range(len(no_dup_matches)):
##            print(i, matches[i])
            if i in invalid_matches:
                self.possible.itemconfig(i, bg=err_colour)
            else:
                
                self.possible.itemconfig(i, bg=lb_colours[1])
        self.saved_word_entered = string_entered


    def set_can_apply(self, value):
        self.can_apply_certain = value

        
    def find_matches(self, text, word): # Find matches of word to words in the text
        result=[]
        find=numberify(word)
        mode=self.search_type.get()
        print(repr(mode))
        if mode == "0":
            text=text.replace("\n", " ") # Remove newlines and put a space -> one line
            text=tuple(word.lower() for word in keep(text, alphabet+alphabet.upper()+" ").split())
            print(text)
            for x in text:
                if numberify(x) == find and not x in result: # No duplicates
                    result.append(x) # If not already there, add
        elif mode == "1":
            text = text.replace("\n", "")
            for i in range(len(text) - len(word)):
                cur_slice=text[i:i + len(word)]
                if numberify(cur_slice) == find:
                    result.append(cur_slice)
        return sorted(result) # Makes it easier to navigate


    def set_mark(self, index, colour_index):
        if colour_index == "invert":
            colour_index = 1-self.marked[index]
        self.marked[index] = colour_index
        self.converts.itemconfig(index, bg=lb_colours[colour_index])
        self.show_permutations()


    def toggle_marked(self):
        for sel in self.converts.curselection():
##5            print(alphabet[sel])
            self.set_mark(sel, "invert")
        self.converts.selection_clear(0, "end")
        
        print(self.marked)
        self.highlight_text_widgets()

    
    def select_all(self):
        self.converts.selection_set(0, "end")

    
    def create_popup(self, event, widget):
        try:
            widget.tk_popup(event.x_root, event.y_root, 0)
        finally:
            widget.grab_release()


    def match_finder(self, *args):
        try:
            if self.find_in.get() == 0:
                self.highlight_words(self.answer, self.encipher(self.to_find.get()))
                self.highlight_words(self.enter, self.to_find.get())
            else:
                self.highlight_words(self.answer, self.to_find.get())
                self.highlight_words(self.enter, self.decipher(self.to_find.get()))
            self.ctrlf.config(fg="black")
        except Exception as error: # Invalid regex
            self.ctrlf.config(fg="red")
##            print(error)

        
    def highlight_words(self, widget, *words, background="yellow", display_matches=True): # Find all points to highlight and highlight them
        widget.tag_delete("selected")
        widget.tag_configure("selected", background=background)
        print(words)
        positions = []
        for word in words:
            positions = find_pos(get(widget).split("\n"), word, self.word_option.get())
            # 'self.word_option.get()' is whether is looks for string (0/False) or regexp (1/True)
            for pos in positions:
                self.highlight(widget, *pos)
        if display_matches:
            self.match_num.config(text = "Matches: "+str(len(positions)))

        
    def highlight(self, widget, index1="1.0", index2="1.0"): # Highlight between two points
        widget.tag_add("selected", index1, index2)


    def highlight_text_widgets(self):
        to_highlight = []
        for i in range(26):
            if self.marked[i] == 1:
                to_highlight.append(self.changed[i])
        self.highlight_words(self.answer, *to_highlight, background=lb_colours[1])

        
    def on_possible_select(self, event): # Activate when listbox item selected
        print("before:", self.marked)
        self.set_btn_state(self.apply_certain, "normal")
        widget = event.widget
        index = widget.curselection()
        if len(index) == 1:
##            self.set_text(msg, self.error_log)
            self.saved_string_selected = simplify_text(widget.get(index).lower())
            found = self.saved_string_selected[:]
            enciphered_found = self.encipher(found)
            word_entered = simplify_text(self.word_search.get())
            print("1:", found, "2:", word_entered, "3:", enciphered_found)
##            for i in range(len(found)):
##                if found[i] in alphabet:
##                    print(enciphered_found[i], word_entered[i])
##                    self.switch(enciphered_found[i], word_entered[i], uses_custom_marking=True)
##                    print(self.changed)
            for letter in word_entered:
                self.changed[self.changed.index(letter)] = "."
            for i in range(len(found)):
                self.changed[alphabet.index(found[i])] = word_entered[i]
            unused_letters = tuple(set(alphabet) - set(self.changed))
            unused_indexes = []
            for i in range(26):
                if self.changed[i] == ".":
                    unused_indexes.append(i)
            for i in range(len(unused_letters)):
                self.changed[unused_indexes[i]] = unused_letters[i]

            print(found, self.word_search.get())
##            self.update_marked()
            #for letter in found:
                #self.set_mark(alphabet.index(letter), 1)
            self.decrypt_current()
            self.update_marked()
        self.update_conversions()
        print("after:", self.marked)


    def on_conversion_select(self, event):
        return
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        print(index, value)
        self.letter_var1.set(value[0])

            
    def decrypt_current(self):
        self.set_text(self.encipher(get(self.enter)), self.answer)
        self.enter.tag_delete("selected")
        self.answer.tag_delete("selected")
        self.set_order_lbl()

    
    def set_letters(self, arr, listbox):
        listbox.delete(0, "end")
        for x in arr:
            listbox.insert("end", x)


    def set_text(self, value, widget):
        is_disabled = widget.cget("state") == "disabled"
        if is_disabled:
            widget.config(state = "normal")
        widget.delete("1.0", "end")
        widget.insert("end", value)
        if is_disabled:
            widget.config(state = "disabled")


    def error(self, text):
        self.set_text(text, self.error_log)

    
    def set_order_lbl(self):
        self.order_lbl.config(text=add_spaces(order_rating(self.changed)))


    def set_change(self, plain_txt):
        self.marked = [0]*26
        tallied=amount(plain_txt)
##        print("TALLIED:", len(tallied))
##        print(alphabet, self.changed)
        self.reset_changed()
        self.changed = assign(tallied)
        self.set_order_lbl()
##        print(tallied)
##        print(self.changed)
        self.set_text(self.encipher(plain_txt), self.answer)
        self.set_letters(self.conversions(), self.converts)


    def return_letter1(self, event):
        if self.letter_var1.get() == "":
            return
##        print("enter")
        self.letter_entry2.focus()


    def return_letter2(self, event):
        if self.letter_var2.get() == "":
            return
        self.switch_btn.invoke()
        self.letter_entry1.focus()

    
    def check_letter1(self, *args):
        self.letter_var1.set(set_to_letter(self.letter_var1.get()))
        if self.check_both():
            pass


    def check_letter2(self, *args):
        self.letter_var2.set(set_to_letter(self.letter_var2.get()))
        self.check_both()


    def check_both(self):
        vals=(self.letter_var1.get(), self.letter_var2.get())
        if "" in vals or len(set(vals)) == 1: # None empty and no duplicates
            self.switch_btn.config(state="disabled")
            return False
        else:
            self.switch_btn.config(state="normal")
            return True

    
    def reset_changed(self):
        self.changed = list(alphabet)  # Has to swap letters, must me mutable, this is default if no letters are entered
        self.update_all()

    
    def find_from_answer_selection(self):
        print(self.decipher(self.answer.selection_get()))
        self.find_from_entry_selection(self.answer)


    def find_from_entry_selection(self, widget=None):
        if widget is None:
            widget = self.enter
        try:
            selected = widget.selection_get()
            length = len(selected)
            if length > 22:
                return
        except TclError: #From _tkinter
            return
        selected_pattern = numberify(selected)
        required_letters = {}
        for index in range(len(selected)):
            letter_index = alphabet.index(selected[index])
            if self.marked[letter_index] == 1:
                required_letters[index] = self.changed[letter_index]
        lines = {}
        for folder in {"plain", "numerical"}:
            with open("words\\" + folder + "\\" + str(length) + ".txt") as file:
                lines[folder + "_lines"] = [line.rstrip("\n") for line in file.readlines()]
        plain_lines = lines["plain_lines"]
        pattern_lines = lines["numerical_lines"]
        matching_words = []
        for i in range(len(pattern_lines)):
            if pattern_lines[i] == selected_pattern:
                required_letters_correct = True
                for index, letter in required_letters.items():
                    if plain_lines[i][index] != letter:
                        required_letters_correct = False
                if required_letters_correct:
                    matching_words.append(plain_lines[i])
        # print(matching_words)
        self.word_search.set(selected)
        self.set_letters(matching_words, self.possible)


    def switch(self, char1, char2, uses_custom_marking=False): # Switch two letters in changed
        char2_index = self.changed.index(char2)
        self.changed[self.changed.index(char1)] = self.changed[self.changed.index(char2)]
        self.changed[char2_index] = char1
        self.set_letters(self.conversions(), self.converts)
        self.letter_var1.set("")
        self.letter_var2.set("")
        self.decrypt_current() # After switching, decrypt with new
        if self.mark_as_correct.get() and not uses_custom_marking:
            print(char1, char2)
            self.marked[self.changed.index(char2)] = 1
            self.update_marked()


class ActionStack:
    def __init__(self, parent):
        self.parent = parent
        self.stack = []
        self.save_state()
        self.position = 1
    
    def save_state(self):
        print("".join(self.parent.changed))
        self.stack.append({"marked": self.parent.marked, "changed": self.parent.changed[:]})

    def undo(self):
        print("undo", self.position)
        if len(self.stack) != 0 and self.position != 0:
            self.position -= 1
            self.display_state()
        print(self.position)
    
    def redo(self):
        print("redo", self.position)
        if len(self.stack) != 0 and self.position != len(stack) - 1:
            self.position += 1
            self.display_state()
        print(self.position)

    def display_state(self):
        print(self.position)
        selected_state = self.stack[self.position - 1]
        self.parent.changed = selected_state["changed"]
        self.parent.marked = selected_state["marked"]
        #print("updating to", selected_state)
        self.parent.update_all()

    def action(self):
        print("deleting", self.stack[self.position:])
        del self.stack[self.position:]
        self.position += 1
        print("after deletion", ["".join(el["changed"]) for el in self.stack])
        self.save_state()
        print("position is now", self.position)
        print("saved is now", ["".join(el["changed"]) for el in self.stack])
        print("id's are", [id(el["changed"]) for el in self.stack])

class Graph(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Window")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas=tk.Canvas(self, width=600, height=300)
        self.canvas.grid(row=0, column=0, sticky="NESW")
##        self.canvas.bind("<Configure>", self.on_resize)
        self.t_screen=turtle.TurtleScreen(self.canvas)
        self.t_screen.delay(0)
##        self.t_screen.tracer(0, 0)
        self.t=turtle.RawTurtle(self.t_screen)
        self.t.setpos(100, 100)
##        self.t_screen.update()
        self.canvas.addtag_all("all")
        self.mainloop()

    def on_resize(self, event):
        change_scale_x=event.width/self.canvas.width
        change_scale_y=event.height/self.canvas.height
        self.canvas.width=event.width
        self.canvas.height=event.height
        self.canvas.config(width=self.canvas.width, height=self.canvas.height)
        self.scale("all",0,0,change_scale_x, change_scale_y)        
    
if __name__ == "__main__":
    app=Main()
