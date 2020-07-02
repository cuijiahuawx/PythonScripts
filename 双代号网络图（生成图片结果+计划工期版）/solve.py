from graphviz import Digraph
import os

class Work:      
    def __init__(self, info):
        self.ES, self.EF, self.LS, self.LF, self.TF, self.FF = [0 for i in range(6)] 
        self.prework, self.work, self.time, self.nexwork = info.split('-')
        self.time = int(self.time)         
        self.color = False
    def setcolor(self):
        self.color = True
    def __repr__(self):
        return f""" 
work:{self.work}
{self.prework}, {self.work}, {self.time}, {self.nexwork}
{self.ES}, {self.EF}, {self.LS}, {self.LF}, {self.TF}, {self.FF}
"""

class Network:
    def __init__(self):
        self.dic = dict(); self.index = []; self.revers = []; self.endtag = []; self.endTF = 0; self.plane = "no";self.calculatime = 0
        with open('question.txt', 'r', encoding='utf-8') as f:
            question = [i.strip('\n') for i in f.readlines()]
        if "-" not in question[-1]:
            self.plane = eval(question[-1])
            question = question[:-1]
        for i in question:
            worktag = i.split('-')[1]
            nextag = i.split('-')[-1]
            self.dic[worktag] = Work(i)
            self.index.append(worktag)
            self.revers = self.index[::-1]
            if nextag == "empty":
                self.endtag.append(worktag)
    def setcolor(self, work):
        if work.TF == self.endTF:
            work.setcolor()
    def solve(self):
        # ES, EF
        for i in self.index:
            work = self.dic[i]
            pretag = work.prework
            if pretag == "empty":
                pass
            elif len(pretag) == 1:
                work.ES = self.dic[pretag].EF
            else:
                work.ES = max([self.dic[i].EF for i in pretag])
            work.EF = work.ES + work.time
        # LS, LF
        for i in self.revers:
            work = self.dic[i]
            nextag = work.nexwork
            if nextag == "empty":
                self.calculatime = max([self.dic[i].EF for i in self.endtag])
                if self.plane == "no":
                    work.LF = self.calculatime
                else:
                    work.LF = self.plane
            elif len(nextag) == 1:
                work.LF = self.dic[nextag].LS
            else:
                work.LF = min([self.dic[i].LS for i in nextag])
            work.LS = work.LF - work.time
        # TF
        for i in self.index:
            work = self.dic[i]
            work.TF = work.LS - work.ES
        # 查找关键线路节点TF值
        self.endTF = min(self.dic[i].TF for i in self.endtag)
        # FF
        for i in self.revers:
            work = self.dic[i]
            nextag = work.nexwork
            endLF = max(self.dic[i].LF for i in self.endtag)
            if nextag == "empty":
                work.FF = endLF - work.EF
            elif len(nextag) == 1:
                work.FF = self.dic[nextag].ES - work.EF
            else:
                work.FF = min([self.dic[i].ES for i in nextag]) - work.EF
        with open('answer.txt', 'w', encoding='utf-8') as f:
            f.write(f'活动：\n----------\n|ES|LS|TF|\n|EF|LF|FF|\n----------\n')
            for a, i in self.dic.items():
                f.write(f'{i.work}:\n{i.ES},{i.LS},{i.TF},\n{i.EF},{i.LF},{i.FF},\n')
        try:
            f = Digraph(name='result', filename='result.gv', format="png", node_attr={'color': 'lightblue2', 'style': 'filled'})
            f.attr(rankdir='LR', size='10,10')
            def gen_node(work):
                string = f"{work.work}-{work.time}\n{work.ES},{work.LS},{work. TF}\n{work.EF},{work.LF},{work.FF}"
                return string
            for i in self.index:
                work = self.dic[i]
                self.setcolor(work)
                if work.color:
                    f.node(gen_node(work), color='red')
                else:
                    f.node(gen_node(work))
            for i in self.index:
                work = self.dic[i]
                info = gen_node(work)
                if work.nexwork == 'empty':
                    pass
                elif len(work.nexwork) == 1:
                    if work.color and self.dic[work.nexwork].color:
                        f.edge(info, gen_node(self.dic[work.nexwork]), color='red')
                    else:
                        f.edge(info, gen_node(self.dic[work.nexwork]))
                else:
                    for i in list(work.nexwork):
                        if work.color and self.dic[i].color:
                            f.edge(info, gen_node(self.dic[i]), color='red')
                        else:
                            f.edge(info, gen_node(self.dic[i]))
            f.render(filename='result')
        except:
            print("生成网络图失败，可能是graphviz软件没有安装，或者没有把该软件加入系统的环境变量，详情参考“程序使用方法文件”")
        
a = Network()
a.solve()
os.remove("result")