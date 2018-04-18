import wx, os, random, time, random

class UnoGame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Uno')
        self.SetSize((900,700))
        self.Move((50,25))
        self.panel1 = wx.Panel(self)
        
        
        #define how big game is...can be useful for making skill options later
        #self.numPairs = 12
        
     
        #get all images in directory called "Images" & shuffle order
        #self.imageArray = GetJpgList("./Images")
        #random.shuffle(self.imageArray)
        
        #create array with how many cards needed and double it to make matched pairs        
        #self.imagePairs = self.imageArray[0:self.numPairs]
        #self.imagePairs = self.imagePairs * 2

        #because we doubled, we need to re-shuffle order
        #random.shuffle(self.imagePairs)
        
        #PRINT KEY TO TERMINAL SO YOU CAN QUICKLY SOLVE
#         countrow=0
#         for card in self.imagePairs:
#             countrow +=1
#             if countrow%6 == 0:
#                 print card
#             else:
#                 print card,
        
        #replace later with randomly generated first hand & top card
        p1hand = ['blue_0','green_2','green_3','green_5','red_8','black_wildcard','blue_reverse']
        discard = 'red_6'
        
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
    
    def draw(self, event):
        print("drawing card")
        drawn_card = "red_+2"
        card_png = './images/'+drawn_card+'.png'
        card = wx.Image(card_png,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        if self.P1HandSize < len(self.P1Cards): #add check for if none of their cards can be played
            self.P1Cards[self.P1HandSize].SetBitmap(card)
            self.P1Cards[self.P1HandSize].SetName(drawn_card)
            self.P1Cards[self.P1HandSize].Show()
            self.P1HandSize += 1
        else:
            self.popup_win("You have a playable card")
            
        self.opp_play()
    
    def play(self, event):
        
        #get card clicked on, hide corresponding card image
        newCard = event.GetEventObject()
        print("playing card " + newCard.GetName())
        if newCard.IsShown(): #also should check if it's a legal play
            #add to discard
            self.discard.SetBitmap(newCard.GetBitmap())
            self.discard.SetName(newCard.GetName())
            
            for i in range(self.P1Cards.index(newCard),self.P1HandSize-1):
                self.P1Cards[i].SetBitmap(self.P1Cards[i+1].GetBitmap())
                self.P1Cards[i].SetName(self.P1Cards[i+1].GetName())
                self.P1Cards[i].Refresh()
            self.P1Cards[self.P1HandSize-1].Hide()
            self.P1HandSize -= 1
            
            if self.P1HandSize == 0:
                self.end_game(1)
            else:
                self.opp_play()
        
    def opp_play(self):
        #opponent randomly draws a card or plays a card (change when we have actual AI player)
        print('opponent playing')
        msg = "Player 2 draws a card"
        if random.random() > 0.4:
            print("played card")
            played_card = "green_4" #replace with actual card selected by AI
            msg = "Player 2 plays a " + played_card
            #add to discard
            self.discard.SetBitmap(wx.Image('./images/'+played_card+'.png',wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.discard.SetName(played_card)
            
            self.P2Cards[self.P2HandSize-1].Hide()
            self.P2HandSize -= 1
        else:
            print("drew card")
            self.P2Cards[self.P2HandSize].Show()
            self.P2HandSize += 1
        
        if self.P2HandSize == 0:
            self.end_game(0)
        else:
            self.popup_win(msg)
        
    def end_game(self,winner):
        if winner == 1:
            self.popup_win("You win")
        else:
            self.popup_win("You lose")
        #reset game (new game)
        
        #replace later with randomly generated first hand & top card
        p1hand = ['blue_0','green_2','green_3','green_5','red_8','black_wildcard','blue_reverse']
        discard = 'blue_skip'
        
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

##get all JPEGs in a directory that is passed and return image names array
##Note I found this code snippet here:   http://wiki.wxpython.org/wxStaticBitmap
#def GetJpgList(loc):
#    jpgs = [f for f in os.listdir(loc) if f[-4:] == ".jpg"]
#    #print "JPGS are:", jpgs
#    return [os.path.join(loc, f) for f in jpgs]
      
    
if __name__ == '__main__':
    app = wx.App(False)
    frame = UnoGame()
    app.MainLoop()