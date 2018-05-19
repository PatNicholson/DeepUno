import wx, os, random, time, random
import sys
from objects import *
from control import Control
from heuristic_decision_tree import Heuristic_dt
from heuristic_v2 import Heuristic_v2

def card_from_name(filename):
    [color,value] = filename.split('_')
    flag = 0
    if color == 'black':
        color = None
    if value == 'reverse':
        return Card(10,color,1)
    elif value == 'skip':
        return Card(10,color,2)
    elif value == '+2':
        return Card(10,color,3)
    elif value == 'wildcard':
        return Card(10,color,4)
    elif value == '+4':
        return Card(10,color,5)
    else:
        return Card(int(value),color,0)
    
def name_from_card(card):
    name = ''
    if card.color == None:
        name += 'black_'
    else:
        name += card.color+'_'
    
    if card.flag == 0:
        return card.color+'_'+str(card.value)
    elif card.flag == 1:
        return card.color+'_'+'reverse'
    elif card.flag == 2:
        return card.color+'_'+'skip'
    elif card.flag == 3:
        return card.color+'_'+'+2'
    elif card.flag == 4:
        return 'black_wildcard'
    elif card.flag == 5:
        return 'black_+4'
    
def playable(game,card):
    if card.flag >= 4:
        return True
    if card.value == game.recent_played_card.value:
        return True
    if card.color == game.recent_played_card.color:
        return True
    if card.color == game.wild_color:
        return True

class UnoGame(wx.Frame):
    def __init__(self, ai_type):
        #set up game engine
        self.game = UNO_Game(Deck())
        self.game.player1 = Player(self.game,'P1')
        self.ai_type = ai_type
        if self.ai_type == 'DT':
            self.game.player2 = Heuristic_dt(self.game,'P2')
            print('Playing against Decision Tree Player')
        elif self.ai_type == 'V2':
            self.game.player2 = Heuristic_v2(self.game,'P2')
            print('Playing against Second Heuristic Player')
        else:
            self.game.player2 = Control(self.game,'P2') #control player is default
            print('Playing against Random Player')
        
        #set up frame
        wx.Frame.__init__(self, None, title='Uno')
        self.SetSize((900,700))
        self.Move((50,25))
        self.panel1 = wx.Panel(self)
        
        #fill player 1's hand and top discard card
        p1hand = []
        for c in self.game.player1.hand.cards:
            p1hand.append(name_from_card(c))
        discard = name_from_card(self.game.discard_pile.cards[0])
        
        #create player 1's hand and give name of file name
        self.P1Cards =[]
        self.P2Cards = []
        self.P1HandSize = 7
        self.P2HandSize = 7
        black_card = wx.Image('./images/black.png',wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        for i in range(7): #add actual cards
            card_png = './images/'+p1hand[i]+'.png'
            card = wx.Image(card_png,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.P1Cards.append(wx.StaticBitmap(self.panel1,wx.ID_ANY, card,name=p1hand[i]))
            self.P2Cards.append(wx.StaticBitmap(self.panel1,wx.ID_ANY, black_card,name=str(i)))
            
        for i in range(7,24): #add hidden spaces for possible future cards
            self.P1Cards.append(wx.StaticBitmap(self.panel1,wx.ID_ANY, black_card,name=str(i)))
            self.P1Cards[i].Hide()
            self.P2Cards.append(wx.StaticBitmap(self.panel1,wx.ID_ANY, black_card,name=str(i)))
            self.P2Cards[i].Hide()
            
        #bind left click to each card in player 1's hand
        for img in self.P1Cards:
            img.Bind(wx.EVT_LEFT_DOWN, self.play)
        #bind to draw pile
        self.draw_pile = wx.StaticBitmap(self.panel1,wx.ID_ANY, black_card,name='Draw')
        self.draw_pile.Bind(wx.EVT_LEFT_DOWN, self.draw)
      
        #Visual Layout
        self.hbox = wx.BoxSizer(wx.VERTICAL)
        
        font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        lbl = wx.StaticText(self.panel1,-1,style = wx.ALIGN_LEFT)
        lbl.SetFont(font) 
        lbl.SetLabel(" Discard        Draw")
        self.hbox.Add(lbl, proportion=0, flag = wx.LEFT | wx.TOP, border = 10)
        
        gs1 = wx.GridSizer(1, 2, 15, 15)
        card = wx.Image('./images/'+discard+'.png',wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.discard = wx.StaticBitmap(self.panel1,wx.ID_ANY, card,name=discard)
        gs1.Add(self.discard)
        gs1.Add(self.draw_pile)
        self.hbox.Add(gs1, proportion=0, flag = wx.LEFT | wx.TOP, border = 10)
        
        lbl1 = wx.StaticText(self.panel1,-1,style = wx.ALIGN_LEFT)
        lbl1.SetFont(font) 
        lbl1.SetLabel("Player 2")
        self.hbox.Add(lbl1, proportion=0, flag = wx.LEFT | wx.TOP, border = 10)
        
        gs2 = wx.GridSizer(2, 12, 15, 15)
        gs2.AddMany(self.P2Cards)
        self.hbox.Add(gs2, proportion=0, flag = wx.LEFT | wx.TOP, border = 10)
        
        lbl2 = wx.StaticText(self.panel1,-1,style = wx.ALIGN_LEFT)
        lbl2.SetFont(font) 
        lbl2.SetLabel("Player 1")
        self.hbox.Add(lbl2, proportion=0, flag = wx.LEFT | wx.TOP, border = 10)
        
        self.gs3 = wx.GridSizer(2, 12, 15, 15)
        self.gs3.AddMany(self.P1Cards)
        self.hbox.Add(self.gs3, proportion=0, flag = wx.LEFT | wx.TOP, border = 10)
        
        self.panel1.SetSizer(self.hbox)
        self.Show()

    #----------------------------------------------------------------------
    def popup_win(self,msg):
        popup = wx.PopupTransientWindow(self,wx.SIMPLE_BORDER)
        popup.SetBackgroundColour(wx.WHITE)
        text = wx.StaticText(popup, label=msg)
        text.SetFont(wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD))
        sz = text.GetBestSize()
        popup.SetSize( (sz.width, sz.height))
        pos = self.ClientToScreen( (0,0) )
        sz2 =  self.GetSize()
        psz = popup.GetSize()
        popup.SetPosition(wx.Point(pos[0]+0.5*sz2[0]-0.5*psz[0],pos[1]+0.15*sz2[1]))
        popup.Popup()
        
    def draw_helper(self,card_drawn):
        drawn_card = name_from_card(card_drawn)
        card_png = './images/'+drawn_card+'.png'
        card = wx.Image(card_png,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        if self.P1HandSize < len(self.P1Cards):
            self.P1Cards[self.P1HandSize].SetBitmap(card)
            self.P1Cards[self.P1HandSize].SetName(drawn_card)
            self.P1Cards[self.P1HandSize].Show()
            self.P1HandSize += 1
        else:
            self.popup_win("too many cards")
    
    def draw(self, event):
        if self.game.player1.possible_card():
            print('cannot draw, you can play a card')
            return
        card_drawn = self.game.player1.draw()
        self.draw_helper(card_drawn)   
        self.opp_play()
    
    def play(self, event):
        #get card clicked on, hide corresponding card image
        newCard = event.GetEventObject()
        card_played = card_from_name(newCard.GetName())
        
        if not playable(self.game,card_played):
            print('cannot play that card')
            return
        if newCard.IsShown():
            self.game.player1.discard(card_played)
            #add to discard
            self.discard.SetBitmap(newCard.GetBitmap())
            self.discard.SetName(newCard.GetName())
            
            for i in range(self.P1Cards.index(newCard),self.P1HandSize-1):
                self.P1Cards[i].SetBitmap(self.P1Cards[i+1].GetBitmap())
                self.P1Cards[i].SetName(self.P1Cards[i+1].GetName())
                self.P1Cards[i].Refresh()
            self.P1Cards[self.P1HandSize-1].Hide()
            self.P1HandSize -= 1
            
            self.game.wild_color = None
            #handle special cards
            if card_played.flag == 3: #draw 2
                self.game.player2.draw()
                self.game.player2.draw()
                self.P2Cards[self.P2HandSize].Show()
                self.P2Cards[self.P2HandSize+1].Show()
                self.P2HandSize += 2
            elif card_played.flag == 4: #wild card (change later to add color selection)
                self.game.wild_color = 'blue'
                dlg = wx.TextEntryDialog(self, 'Which color is the wildcard?')
                dlg.ShowModal()
                tmp = dlg.GetValue()
                if tmp in ["red", "blue", "green", "yellow"]:
                    self.game.wild_color = tmp
            elif card_played.flag == 5: #wild draw 4 (change later to add color selection)
                self.game.wild_color = 'blue'
                dlg = wx.TextEntryDialog(self, 'Which color is the wildcard?')
                dlg.ShowModal()
                tmp = dlg.GetValue()
                if tmp in ["red", "blue", "green", "yellow"]:
                    self.game.wild_color = tmp
                for i in range(4):
                    self.game.player2.draw()
                    self.P2Cards[self.P2HandSize].Show()
                    self.P2HandSize += 1
            
            if self.P1HandSize == 0:
                self.end_game(1)
            elif (card_played.flag == 0) or (card_played.flag >= 3):
                self.opp_play()
        
    def opp_play(self):
        [play_type,card,self.game.wild_color] = self.game.player2.play()
        msg = "Player 2 draws a card"
        if play_type == 0:
            played_card = name_from_card(card)
            msg = "Player 2 plays a " + played_card
            #add to discard
            self.discard.SetBitmap(wx.Image('./images/'+played_card+'.png',wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.discard.SetName(played_card)
            
            self.P2Cards[self.P2HandSize-1].Hide()
            self.P2HandSize -= 1
            
            if card.flag >= 4:
                msg += " with color " + self.game.wild_color
            
            if card.flag == 3:
                card_drawn = self.game.player1.draw()
                self.draw_helper(card_drawn)
                card_drawn = self.game.player1.draw()
                self.draw_helper(card_drawn)
            elif card.flag == 5:
                for i in range(4):
                    card_drawn = self.game.player1.draw()
                    self.draw_helper(card_drawn)
            
            if self.P2HandSize == 0:
                self.end_game(0)
            elif (card.flag == 1) or (card.flag == 2):
                self.opp_play()
            else:
                self.popup_win(msg)
        else:
            print("drew card")
            self.P2Cards[self.P2HandSize].Show()
            self.P2HandSize += 1
            self.popup_win(msg)
        
    def end_game(self,winner):
        if winner == 1:
            self.popup_win("You win")
        else:
            self.popup_win("You lose")
        #reset game (new game)
        
        #Restart:
        #set up game engine
        self.game = UNO_Game(Deck())
        self.game.player1 = Player(self.game,'P1')
        self.game.player2 = Control(self.game,'P2') #control player is default
        if self.ai_type == 'bestfirst':
            print('this ai not yet implemented')
            
        #fill player 1's hand and top discard card
        p1hand = []
        for c in self.game.player1.hand.cards:
            p1hand.append(name_from_card(c))
        discard = name_from_card(self.game.discard_pile.cards[0])
        
        #create player 1's hand
        self.P1HandSize = 7
        self.P2HandSize = 7
        self.discard.SetBitmap(wx.Image('./images/'+discard+'.png',wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.discard.SetName(discard)
        for i in range(7): #add actual cards
            card_png = './images/'+p1hand[i]+'.png'
            self.P1Cards[i].SetBitmap(wx.Image(card_png,wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.P1Cards[i].SetName(p1hand[i])
            self.P1Cards[i].Show()
            self.P2Cards[i].Show()
        for i in range(7,24):
            self.P1Cards[i].Hide()
            self.P2Cards[i].Hide()
        self.Show()

    
if __name__ == '__main__':
    app = wx.App(False)
    frame = UnoGame(sys.argv[1])
    app.MainLoop()