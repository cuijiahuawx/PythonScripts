from graphviz import Digraph
import os


class Work:      

    def __init__(self, info):
        self.ES, self.EF, self.LS, self.LF, self.TF, self.FF = [0 for i in range(6)]
        self.e_flag, self.l_flag, self.f_flag = [False for i in range(3)]  
        self.pre_work, self.work, self.time, self.next_work = info.split('-')
        self.time = int(self.time)         
        self.color = False

    def qes_e(self, pre_work):
        self.ES = pre_work.EF
        self.EF = self.ES + self.time
        self.e_flag = True   

    def qes_l(self, nex_work):
        self.LF = nex_work.LS
        self.LS = self.LF - self.time
        self.l_flag = True 

    def qes_f(self, nex_work):
        self.FF = nex_work.ES - self.EF
        self.f_flag = True

    def qes_tf(self):
        self.TF = self.LS - self.ES

    def set_color(self):
        self.color = True   

    def __repr__(self):
        return f""" 
work:{self.work}
{self.pre_work}, {self.work}, {self.time}, {self.next_work}
{self.ES}, {self.EF}, {self.LS}, {self.LF}, {self.TF}, {self.FF}
{self.e_flag}, {self.l_flag}, {self.f_flag}"""


class Network:
    def __init__(self):
        with open('question.txt', 'r', encoding='utf-8') as f:
            question = [i.strip('\n') for i in f.readlines()]
            if '-' in question[-1]:
                self.question = question
                self.plane = 'default'
            else:
                self.question = question[:-1]
                self.plane = question[-1]
        self.dic = dict()
        self.endwork_ls = []
        self.endwork_tf = []

    def set_color(self, work):
        if work.TF == min(self.endwork_tf):
            work.set_color()

    def solve(self):
        for i in self.question:
            self.dic[i.split('-')[1]] = Work(i)
        # 计算ES， EF
        for tag, work in self.dic.items():
            if work.pre_work == 'empty':
                work.EF += work.time
                work.e_flag = True
            elif len(work.pre_work) == 1:
                work.qes_e(self.dic[work.pre_work])
            else:
                work_name = max((self.dic[_].EF,self.dic[_].work) for _ in list(work.pre_work))[1]
                work.qes_e(self.dic[work_name]) 
            if work.next_work == 'empty':
                self.endwork_ls.append(work.EF)     
            self.dic = dict(sorted(self.dic.items(), key=lambda t: t[0],reverse = True))
        # 计算LS， LF
        for tag, work in self.dic.items():
            if work.next_work == 'empty':
                if self.plane != 'default' :
                    work.LF = int(self.plane)
                else:
                    work.LF = max(self.endwork_ls)
                work.LS = work.LF - work.time
                work.l_flag = True
            elif len(work.next_work) == 1:
                work.qes_l(self.dic[work.next_work]) 
            else:
                work_name = min((self.dic[_].LS,self.dic[_].work) for _ in list(work.next_work))[1]
                work.qes_l(self.dic[work_name])
        # 计算TF
        for tag, work in self.dic.items():
            work.qes_tf()
            self.endwork_tf.append(work.TF)
        # 计算FF
        for tag, work in self.dic.items():
            if work.next_work == 'empty':
                work.FF = max(self.endwork_ls) - work.EF
                work.f_flag = True
            elif len(work.next_work) == 1:
                work.qes_f(self.dic[work.next_work])
            else:
                work_name = min((self.dic[_].ES,self.dic[_].work) for _ in list(work.next_work))[1]
                work.qes_f(self.dic[work_name])
        self.dic = dict(sorted(self.dic.items(), key=lambda t: t[0],reverse = False))
        with open('answer.txt', 'w', encoding='utf-8') as f:
            f.write(f'活动：\n----------\n|ES|LS|TF|\n|EF|LF|FF|\n----------\n')
            for a, i in self.dic.items():
                f.write(f'{i.work}:\n{i.ES},{i.LS},{i.TF},\n{i.EF},{i.LF},{i.FF},\n')

    def show(self):
        try:
            f = Digraph(name='result', filename='result.gv', format="png", node_attr={'color': 'lightblue2', 'style': 'filled'})
            f.attr(rankdir='LR', size='10,10')
            def gen_node(work):
                string = f"{work.work}-{work.time}\n{work.ES},{work.LS},{work. TF}\n{work.EF},{work.LF},{work.FF}"
                return string
            for tag, work in self.dic.items():
                self.set_color(work)
                if work.color:
                    f.node(gen_node(work), color='red')
                else:
                    f.node(gen_node(work))

            for tag, work in self.dic.items():
                info = gen_node(work)
                if work.next_work == 'empty':
                    pass
                elif len(work.next_work) == 1:
                    if work.color and self.dic[work.next_work].color:
                        f.edge(info, gen_node(self.dic[work.next_work]), color='red')
                    else:
                        f.edge(info, gen_node(self.dic[work.next_work]))
                else:
                    for i in list(work.next_work):
                        if work.color and self.dic[i].color:
                            f.edge(info, gen_node(self.dic[i]), color='red')
                        else:
                            f.edge(info, gen_node(self.dic[i]))
            f.render(filename='result')
        except:
            pass


qes = Network()
qes.solve()
qes.show()
os.remove("result")