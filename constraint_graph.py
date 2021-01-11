import networkx as nx
import ast
from typing import Optional, Tuple, Any
from typy import get_type_candidate

class ConstraintGraph:
    def __init__(self, tree=None):
        self.g = nx.DiGraph()
        if tree:
            self.dispatch(tree)

    def dispatch(self, tree):
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return None
        meth = getattr(self, '_' + tree.__class__.__name__)
        return meth(tree)

    def remove_node_and_connect(self, label):
        for e1 in self.g.in_edges(label):
            for e2 in self.g.out_edges(label):
                self.g.add_edge(e1[0], e2[1])
        self.g.remove_node(label)


    def get_types(self, label):
        types = []
        for n in nx.ancestors(self.g, label):
            if n.startswith('Constant_'):
                types.extend(get_type_candidate({}, self.g.nodes[n]['value']))
            elif n.startswith('List_'):
                types.extend(get_type_candidate({}, self.g.nodes[n]['value']))
        return types


    def _Module(self, tree):
        for stmt in tree.body:
            self.dispatch(stmt)

    def _Assign(self, t):
        u = self.dispatch(t.value)
        self.g.add_node(u[0], value=u[1])
        for target in t.targets:
            v = self.dispatch(target)
            #if self.g.has_node(v[0]):
            #    self.remove_node_and_connect(v[0])
            self.g.add_node(v[0], value=v[1])
            self.g.add_edge(u[0], v[0])

    def _FunctionDef(self, t):
        self.dispatch(t.body)

    def _If(self, t):
        self.dispatch(t.body)
        while (t.orelse and len(t.orelse) == 1 and isinstance(t.orelse[0], ast.If)):
            t = t.orelse[0]
            self.dispatch(t.body)
        if t.orelse:
            self.dispatch(t.orelse)

    def _Name(self, t: ast.Name) -> Tuple[str, ast.Name]:
        label = t.__class__.__name__ + '_' + t.id
        return label, t

    def _Constant(self, t: ast.Constant) -> Tuple[str, ast.Constant]:
        label = t.__class__.__name__ + '_' + repr(t.value)
        return label, t

    def _List(self, t: ast.List) -> Tuple[str, ast.List]:
        label = t.__class__.__name__ + '_' + repr(t)
        return label, t

    def _Return(self, t: ast.Return):
        pass
