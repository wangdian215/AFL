# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:21:42 2020

@author: Diane
"""


import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter
from matplotlib.pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  
mpl.rcParams['axes.unicode_minus']=False      
Blueprint = np.zeros((300,200), dtype=np.uint8)
#Blueprint[10:370,:] = 255
Blueprint_height,Blueprint_width = Blueprint.shape[1],Blueprint.shape[0]

class AutoLayout:
    def __init__(self,DESK_Number,DESK_Basic_Size,DESK_Basic_Interval,MeetingDesk_Number,MeetingDesk_Basic_Size,MeetingDesk_Basic_Interval): 
        self.DESK_Number = DESK_Number
        self.DESK_Basic_Size= DESK_Basic_Size
        self.DESK_Basic_Interval = DESK_Basic_Interval
        self.MeetingDesk_Number = MeetingDesk_Number                  
        self.MeetingDesk_Basic_Size=MeetingDesk_Basic_Size             
        self.MeetingDesk_Basic_Interval=MeetingDesk_Basic_Interval
        self.population_size = 500
        self.chromosome_length = self.DESK_Number+self.MeetingDesk_Number
        
    def species_origin(self):
        population=[[]]
    
        for i in range(self.population_size):
            temporary=[]
    
            for j in range(self.chromosome_length):
                temporary.append(random.randint(0,Blueprint_height))
                temporary.append(random.randint(0,Blueprint_width))
                temporary.append(random.randint(0,3))
    
            population.append(temporary)
    
        return population[1:]
    
    
    def areaCalculation(self,population):
        count = 0
        DESK_height,DESK_width = self.DESK_Basic_Size.shape[0]+self.DESK_Basic_Interval,self.DESK_Basic_Size.shape[1]+self.DESK_Basic_Interval
        MeetingDesk_height,MeetingDesk_width = self.MeetingDesk_Basic_Size.shape[0]+self.MeetingDesk_Basic_Interval,self.MeetingDesk_Basic_Size.shape[1]+self.MeetingDesk_Basic_Interval    
        Total_Ref = self.DESK_Number*DESK_height*DESK_width + self.MeetingDesk_Number*MeetingDesk_height*MeetingDesk_width
        SCORE = []
        for p in population:
            basic = np.zeros((Blueprint_width,Blueprint_height), dtype=np.uint8)
            for i in range(self.DESK_Number):
                if p[i*3+2] == 0 or p[i*3+2] == 2:
                    basic[p[i*3]:p[i*3]+DESK_width,p[i*3+1]:p[i*3+1]+DESK_height]=1
                if p[i*3+2] == 1 or p[i*3+2] == 3:
                    basic[p[i*3]:p[i*3]+DESK_height,p[i*3+1]:p[i*3+1]+DESK_width]=1
            for i in range(self.DESK_Number,self.DESK_Number+self.MeetingDesk_Number):
                #basic[p[i*3]:p[i*3]+MeetingDesk_width,p[i*3+1]:p[i*3+1]+MeetingDesk_height]=1
                if p[i*3+2] == 0 or p[i*3+2] == 2:
                    basic[p[i*3]:p[i*3]+MeetingDesk_width,p[i*3+1]:p[i*3+1]+MeetingDesk_height]=1
                if p[i*3+2] == 1 or p[i*3+2] == 3:
                    basic[p[i*3]:p[i*3]+MeetingDesk_height,p[i*3+1]:p[i*3+1]+MeetingDesk_width]=1
                
            score = sum(sum(basic))/Total_Ref
            SCORE.append(score)
            if score == 1:
                count = count + 1
        return SCORE
    
    
    
    def cumsum(self,SCORE):
        for i in range(len(SCORE)-2,-1,-1):
            # range(start,stop,[step])
    
            total=0
            j=0
            while(j<=i):
                total+=SCORE[j]
                j+=1
    
            SCORE[i]=total
            SCORE[len(SCORE)-1]=1
    
    
    def selection(self,population,SCORE,pop):
        new_fitness=[]
    
        total_fitness=sum(SCORE)
    
        for i in range(len(SCORE)):
            new_fitness.append(SCORE[i]/total_fitness)
    
        self.cumsum(new_fitness)
    
        ms=[]
    
        population_length=pop_len=len(population)
    
     
        for i in range(pop_len):
            ms.append(random.random())
    
        ms.sort()
    
        fitin=0
        newin=0
        new_population=new_pop=population
     
    
        while newin<pop_len:
            if(ms[newin]<new_fitness[fitin]):
                new_pop[newin]=pop[fitin]
                newin+=1
            else:
                fitin+=1
        population=new_pop
        
    def crossover(self,population,pc,pop):
    #pc是概率阈值，选择单点交叉还是多点交叉，生成新的交叉个体，这里没用
        pop_len=len(population)
     
        for i in range(pop_len-1):
            cpoint=random.randint(0,len(population[0]))
            #在种群个数内随机生成单点交叉点
            temporary1=[]
            temporary2=[]
     
            temporary1.extend(pop[i][0:cpoint])
            temporary1.extend(pop[i+1][cpoint:len(population[i])])
            #将tmporary1作为暂存器，暂时存放第i个染色体中的前0到cpoint个基因，
            #然后再把第i+1个染色体中的后cpoint到第i个染色体中的基因个数，补充到temporary2后面
     
            temporary2.extend(pop[i+1][0:cpoint])
            temporary2.extend(pop[i][cpoint:len(pop[i])])
            # 将tmporary2作为暂存器，暂时存放第i+1个染色体中的前0到cpoint个基因，
            # 然后再把第i个染色体中的后cpoint到第i个染色体中的基因个数，补充到temporary2后面
            pop[i]=temporary1
            pop[i+1]=temporary2
            # 第i个染色体和第i+1个染色体基因重组/交叉完成
    
    
    def mutation(self,population,pm):
        
        px=len(population)
        
        py=len(population[0])
        
        for i in range(px):
            if(random.random()<pm):
            
                mpoint=random.randint(0,py-1)
                '''
                if(population[i][mpoint]==1):
                
                    population[i][mpoint]=0
                else:
                    population[i][mpoint]=1
                '''
                if mpoint%3 != 2:
                    population[i][mpoint]= population[i][mpoint] + random.uniform(-5,5)
                else:
                    population[i][mpoint]= random.randint(0,3)
     
    def best(self,population,fitness1):
     
        px=len(population)
        bestindividual=[]
        bestfitness=fitness1[0]
     
        for i in range(1,px):
       # 循环找出最大的适应度，适应度最大的也就是最好的个体
            if(fitness1[i]>bestfitness):
     
                bestfitness=fitness1[i]
                bestindividual=population[i]
     
        return [bestindividual,bestfitness]
    
    
    
    #%%
   
    def layout(self):
        population_size=500
        
        chromosome_length=self.DESK_Number+self.MeetingDesk_Number
        pc=0.7
        pm=0.02
         
        #results=[[]]
        fitness1=[]
        #fitmean=[]
        best_fitness = 0
        B = []
        while best_fitness < 1:
            population=pop=self.species_origin()
            SCORE = self.areaCalculation(population)
            best_individual,best_fitness=self.best(population,SCORE)
            self.selection(population,SCORE,pop)
            self.crossover(population,pc,pop)
            self.mutation(population,pm)
            B.append(best_fitness)
            #print(best_fitness)
        
        form = Form(best_individual,self.DESK_Number,self.MeetingDesk_Number,self.DESK_Basic_Size,self.MeetingDesk_Basic_Size)
            
    
class Form:
    def __init__(self,best_individual,DESK_Number,MeetingDesk_Number,DESK_Basic_Size,MeetingDesk_Basic_Size): 
        self.best_individual = best_individual
        self.DESK_Number= DESK_Number
        self.MeetingDesk_Number = MeetingDesk_Number
        self.DESK_Basic_Size = DESK_Basic_Size
        self.MeetingDesk_Basic_Size = MeetingDesk_Basic_Size
        self.root=tkinter.Tk()                    
        self.canvas=tkinter.Canvas()             
        self.figure=self.create_matplotlib() 
        self.create_form(self.figure)        
        self.root.mainloop()
        
 
    def create_matplotlib(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.axis([0,300,0,200])
        for ii in range(self.DESK_Number):
            
            if self.best_individual[ii*3+2]== 0 or self.best_individual[ii*3+2] == 2:
                print('mode1')
                ax.add_patch(
                    plt.Rectangle((self.best_individual[ii*3], self.best_individual[ii*3+1]),
                                  self.DESK_Basic_Size.shape[1],
                                  self.DESK_Basic_Size.shape[0], fill=False,
                                  edgecolor='red', linewidth=3.5)
                )
                ax.text(self.best_individual[ii*3],self.best_individual[ii*3+1],
                    'Desk',
                    bbox=dict(facecolor='blue', alpha=0.5),
                    fontsize=14, color='white')
            if self.best_individual[ii*3+2]== 1 or self.best_individual[ii*3+2] == 3:
                print('mode2')
                ax.add_patch(
                    plt.Rectangle((self.best_individual[ii*3],self.best_individual[ii*3+1]),
                                  self.DESK_Basic_Size.shape[0],
                                  self.DESK_Basic_Size.shape[1], fill=False,
                                  edgecolor='red', linewidth=3.5)
                )
                ax.text(self.best_individual[ii*3],self.best_individual[ii*3+1],
                    'Desk',
                    bbox=dict(facecolor='blue', alpha=0.5),
                    fontsize=14, color='white')
            
            plt.tight_layout()
            plt.draw()
        for ii in range(self.DESK_Number,self.DESK_Number+self.MeetingDesk_Number):
            
            if self.best_individual[ii*3+2]== 0 or self.best_individual[ii*3+2] == 2:
                print('mode1')
                ax.add_patch(
                    plt.Rectangle((self.best_individual[ii*3], self.best_individual[ii*3+1]),
                                  self.MeetingDesk_Basic_Size.shape[1],
                                  self.MeetingDesk_Basic_Size.shape[0], fill=False,
                                  edgecolor='red', linewidth=3.5)
                )
                ax.text(self.best_individual[ii*3],self.best_individual[ii*3+1],
                    'Meeting Desk',
                    bbox=dict(facecolor='blue', alpha=0.5),
                    fontsize=14, color='white')
            if self.best_individual[ii*3+2]== 1 or self.best_individual[ii*3+2] == 3:
                print('mode2')
                ax.add_patch(
                    plt.Rectangle((self.best_individual[ii*3],self.best_individual[ii*3+1]),
                                  self.MeetingDesk_Basic_Size.shape[0],
                                  self.MeetingDesk_Basic_Size.shape[1], fill=False,
                                  edgecolor='red', linewidth=3.5)
                )
                ax.text(self.best_individual[ii*3],self.best_individual[ii*3+1],
                    'Meeting Desk',
                    bbox=dict(facecolor='blue', alpha=0.5),
                    fontsize=14, color='white')
            #plt.axis('off')
            plt.tight_layout()
            plt.draw()             
        
        return fig
 
    def create_form(self,figure):
        
        self.canvas=FigureCanvasTkAgg(figure,self.root)
        self.canvas.draw()  
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
 
        
        toolbar =NavigationToolbar2Tk(self.canvas, self.root) 
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
 

#layout()
#L = AutoLayout(1,np.zeros((100,180), dtype=np.uint8),10,1,np.zeros((110,180), dtype=np.uint8),10)
#L.layout()