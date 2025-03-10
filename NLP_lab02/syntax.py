#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Submit just this file, no zip, no additional files
# -------------------------------------------------

# Students:
#     - CHERGUELAINE Oussama
#     - RAHOU Meriem

"""QUESTIONS/ANSWERS

----------------------------------------------------------
Q1: "If PoS tagging is used with CKY, there will be no ambiguities". True or False? Justify.

A1: False. PoS tagging helps reduce ambiguity, but CKY parsing still faces structural ambiguities in sentence parsing.

----------------------------------------------------------

----------------------------------------------------------
Q2: If PoS tagging is used with CKY, there will be no out-of-vocabulary problem". True or False? Justify.

A2: False. PoS tagging does not eliminate out-of-vocabulary (OOV) issues, as unknown words may still appear and require handling.

----------------------------------------------------------
"""

import re
import random
from typing import Dict, List, Tuple, Set


# ======================================================
#                   Analyse CKY
# ======================================================
from typing import List, Tuple, Dict
from typing import List, Tuple, Dict

class CKY:

    def __init__(self, gram: List[Tuple[str, str, str]], lex: Dict[str, List[str]]):
        self.gram = gram
        self.lex = lex

    # TODO: complete this function
    def parse(self, sent: List[str]) -> List[List[List[Tuple[str, int, int, int]]]]:
        n = len(sent)
        T = [[[] for _ in range(n)] for _ in range(n)]

        for i, word in enumerate(sent):
            tags = self.lex.get(word, [])
            T[i][i].extend((tag, -1, -1, -1) for tag in tags)

            queue = list(T[i][i])
            seen = set(queue)
            while queue:
                B = queue.pop(0)[0]
                for A, B_rule in filter(lambda r: len(r) == 2, self.gram):
                    if B_rule == B:
                        new_entry = (A, -1, next((idx for idx, e in enumerate(T[i][i]) if e[0] == B), -1), -1)
                        if new_entry not in seen:
                            T[i][i].append(new_entry)
                            queue.append(new_entry)
                            seen.add(new_entry)

        def process_cell(i, j):
            for k in range(i, j):
                for A, B, C in filter(lambda r: len(r) == 3, self.gram):
                    left_matches = [entry for entry in T[i][k] if entry[0] == B]
                    right_matches = [entry for entry in T[k+1][j] if entry[0] == C]
                    T[i][j].extend((A, k, T[i][k].index(lb), T[k+1][j].index(rb))
                                   for lb in left_matches for rb in right_matches)

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                process_cell(i, j)

                queue = list(T[i][j])
                seen = set(queue)
                while queue:
                    B = queue.pop(0)[0]
                    for A, B_rule in filter(lambda r: len(r) == 2, self.gram):
                        if B_rule == B:
                            new_entry = (A, -1, next((idx for idx, e in enumerate(T[i][j]) if e[0] == B), -1), -1)
                            if new_entry not in seen:
                                T[i][j].append(new_entry)
                                queue.append(new_entry)
                                seen.add(new_entry)

        return T

    def export_json(self):
        return {k: v for k, v in self.__dict__.items()}

    def import_json(self, data):
        self.__dict__.update(data)



# ======================================================
#                Parsing
# ======================================================

# TODO: complete this function
def pr_eval(ref, sys):
    if ref is None and sys is None:
        return 1.0, 1.0
    elif ref is None or sys is None:
        return 0.0, 0.0
    else:
        ref_arcs, sys_arcs, common_arcs = compute_arc_counts(ref, sys)
        precision = common_arcs / sys_arcs if sys_arcs > 0 else 0.0
        recall = common_arcs / ref_arcs if ref_arcs > 0 else 0.0
        return precision, recall

def compute_arc_counts(ref, sys):
    if ref is None and sys is None:
        return 0, 0, 0
    elif ref is None:
        sys_arcs = 0
        if isinstance(sys, tuple):
            if len(sys) > 1 and isinstance(sys[1], tuple):
                _, s, _ = compute_arc_counts(None, sys[1])
                sys_arcs += 1 + s
            if len(sys) > 2 and isinstance(sys[2], tuple):
                _, s, _ = compute_arc_counts(None, sys[2])
                sys_arcs += 1 + s
        return 0, sys_arcs, 0
    elif sys is None:
        ref_arcs = 0
        if isinstance(ref, tuple):
            if len(ref) > 1 and isinstance(ref[1], tuple):
                r, _, _ = compute_arc_counts(ref[1], None)
                ref_arcs += 1 + r
            if len(ref) > 2 and isinstance(ref[2], tuple):
                r, _, _ = compute_arc_counts(ref[2], None)
                ref_arcs += 1 + r
        return ref_arcs, 0, 0
    else:
        if not isinstance(ref, tuple) or not isinstance(sys, tuple):
            return 0, 0, 0
        root_match = ref[0] == sys[0]
        left_ref = ref[1] if len(ref) > 1 else None
        left_sys = sys[1] if len(sys) > 1 else None
        right_ref = ref[2] if len(ref) > 2 else None
        right_sys = sys[2] if len(sys) > 2 else None
        left_counts = compute_arc_counts(left_ref, left_sys)
        right_counts = compute_arc_counts(right_ref, right_sys)
        ref_arcs = 0
        if isinstance(left_ref, tuple):
            ref_arcs += 1 + left_counts[0]
        if isinstance(right_ref, tuple):
            ref_arcs += 1 + right_counts[0]
        sys_arcs = 0
        if isinstance(left_sys, tuple):
            sys_arcs += 1 + left_counts[1]
        if isinstance(right_sys, tuple):
            sys_arcs += 1 + right_counts[1]
        common_arcs = 0
        if root_match:
            if isinstance(left_ref, tuple) and isinstance(left_sys, tuple) and left_ref[0] == left_sys[0]:
                common_arcs += 1 + left_counts[2]
            if isinstance(right_ref, tuple) and isinstance(right_sys, tuple) and right_ref[0] == right_sys[0]:
                common_arcs += 1 + right_counts[2]
        return ref_arcs, sys_arcs, common_arcs
    
    


def construct(T, sent, i, j, pos):
    A, k, iB, iC = T[i][j][pos]
    if k >= 0:
        left = construct(T, sent, i, k, iB)
        if iC == -1:
            return (A, left)
        right = construct(T, sent, k+1, j, iC)
        return (A, left, right)
    else:
        # lahna lazm nkmlo derivation
        if iB != -1:
            child = construct(T, sent, i, j, iB)
            return (A, child)
        else:
            return (A, sent[i])
        
def parse_tuple(string):
    string = re.sub(r'([^\s(),]+)', "'\\1'", string)
    #print(string)
    try:
        s = eval(string)
        if type(s) == tuple:
            return s
        return
    except:
        return

class Syntax():
    def __init__(self):
        self.eval = []

    def _parse(self, sent):
        r = None
        T = self.model.parse(sent)
        n = len(sent) - 1
        # for i in range(n+1):
        #     for j in range(i, n+1):
        #         print(i+1, j+1, T[i][j])
        for pos in range(len(T[0][n])):
            if T[0][n][pos][0] == 'S':
                # print('bingo')
                r = construct(T, sent, 0, n, pos)
                break
        return r

    def parse(self, sent: str):
        return self._parse(sent.strip().lower().split())

    def load_model(self, url):
        f = open(url, 'r')
        lex = {}
        gram = []
        for l in f: # line-by-line reading
            l = l.strip()
            if len(l) < 3 or l.startswith('#') :
                continue
            info = l.split('	')
            if len(info) == 2:
                if info[1][0].isupper():
                    gram.append((info[0], info[1]))
                else:
                    if not info[1] in lex:
                        lex[info[1]] = []
                    lex[info[1]].append(info[0])
            elif len(info) == 3:
                gram.append((info[0], info[1], info[2]))
        self.model = CKY(gram, lex)
        f.close()


    def load_eval(self, url):
        f = open(url, 'r')
        for l in f: # line-by-line reading
            l = l.strip()
            if len(l) < 5 or l.startswith('#'):
                continue
            info = l.split('	')
            
            self.eval.append((info[0], parse_tuple(info[1])))

    def evaluate(self, n):
        if n == -1:
            S = self.eval
            n = len(S)
        else :
            S = random.sample(self.eval, n)
        P, R = 0.0, 0.0
        for i in range(n):
            test = S[i]
            print('=======================')
            print('sent:', test[0])
            print('ref tree:', test[1])
            tree = self.parse(test[0])
            print('sys tree:', tree)
            P_i, R_i = pr_eval(test[1], tree)
            print('P, R:', P_i, R_i)
            P += P_i
            R += R_i

        P, R = P/n, R/n
        print('---------------------------------')
        print('P, R: ', P, R)



# ======================================================
#        Graph generation (Dot language)
# ======================================================

def generate_node(node, id=0):
    # If the node does not exist
    if node is None:
        return 0, ''
    # If the node is final
    nid = id + 1
    if (len(node) == 2) and (type(node[1]) == str) :
        return nid, 'N' + str(id) + '[label="' + node[0] + "=" + node[1] + '" shape=box];\n'
    # Otherzise,
    # If there are children, print if else
    res = 'N' + str(id) + '[label="' + node[0] + '"];\n'
    nid_l = nid
    nid, code = generate_node(node[1], id=nid_l)
    res += code
    res += 'N' + str(id) + ' ->  N' + str(nid_l) + ';\n'
    if len(node) > 2:
        nid_r = nid
        nid, code = generate_node(node[2], id=nid_r)
        res += code
        res += 'N' + str(id) + ' ->  N' + str(nid_r) + ';\n'
    return nid, res

def generate_graphviz(root, url):
    res = 'digraph Tree {\n'
    id, code = generate_node(root)
    res += code
    res += '}'
    f = open(url, 'w')
    f.write(res)
    f.close()


# ======================================================
#                       TESTES
# ======================================================

# Test in the lecture
def test_cky():
    parser = Syntax()
    parser.load_model('data/gram1.txt')
    sent = 'la petite forme une petite phrase'
    result = "('S', ('NP', ('D', 'la'), ('N', 'petite')), ('VP', ('V', 'forme'), ('NP', ('D', 'une'), ('AP', ('J', 'petite'), ('N', 'phrase')))))"
    tree = parser.parse(sent)
    print('Real Result: ', result)
    print('My Result: ', tree)
    generate_graphviz(tree, 'parse_tree.gv')

# test the pr evaluation
def test_eval_tree():
    t1 = ('A', ('B', 'b'), ('C', ('A', 'a'), ('B', ('A', 'a'), ('C', 'c'))))
    t2 = ('A', ('B', 'b'), ('C', ('B', 'b'), ('D', 'd')))
    t3 = ('A', ('B', 'b'), ('C', ('B', 'b')))
    print('Real: (0., 0.), Found: ', pr_eval(None, t1))
    print('Real: (1., 1.), Found: ', pr_eval(None, None))
    print('Real: (0.5, 0.333), Found: ', pr_eval(t1, t2))
    print('Real: (0.333, 0.5), Found: ', pr_eval(t2, t1))
    print('Real: (1., 0.75), Found: ', pr_eval(t2, t3))
    print('Real: (1., 1.), Found: ', pr_eval(t1, t1))

# evaluate an existing example
def test_evaluate():
    parser = Syntax()
    parser.load_model('data/gram1.txt')
    parser.load_eval('data/test1.txt')
    parser.evaluate(-1)


if __name__ == '__main__':
    test_cky()
    test_eval_tree()
    test_evaluate()
