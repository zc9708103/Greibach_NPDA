from Grammar.grammar import Grammar, add1_to_str, sentence


class GNF(Grammar):
    def __init__(self, grammar):
        self.grammar = grammar
        self.sen_list = self.grammar.sen_list
        print("-" * 10, "create GNF...", "-" * 10)

    def print_sen_format(self):
        for sen in self.sen_list:
            print(sen.get_left(), '-', sen.get_right())

    def simGra_to_GNF(self):
    # 将化简后的产生式转换为Greibach范式
        sen_list = self.sen_list
        new_Vn_dict = {}
        # 找到只有一个字符的产生式，并以此或者新的产生式
        for segment in sen_list:
            right = segment.get_right()
            if len(right) != 1:
                for i in range(1, len(right)):
                    # 不在字典中就去形成一个新的产生式
                    if 'a' <= right[i] and right[i] <= 'z' and right[
                            i] not in new_Vn_dict:
                        new_Vn_dict[right[i]] = self.grammar.get_new_Vn()
        # print(new_Vn_dict)
        # 根据字典替换产生式
        for segment in sen_list:
            right = list(segment.get_right())
            if len(right) == 1:
                continue
            for i in range(1, len(right)):
                if 'a' <= right[i] and right[i] <= 'z':
                    right[i] = new_Vn_dict[right[i]]
            segment.right = ''.join(right)
        # 添加新分配的产生式
        for key in new_Vn_dict.keys():
            new_g = new_Vn_dict[key] + '-' + key
            sen_list.append(sentence(new_g))
