# 修改为新的终结符
def add1_to_str(string):
    string = chr(ord(string) + 1)
    return string


class sentence:
    def __init__(self, segment):
        self.left, self.right = segment.split('-')

    def get_left(self):
        return str(self.left)

    def get_right(self):
        return str(self.right)

    def info(self):
        print("left: ", self.left, " right: ", self.right)


class Grammar:
    def __init__(self, gra_list):
        self.gra_list = gra_list
        self.sen_list = []
        self.give_index = 1
        self.Vt = []  # 终结符
        self.Vn = []  # 非终结符
        self.start_left = 'S'  # 一般都是这个
        self.new_Vn = 'S'

    def print_gra(self):
        for g in self.gra_list:
            print(g)

    def print_sen(self):
        for s in self.sen_list:
            s.info()

    def get_ε_list(self):
        return []

    def get_new_Vn(self):
        new_Vn = add1_to_str(self.new_Vn)
        self.new_Vn = new_Vn
        self.Vn.append(new_Vn)
        return new_Vn

    def to_sen_list(self):
        '''
            1、化解代'|'的产生式
            2、获得终结符和非终结符（后面有用
        '''
        for g in self.gra_list:
            left, right = g.split('-')
            right_list = right.split('|')
            # 有'|'的话就分割并且加入到后面再处理
            if len(right_list) > 1:
                for r in right_list:
                    new_g = left + '-' + r
                    self.gra_list.append(new_g)
            else:
                segment = sentence(g)
                # 获得非终结符
                if segment.get_left() not in self.Vn:
                    self.Vn.append(segment.get_left())
                # 获得终结符
                for i in segment.get_right():
                    if i not in self.Vt:
                        if i >= 'A' and i <= 'Z':
                            continue
                        self.Vt.append(i)
                self.sen_list.append(segment)

    def reduce_indirect_left_recursion(self):
        '''
            1、 编号
            2、 用排在它前面的非终结符号代入
            3、 去除重复、多余生产式
        '''
        sen_list = self.sen_list
        index_segment = {}
        del_segment = []
        index = 26
        # 编号
        for segment in sen_list:
            if segment.get_left() not in index_segment:
                index_segment[str(segment.get_left())] = index
                index = index - 1
        print(index_segment)
        # 开始代入工作
        for segment in sen_list:
            # segment.info()
            segment_right = str(segment.get_right()[0])
            # 找到在前边的就代入
            if 'A' <= segment_right and segment_right <= "Z" and index_segment[
                    segment_right] < index_segment[segment.get_left()]:
                for s in sen_list:
                    if segment_right == s.get_left():
                        new_g = segment.get_left() + '-' + s.get_right(
                        ) + segment.get_right()[1:]
                        sen_list.append(sentence(new_g))
                del_segment.append(segment)
        # 去除旧的生产式
        for d in del_segment:
            if d in sen_list:
                sen_list.remove(d)
        self.sen_list = sen_list

    def reduce_direct_left_recursion(self):
        '''
            1、找到直接左递归的式子
            2、变换生产式，用非递归的式子代替直接左递归的式子
            3、整理式子，删除旧生产式
        '''
        sen_list = self.sen_list
        is_direct_seg = []
        not_direct_seg = []
        del_segment = []
        flag = True
        for segment in sen_list:
            # 找到直接左递归的式子
            if segment.get_left() == segment.get_right()[0]:
                is_direct_seg.append(segment)
                del_segment.append(segment)
                # 根据上边直接左递归式子的左符号，找到 要消除左递归 用到的产生式
                for s in sen_list:
                    if s.get_left() != s.get_right()[0] and s.get_left(
                    ) == segment.get_left():
                        # 生产式相同就跳过
                        if (segment.get_left() is s.get_left()
                                and segment.get_right() is s.get_right()):
                            continue
                        not_direct_seg.append(s)
                        del_segment.append(s)
        # 去除旧的生产式
        for d in del_segment:
            if d in sen_list:
                sen_list.remove(d)
        # 加上新的消除左递归后的产生式
        # 先找到要更新的非终结符：
        update_Vn = {}
        for seg in not_direct_seg:
            if seg.get_left() not in update_Vn:
                update_Vn[seg.get_left] = self.get_new_Vn(seg.get_left)
        # 更新此非终符
        for seg in not_direct_seg:
            new_g = seg.get_left() + '-' + seg.get_right() + add1_to_str(
                seg.get_left())
            sen_list.append(sentence(new_g))
        for seg in is_direct_seg:
            new_g = add1_to_str(
                seg.get_left()) + '-' + seg.get_right()[1:] + add1_to_str(
                    seg.get_left())
            sen_list.append(sentence(new_g))
        # 根据情况 (flag) 加上 'ε'
        add_ε_list = []
        for seg in is_direct_seg:
            if seg.get_left() not in add_ε_list:
                add_ε_list.append(seg.get_left())
        for s in add_ε_list:
            if flag is True:
                new_g = add1_to_str(s) + '-' + 'ε'
                sen_list.append(sentence(new_g))
        self.sen_list = sen_list

    def reduce_left_recursion(self):
        # 消除间接左递归
        self.reduce_indirect_left_recursion()
        # 消除直接左递归
        self.reduce_direct_left_recursion()

    def reduce_null_production(self):
        # 先找到含有空产生式的生产式左端字符
        sen_list = self.sen_list
        ε_production_list = []
        del_segment = []
        for segment in sen_list:
            # print(segment.get_right())
            if segment.get_right() == 'ε' and segment.get_left(
            ) not in ε_production_list:
                ε_production_list.append(segment.get_left())
        # 根据 此空产生式的左端字符 找到 此产生式的右端产生式
        ε_production_right_list = {}
        for left in ε_production_list:
            lst = []
            for segment in sen_list:
                if segment.get_left() == left:
                    lst.append(segment.get_right())
            ε_production_right_list[left] = lst
        # print(ε_production_right_list)
        for left in ε_production_list:
            for segment in sen_list:
                # 消除此空产生式
                if left == segment.get_left() and 'ε' == segment.get_right():
                    del_segment.append(segment)
                if left in segment.get_right():
                    # 加上空产生式的式子
                    split_right = segment.get_right().split(left)
                    new_g = segment.get_left() + '-' + "".join(split_right)
                    sen_list.append(sentence(new_g))
                    # 去除旧的生产式
            for d in del_segment:
                if d in sen_list:
                    sen_list.remove(d)

    def reduce_useless_production(self):
        del_segment = []
        start_left = self.start_left
        sen_list = self.sen_list
        queue = []
        queue.append(start_left)
        from_start_left_collection = []
        from_start_left_collection.append(start_left)
        while len(queue) != 0:
            new_left = queue[0]
            for segment in sen_list:
                if segment.get_left() == new_left:
                    for right in segment.get_right():
                        if 'A' <= right and right <= 'Z' \
                        and right not in from_start_left_collection:
                            queue.append(right)
                            from_start_left_collection.append(right)
            queue = queue[1:]
        for segment in sen_list:
            if segment.get_left() not in from_start_left_collection:
                del_segment.append(segment)
