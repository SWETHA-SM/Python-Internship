from tkinter import *
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
root = Tk()
L= Label(root, text = "SM'S PRICE COMPARISON",font=("Time Roman bold", 14),fg="white",bg="black").place(x = 100, y = 0)
root.geometry("450x200")
class Price_compare:

    def __init__(self, master):
        self.var = StringVar()
        self.var_flipkart = StringVar()
        self.var_amzn = StringVar()        
        label = Label(master, text="Enter The Product",font=("Time Roman bold", 12)).place(x = 0, y = 60)
        entry = Entry(master, textvariable=self.var,font=20).place(x = 140, y = 63)
        button_find = Button(master, text="Find", bd=4,font=30, command=self.find).place(x = 180, y = 100)

    def find(self):
        self.product = self.var.get()
        self.product_arr = self.product.split()
        self.n = 1
        self.key = ""
        self.title_flip_var = StringVar()
        self.title_amzn_var = StringVar()
        self.variable_amzn = StringVar()
        self.variable_flip = StringVar()
        for word in self.product_arr:
            if self.n == 1:
                self.key = self.key + str(word)
                self.n += 1
            else:
                self.key = self.key + '+' + str(word)
        self.window = Toplevel(root)
        self.window.title("SM Price Comparison")
        label_title_flip = Label(self.window, text="Flipkart Title:").place(x = 0, y = 0)
        label_flipkart = Label(self.window,text='Flipkart Price (Rs):').place(x = 0, y = 30)      
        entry_flipkart = Entry(self.window, textvariable=self.var_flipkart)
        entry_flipkart.grid(row=1, column=1, sticky=W)        
        label_title_amzn = Label(self.window, text='Amazon Title:')
        label_title_amzn.grid(row=3, column=0, sticky=W)
        label_amzn = Label(self.window, text='Amazon price (Rs):')
        label_amzn.grid(row=4, column=0, sticky=W)        
        entry_amzn = Entry(self.window, textvariable=self.var_amzn)
        entry_amzn.grid(row=4, column=1, sticky=W)
        self.price_flipkart(self.key)
        self.price_amzn(self.key)
        try:
            self.variable_amzn.set(self.matches_amzn[0])
        except:
            self.variable_amzn.set('Product not available')
        try:
            self.variable_flip.set(self.matches_flip[0])
        except:
            self.variable_flip.set('Product not available')
            
        option_amzn = OptionMenu(self.window, self.variable_amzn, *self.matches_amzn)
        option_amzn.grid(row=3, column=1, sticky=W)
        lab_amz = Label(self.window, text='Not this? Try out suggestions by clicking on the title')
        lab_amz.grid(row=3, column=2, padx=4)
        option_flip = OptionMenu(self.window, self.variable_flip, *self.matches_flip)
        option_flip.grid(row=0, column=1, sticky=W)
        lab_flip = Label(self.window, text='Not this? Try out suggestions by clicking on the title')
        lab_flip.grid(row=0, column=2, padx=4)
        button_search = Button(self.window, text='Search', command=self.search, bd=4)
        button_search.grid(row=2, column=2, sticky=E, padx=10, pady=4)
        button_amzn_visit = Button(self.window, text='Visit Site', command=self.visit_amzn, bd=4)
        button_amzn_visit.grid(row=4, column=2, sticky=W)
        button_flip_visit = Button(self.window, text='Visit Site', command=self.visit_flip, bd=4)
        button_flip_visit.grid(row=1, column=2, sticky=W)

    def price_flipkart(self, key):
        url_flip = 'https://www.flipkart.com/search?q=' + str(key) 
        map = defaultdict(list)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        source_code = requests.get(url_flip, headers=self.headers)
        soup = BeautifulSoup(source_code.text, "html.parser")
        self.opt_title_flip = StringVar()
        home = 'https://www.flipkart.com'
        for block in soup.find_all('div', {'class': '_2kHMtA'}):
            title, price, link = None, 'Currently Unavailable', None
            for heading in block.find_all('div', {'class': '_4rR01T'}):
                title = heading.text
            for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                price = p.text[1:]
            for l in block.find_all('a', {'class': '_1fQZEK'}):
                link = home + l.get('href')
            map[title] = [price, link]
        user_input = self.var.get().title()
        self.matches_flip = get_close_matches(user_input, map.keys(), 20, 0.1)
        self.looktable_flip = {}
        for title in self.matches_flip:
            self.looktable_flip[title] = map[title]
        try:
            self.opt_title_flip.set(self.matches_flip[0])
            self.var_flipkart.set(self.looktable_flip[self.matches_flip[0]][0] + '.00')
            self.link_flip = self.looktable_flip[self.matches_flip[0]][1]
        except IndexError:
            self.opt_title_flip.set('Product not found')

    def price_amzn(self, key):
        url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        map = defaultdict(list)
        home = 'https://www.amazon.in'
        source_code = requests.get(url_amzn, headers=self.headers)
        plain_text = source_code.text
        self.opt_title = StringVar()
        self.soup = BeautifulSoup(plain_text, "html.parser")
        for html in self.soup.find_all('div', {'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'}):
            title, price, link = None, 'Currently Unavailable', None
            for heading in html.find_all('span', {'class': 'a-size-large product-title-word-break'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-size-medium a-color-priceBlockBuyingPriceString'}):
                price = p.text
            for l in html.find_all('a', {'class': 'a-link-normal a-text-normal'}):
                link = home + l.get('href')
            map[title] = [price, link]
        user_input = self.var.get().title()
        self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
        self.looktable = {}
        for title in self.matches_amzn:
            self.looktable[title] = map[title]
        try:
            self.opt_title.set(self.matches_amzn[0])
            self.var_amzn.set(self.looktable[self.matches_amzn[0]][0] + '.00')
            self.product_link = self.looktable[self.matches_amzn[0]][1]
        except IndexError:
            self.opt_title.set('Product not found')        
    def search(self):
        amzn_get = self.variable_amzn.get()
        self.opt_title.set(amzn_get)
        product = self.opt_title.get()
        price, self.product_link = self.looktable[product][0], self.looktable[product][1]
        self.var_amzn.set(price + '.00')
        flip_get = self.variable_flip.get()
        flip_price, self.link_flip = self.looktable_flip[flip_get][0], self.looktable_flip[flip_get][1]
        self.var_flipkart.set(flip_price + '.00')
    def visit_amzn(self):
        webbrowser.open(self.product_link)
    def visit_flip(self):
        webbrowser.open(self.link_flip)
c = Price_compare(root)
root.title('Price Comparison Engine')
root.mainloop()
