from tkinter import *                                              # tkinter for GUI
import requests, bs4                                               # request url and bs4 for html parsing
import webbrowser                                                  # open default web browser

#webbrowser.open('https://anoboy.video/', new=1)

# The main objective of this project:
# 1. Get the on-going anime schedule in GUI
# 2. Open the website based on anime title


class AnimeListbox(Frame):                                          # Make a class that inherite the tkinter Frame
    def __init__(self, animelist, urllist=None, parent=None):       # This is what will the class do when instantiated
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.urlist = urllist
        self.makeListBox(animelist)

    def makeListBox(self, animelist):                               # Make GUI widgets contain anime titles
        sbar = Scrollbar(self)
        list = Listbox(self, width=100, relief=SUNKEN)
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)

        for index, anime in enumerate(animelist):
            list.insert(index, anime)
        list.config(selectmode=SINGLE, setgrid=1)
        list.bind('<Double-1>', self.selectAnime)                   # Bind the anime titles with double-click command
        self.animelist = list

    def selectAnime(self, event):                                   # Determine what event will occur when the user
        index = self.animelist.curselection() # double click        # double click the anime titles
        index = index[0]
        self.openBrowser(self.urlist[index])

    def openBrowser(self, url):                                     # It will open your web browser and redirect you to
        webbrowser.open(url, new=1)                                 # your selected anime website.


def htmlParser():                                                   # Parse the website html code
    url = 'https://anoboy.video'                                    # Target: anoboy.video
    link = requests.get(url)
    soup = bs4.BeautifulSoup(link.content, 'html.parser')

    animeminer = soup.find_all('div', {'class':'amvj'})             # Find all anime titles
    animelist = []
    for anime in animeminer:
        animelist.append(anime.get_text())

    urlminer = soup.find_all('a', {'title':[animelist]})            # Find all anime titles urls
    urlist = []
    for url in urlminer:
        x = url.get('href')
        urlist.append(x)

    return animelist, urlist

if __name__ == '__main__':                                          # Code execution
    win = Tk()
    win.title('Anime List Schedule 2020')
    Label(win, text='Source: Anoboy.Video').pack()
    animelist, urlist = htmlParser()
    AnimeListbox(animelist, urlist, parent=win).mainloop()
