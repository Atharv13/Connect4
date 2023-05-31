import random
import pygame
import numpy
import sys
import math
import time
from pygame.locals import*
board=[]
coin_loc=(0,0)
blue=(25,190,255)
black=(0,0,0)
red=(255,0,0)
yellow=(255,255,0)
white=(255,255,255)
green=(0,255,0)
for i in range(7):
    board.append(['-','-','-','-','-','-'])

def show_board(b):
    print()
    print(*list(range(1,8)),sep=' ')
    print()
    for i in range(1,7):
        for j in range(1,8):
            print(b[j-1][i-1],end=' ')
        if j%7==0:
            print(end='\n')

def add_coin(j,color,b):
    global coin_loc
    if b[j-1][5]=='-':
        b[j-1][5]=color
        coin_loc=(j-1,5)
        return None
    for i in range(5):
        if b[j-1][i]=='-' and (b[j-1][i+1]=='R' or b[j-1][i+1]=='Y'):
            b[j-1][i]=color
            coin_loc=(j-1,i)
            return None
    return None

def add_coinvirtual(j,color,b):
    global coin_loc_v
    if b[j-1][5]=='-':
        b[j-1][5]=color
        coin_loc_v=(j-1,5)
        return None
    for i in range(5):
        if b[j-1][i]=='-' and (b[j-1][i+1]=='R' or b[j-1][i+1]=='Y'):
            b[j-1][i]=color
            coin_loc_v=(j-1,i)
            return None
    return None

def identical(list):
    if len(list)==0:
        return False
    return (list.count(list[0]) == len(list) and (list[0]=='R' or list[0]=='Y'))
digonal1=[]
digonal2=[]
digonal1_v=[]
digonal2_v=[]
def winning_move(b):
    global coin_loc
    (j_0,i_0)=coin_loc
    i_d1,i_d2,j_d1,j_d2=i_0,i_0,j_0,j_0
    for i in range(6):
        if i_d1==5 or j_d1==0:
            break
        i_d1+=1
        j_d1-=1
    for i in range(7):
        if i_d2==5 or j_d2==6:
            break
        i_d2+=1
        j_d2+= 1
    for j in range(4):
        row=[b[j+k][i_0] for k in range(4)]
        if j!=3:column=[b[j_0][j+k] for k in range(4)]
        else:column=[]
        for k in range(4):
            if (((j_d1+j+k) in range(7)) and ((i_d1-j-k) in range(6))):
                #print(f'j{j}k{k}','appending in d1: ',j_d1+j+k,',',i_d1-j-k)
                digonal1.append(b[j_d1+j+k][i_d1-j-k])
        #print(f'diigonal1{digonal1}')
        if len(digonal1)==4 and identical(digonal1):
            t=digonal1[0]
            digonal1.clear()
            return(True,t)
        digonal1.clear()
        for k in range(4):
            if (((j_d2-j-k) in range(7)) and((i_d2-j-k) in range(6))):
                #print(f'j{j}k{k}','appending in d2: ',j_d2-j-k,',',i_d2-j-k)
                digonal2.append(b[j_d2-j-k][i_d2-j-k])
        #print(f'diigonal2{digonal2}')
        if len(digonal2)==4 and identical(digonal2):
            t_1=digonal2[0]
            digonal2.clear()
            return(True,t_1)
        digonal2.clear()
        #print(f'coinloc{coin_loc}(id1,jd1,id2,jd2)({i_d1}{j_d1}{i_d2}{j_d2})\nrow{row}\ncolumn{column}')
        if identical(row):return(True,row[0])
        if identical(column):return(True,column[0])
    return(False,None)

def get_score_col(b,j):
    global c_c
    temporary_board=[row[:] for row in b]
    #show_board(temporary_board)
    add_coinvirtual(j,c_c,temporary_board)
    #show_board(temporary_board)
    return get_score(temporary_board,c_c)+4-j%4
def get_max_col(b):
    scores=[]
    for i in range(1,8):
        scores.append(get_score_col(board,i))
    print(scores)
    return scores.index(max(scores))+1
def get_score(b,piece):
    global coin_loc_v,digonal1_v,digonal2_v
    score=0
    (j_0,i_0)=coin_loc_v
    i_d1,i_d2,j_d1,j_d2=i_0,i_0,j_0,j_0
    fours_list=[]
    for i in range(6):
        if i_d1==5 or j_d1==0:
            break
        i_d1+=1
        j_d1-=1
    for i in range(7):
        if i_d2==5 or j_d2==6:
            break
        i_d2+=1
        j_d2+= 1
    print('\ngetting fours list')
    for j in range(4):
        print('J is:',j)
        row=[b[j+k][i_0] for k in range(4)]
        print('nrow:',row)
        fours_list.append(row)
        if j!=3:
            column=[b[j_0][j+k] for k in range(4)]
            fours_list.append(column)
        else:column=[]
        print('column:',column)
        for k in range(4):
            if (((j_d1+j+k) in range(7)) and ((i_d1-j-k) in range(6))):
                digonal1_v.append(b[j_d1+j+k][i_d1-j-k])
        for k in range(4):
            if (((j_d2-j-k) in range(7)) and((i_d2-j-k) in range(6))):
                digonal2_v.append(b[j_d2-j-k][i_d2-j-k])
        #print('digonal1_v is',digonal1_v)
        if len(digonal1_v)==4:
            fours_list.append(digonal1_v)
            print('digonal1_v:',digonal1_v)
            #print('appending')
        digonal1_v.clear()
        #print('digonal2_v is',digonal2_v)
        if len(digonal2_v)==4:
            fours_list.append(digonal2_v)
            print('digonal2_v:',digonal2_v)
            #print('appending')
        digonal2_v.clear()
    for ele in fours_list:
        if ele.count(piece)==4:
            score+=3000
        elif (ele.count('-')==1 and ele.count(piece)==3):
            #print(ele, 'adding 300')
            score+=300
        elif (ele.count(piece)==2 and ele.count('-')==2) and (
            ele[0]==ele[1] or ele[1]==ele[2] or ele[2]==ele[3]):
            score+=50
            #print(ele, 'adding 50')
        elif (ele.count(piece)==1 and ele.count('-')==3):
            score+=4
            #print(ele, 'adding 4')
    return score

pygame.init()
sqsize=100
width,height=7*sqsize,7*sqsize
size=(width,height)
radius=int(sqsize/2-5)
screen=pygame.display.set_mode(size)
pygame.display.set_caption('Connect4')

def draw_board(b):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen,blue,(c*sqsize,(r+1)*sqsize,sqsize,sqsize))
            pygame.draw.circle(screen,black,(int(c*sqsize+sqsize/2),int((r+1)*sqsize+sqsize/2)),radius)
    for c in range(7):
        for r in range(6):      
            if b[c][r]=='Y':
                pygame.draw.circle(screen,yellow,(int(c*sqsize+sqsize/2),int((r+1)*sqsize+sqsize/2)),radius)             
            elif b[c][r]=='R':pygame.draw.circle(screen,red,(int(c*sqsize+sqsize/2),int((r+1)*sqsize+sqsize/2)),radius)

def empty_board(b):
    for i in range(7):
        for j in range(6):
            if b[i][j]=='R' or b[i][j]=='Y':b[i][j]='-'


#def score_board_col(board=board
def print_game(text,font,s,color,x,y):
    font=pygame.font.SysFont(font,s)
    textobj = font.render(text,True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    screen.blit(textobj, textrect)




def game_2Player():
    running=True
    turn=random.randint(0,1)
    L=[]
    line=(False,'')
    declare_var()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    empty_board(board)
                    running=False
            if event.type== pygame.MOUSEMOTION:
                pygame.draw.rect(screen,black,(0,0,width,sqsize))
                posx=event.pos[0]
                if turn==0:
                    pygame.draw.circle(screen,red,(posx,int(sqsize/2)),radius)
                else:pygame.draw.circle(screen,yellow,(posx,int(sqsize/2)),radius)
            pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                if turn==0:
                    add_coin(int(math.floor(event.pos[0]/100))+1,'R',board)
                    if winning_move(board)[0]:
                        line=(True,'Player1 Wins !!',red)
                else:
                    add_coin(int(math.floor(event.pos[0]/100))+1,'Y',board)
                    if winning_move(board)[0]:
                        line=(True,'Player2 Wins !!',yellow)
                for ele in board:
                    if '-' not in ele:L.append(1)
                if len(L)==7:
                    line=(True,'Match tied')
                else:L.clear()
                turn=(turn+1)%2
            draw_board(board)
            pygame.display.flip()
            if line[0]:
                pygame.draw.rect(screen,black,(0,0,width,sqsize))
                print_game(line[1],'French Script MT',100,line[2],350,50)
                pygame.display.flip()
                time.sleep(2)
                empty_board(board)
                running=False





color={'R':red,'Y':yellow}
def declare_var():
    global p_c,c_c,turn
    turn=random.choice([0,1])
    p_c=random.choice(['R','Y'])
    if p_c=='R':c_c='Y'
    else:c_c='R'
def game_1Player():
    global c_c,p_c,turn
    running=True
    L=[]
    line=(False,'')
    declare_var()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    empty_board(board)
                    running=False
            if event.type== pygame.MOUSEMOTION:
                pygame.draw.rect(screen,black,(0,0,width,sqsize))
                posx=event.pos[0]
                if turn==0:
                    pygame.draw.circle(screen,color[p_c],(posx,int(sqsize/2)),radius)
                else:pygame.draw.circle(screen,color[c_c],(posx,int(sqsize/2)),radius)
            pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                if turn==0 and (line[0]!=True):
                    add_coin(int(math.floor(event.pos[0]/100))+1,p_c,board)
                    if winning_move(board)[0]:
                        line=(True,'Player1 Wins !!')
                    turn=(turn+1)%2
                    draw_board(board)
                    pygame.display.flip
        draw_board(board)
        pygame.display.flip
        if turn==1 and (line[0]!=True):
            #pygame.time.wait(500)
            c=get_max_col(board)
            add_coin(c,c_c,board)
            if winning_move(board)[0]:
                line=(True,'Player2 Wins !!')
            turn=(turn+1)%2
            draw_board(board)
            pygame.display.flip
        for ele in board:
            if '-' not in ele:L.append(1)
        if len(L)==7:
            line=(True,'Match tied')
            draw_board(board)
            pygame.display.flip()
        else:L.clear()
        if line[0]:
            pygame.draw.rect(screen,black,(0,0,width,sqsize))
            print_game(line[1],'French Script MT',100,green,350,50)
            pygame.display.flip()
            time.sleep(2)
            empty_board(board)
            running=False
def main_menu():
    while True:
        screen.fill((0,0,0))
        button_play = pygame.Rect(150,325,100,50)
        button_quit = pygame.Rect(450,325,100,50)
        button_bot  = pygame.Rect(250,575,200,50)
        pygame.draw.rect(screen,red,button_quit)
        pygame.draw.rect(screen,red,button_play)
        pygame.draw.rect(screen,yellow,button_bot)
        print_game('Play','Sans Serif',40,yellow,200,350)
        print_game('Quit','Sans Serif',40,yellow,500,350)
        print_game('vs computer','Sans Serif',40,black,350,600)
        
        mx, my = pygame.mouse.get_pos()
        if button_play.collidepoint((mx, my)):
            if click:
                game_2Player()
        if button_quit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        if button_bot.collidepoint((mx, my)):
            if click:
                game_1Player() 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.flip()

main_menu()
