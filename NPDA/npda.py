from Grammar.grammar import sentence
import copy

flag = False


class ruler():
    def __init__(self, status, segment) -> None:
        self.status = status
        self.segment = segment
        # 非终结符头的栈推导
        self.Vn_stack_top = segment.get_left()
        # 终结符号的字符串推导
        self.Vt_str_top = segment.get_right()[0]
        # 推导后押入栈中
        self.stack_str = (segment.get_right()[1:])

    def print_ruler(self):
        print("[",
              self.status,
              ", ",
              self.Vt_str_top,
              ", ",
              self.Vn_stack_top,
              "]",
              end='')


class NPDA():
    def __init__(self, sen_list) -> None:
        self.sen_list = sen_list
        print("-" * 10, "create NPDA...", "-" * 10)
        self.start_status = 0
        self.ruler_list = []
        self.ruler_dict = {}

    def print_sen_format(self):
        for sen in self.sen_list:
            print(sen.get_left(), '-', sen.get_right())

    def form_ruler(self):
    # 形成可以根据生产式找到推理的字典
        # 加入开始状态
        self.ruler_list.append(ruler(0, sentence('z-εSz')))
        for segment in self.sen_list:
            self.ruler_list.append(ruler(1, segment))
        self.ruler_dict[self.ruler_list[0]] = [[
            1, self.ruler_list[0].stack_str
        ]]
        # 对中间的产生式按情况处理
        for r in self.ruler_list[1:]:
            if r.stack_str != '':
                if r not in self.ruler_dict:
                    self.ruler_dict[r] = [[1, r.stack_str]]
                else:
                    self.ruler_dict[r].append([1, r.stack_str])
            else:
                if r not in self.ruler_dict:
                    self.ruler_dict[r] = [[1, 'ε']]
                else:
                    self.ruler_dict[r].append([1, 'ε'])
        # 加入结束的状态
        self.ruler_list.append(ruler(1, sentence('z-εz')))
        self.ruler_dict[self.ruler_list[-1]] = [[
            2, self.ruler_list[-1].stack_str
        ]]

    def print_rulers(self):
        for ruler in self.ruler_list:
            ruler.print_ruler()
            print(" => ", self.ruler_dict[ruler])


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

    def front(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)

    def isEmpty(self):
        return self.stack == []
    
    def get_stack(self):
        return self.stack

    def print(self):
        print(self.stack)


def dfs(status, string, stack, r_list, r_dict, index):
    '''
        status: 目前的状态，基本上就0、1、2三种（开始、进行、结束）
        string: 要推理的字符串
        stack: 辅助推理的栈
        r_list: 文法所在的列表
        r_dict: 经过推理推理后的产生式字典
        index: 当前推理的字符串索引
        思路: 打一个深搜来完成推理
    '''
    # 一般来讲把index或者状态到达2就算完成
    if index>=len(string) or (stack.front() == 'z' and status == 2):
        print("找到了一种匹配！")
        global flag
        flag = True
        # print("-" * 10, "end inference...  成🌶", "-" * 10)
        return
    char = string[index]
    top = stack.front()
    trans_ruler_list = []
    # 根据推理的字符找到可以用的产生式
    for ruler in r_list:
        if ruler.status == status and ruler.Vt_str_top == char and ruler.Vn_stack_top == top:
            trans_ruler_list.append(ruler)
    # 找不到说明可以结束搜索了(意味着推理错误，产生式不可用)
    if trans_ruler_list == []:
        print("涅马的， 寄🌶")
        return
    # 找到产生式后开始搜索
    for ruler in trans_ruler_list:
        process_res = r_dict[ruler][0]        
        back_pack = [copy.deepcopy(stack), index, status]

        print(string, "index :", index)
        stack.pop()
        print("use: ")
        ruler.print_ruler()
        print(" => ", r_dict[ruler])
        if process_res[1] != 'ε':   
            temp_list = list(process_res[1])
            temp_list.reverse()
            for i in temp_list:
                stack.push(i)
            print("now the stack is :", stack.print())
            index = index + 1
            status = process_res[0]
            dfs(status, string, stack, r_list, r_dict, index)
            print("恢复...")
            status = back_pack[2]
            index = back_pack[1]
            stack = back_pack[0]
            stack.print()
        else:
            print("now the stack is :", stack.print())
            index = index + 1
            status = process_res[0]
            dfs(status, string, stack, r_list, r_dict, index)
            status = back_pack[2]
            index = back_pack[1]
            stack = back_pack[0]
    pass


def NPDA_inference(npda, string):
    npda.print_rulers()
    # 初始化状态
    string = 'ε' + string + 'ε'
    string_stack = Stack()
    string_stack.push('z')
    index = 0
    status = 0
    print("-" * 10, "start inference...", "-" * 10)
    # 开始搜索
    dfs(status, string, string_stack, npda.ruler_list, npda.ruler_dict, index)
    global flag
    # 结束处理，用一个全局变量表示推理结果
    if flag is True:
        print("-" * 10, "end inference...  成🌶", "-" * 10)
    else:
        print("-" * 10, "end inference...  寄完🌶", "-" * 10)
    pass