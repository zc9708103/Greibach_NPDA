from Grammar.grammar import Grammar
from toGNF.GNF import GNF
from NPDA.npda import NPDA, NPDA_inference


def read_grammar(gra_path):
    print('-' * 10, ' read by .readlines() ', '-' * 10)
    gra_list = []
    with open(gra_path, encoding='utf-8') as file:
        content = file.readlines()
        for gra in content:
            gra_list.append(gra[:len(gra) - 1])
        print('content: ', content, ' type: ', type(content))
    return gra_list


gra_path = 'grammar.txt'
gra_list = read_grammar(gra_path)

# 把语法转为对象类存储, 顺便消除'|'
G = Grammar(gra_list)
# G.print_gra()
G.to_sen_list()
G.print_sen()
print("Vn: ", G.Vn)
print("Vt: ", G.Vt)

# 消除单一产生式
print("-" * 10, 'start reduce single production', "-" * 10)
G.reduce_single_production()
G.print_sen()

# 消除左递归
print("-" * 10, 'start reduce left recursion', "-" * 10)
G.reduce_left_recursion()
G.print_sen()

# 消除空产生式
print("-" * 10, 'start reduce null production', "-" * 10)
G.reduce_null_production()
G.print_sen()

# 消除无用符号
print("-" * 10, 'start reduce useless production', "-" * 10)
G.reduce_useless_production()
G.print_sen()

# 简化产生式（消除重复产生式）
print("-" * 10, 'start reduce repeat production', "-" * 10)
G.reduce_repeat_production()
G.print_sen()

# 构成GNF
gnf = GNF(G)
gnf.simGra_to_GNF()
gnf.print_sen_format()

# 创造NPDA
npda = NPDA(gnf.sen_list)
npda.form_ruler()
# npda.print_rulers()

# 下推
# S => (a)i a (bb)i [i>=0]
string = "ba"
NPDA_inference(npda, string)
