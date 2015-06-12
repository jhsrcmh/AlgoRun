#encoding=utf-8
'''

  Wolf's MIS

'''
import codecs as cds
try :
    import cPickle as pickle
except ImportError:
    import pickle
class Node(object):
    """
    后缀树节点
    """
    def __init__(self):
        self.suffix_node = -1   

    def __repr__(self):
        return "Node(suffix link: %d)"%self.suffix_node

class Edge(object):
    """
    后缀树边
    
    first_char_index
        始节点
    last_char_index
        末节点
    source_node_index
	出发源节点的节点索引
    
    dest_node_index
	目标节点的索引
    """
    def __init__(self, first_char_index, last_char_index, source_node_index, dest_node_index):
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        self.source_node_index = source_node_index
        self.dest_node_index = dest_node_index
        
    @property
    def length(self):
        return self.last_char_index - self.first_char_index

    def __repr__(self):
        return 'Edge(%d, %d, %d, %d)'% (self.source_node_index, self.dest_node_index 
                                        ,self.first_char_index, self.last_char_index )


class Suffix(object):
    """
    依次返回子串的后缀
    """
    def __init__(self, source_node_index, first_char_index, last_char_index):
        self.source_node_index = source_node_index
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        
    @property
    def length(self):
        return self.last_char_index - self.first_char_index
                
    def explicit(self):
        return self.first_char_index > self.last_char_index
    
    def implicit(self):
        return self.last_char_index >= self.first_char_index

        
class SuffixTree(object):
    def __init__(self, string, case_insensitive=False):
        self.string = string
        self.case_insensitive = case_insensitive
        self.N = len(string) - 1
        self.nodes = [Node()]
        self.edges = {}
        self.active = Suffix(0, 0, -1)
        if self.case_insensitive:
            self.string = self.string.lower()
        for i in range(len(string)):
            self._add_prefix(i)
    
    def __repr__(self):
        curr_index = self.N
        s = u"\t开始 \t结束 \t后缀 \t开始 \t结束 \t 串 \n"
        values = self.edges.values()
        values.sort(key=lambda x: x.source_node_index)
        for edge in values:
            if edge.source_node_index == -1:
                continue
            s += "\t%s    \t%s     \t%s     \t%s   \t%s   \t "%(edge.source_node_index
                    ,edge.dest_node_index 
                    ,self.nodes[edge.dest_node_index].suffix_node 
                    ,edge.first_char_index
                    ,edge.last_char_index)
                    
            
            top = min(curr_index, edge.last_char_index)
            s += self.string[edge.first_char_index:top+1] + "\n"
        return s
            
    def _add_prefix(self, last_char_index):
        last_parent_node = -1
        while True:
            parent_node = self.active.source_node_index
            if self.active.explicit():
                if (self.active.source_node_index, self.string[last_char_index]) in self.edges:
                    # 前缀存在
                    break
            else:
                e = self.edges[self.active.source_node_index, self.string[self.active.first_char_index]]
                if self.string[e.first_char_index + self.active.length + 1] == self.string[last_char_index]:
                    # 前缀存在
                    break
                parent_node = self._split_edge(e, self.active)
        

            self.nodes.append(Node())
            e = Edge(last_char_index, self.N, parent_node, len(self.nodes) - 1)
            self._insert_edge(e)
            
            if last_parent_node > 0:
                self.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node
            
            if self.active.source_node_index == 0:
                self.active.first_char_index += 1
            else:
                self.active.source_node_index = self.nodes[self.active.source_node_index].suffix_node
            self._canonize_suffix(self.active)
        if last_parent_node > 0:
            self.nodes[last_parent_node].suffix_node = parent_node
        self.active.last_char_index += 1
        self._canonize_suffix(self.active)
        
    def _insert_edge(self, edge):
        self.edges[(edge.source_node_index, self.string[edge.first_char_index])] = edge
        
    def _remove_edge(self, edge):
        self.edges.pop((edge.source_node_index, self.string[edge.first_char_index]))
        
    def _split_edge(self, edge, suffix):
        self.nodes.append(Node())
        e = Edge(edge.first_char_index, edge.first_char_index + suffix.length, suffix.source_node_index, len(self.nodes) - 1)
        self._remove_edge(edge)
        self._insert_edge(e)
        self.nodes[e.dest_node_index].suffix_node = suffix.source_node_index  ### need to add node for each edge
        edge.first_char_index += suffix.length + 1
        edge.source_node_index = e.dest_node_index
        self._insert_edge(edge)
        return e.dest_node_index

    def _canonize_suffix(self, suffix):
        if not suffix.explicit():
            e = self.edges[suffix.source_node_index, self.string[suffix.first_char_index]]
            if e.length <= suffix.length:
                suffix.first_char_index += e.length + 1
                suffix.source_node_index = e.dest_node_index
                self._canonize_suffix(suffix)
 

    # 子串寻找
    def find_substring(self, substring):
        if not substring:
            return -1
        if self.case_insensitive:
            substring = substring.lower()
        curr_node = 0
        i = 0
        while i < len(substring):
            edge = self.edges.get((curr_node, substring[i]))
            if not edge:
                return -1
            ln = min(edge.length + 1, len(substring) - i)
            if substring[i:i + ln] != self.string[edge.first_char_index:edge.first_char_index + ln]:
                return -1
            i += edge.length + 1
            curr_node = edge.dest_node_index
        return edge.first_char_index - len(substring) + ln

    def has_substring(self, substring):
        return self.find_substring(substring) != -1


    def find_substring_by_pattern(self, patterns):
        for pattern in patterns:
            i = 0
            while True:
                if not unvisited(tree).empty() and pattern[i]:
                    current, current_index = unvisited.top()
                    cursor, cursor_index = unvisited.pop()
                    #判定当前元素是否满足模板中的相应元素
                    if not cursor == pattern[i]:
                        #不满足,回溯,进行下一次匹配,每次子串匹配使用KMP算法
                        backbone()
                        continue
                    i = i+1
                    #深度优先遍历
                    if(current.right!=NULL):
                        unvisited.push(current.right);
                    if(current.left!=NULL):
                        unvisited.push(current.left);

                    #跳至子节点
                    current = self.current

                    #循环终止条件
                    if not pattern[i].exist():
                        RelationShip.append(dealed_txt[current_index, cursor_index])
                        break
        
        return RelationShip

    def unvisited(self, tree):
        #need to relize
        return 
if __name__ == "__main__":
   f = cds.open("test.txt", encoding="utf-8")
   st = SuffixTree(f.read())
   print st.find_substring(u"概括性总结")
