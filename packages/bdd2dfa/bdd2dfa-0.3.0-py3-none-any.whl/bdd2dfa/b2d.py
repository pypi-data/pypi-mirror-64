from typing import TypeVar

import attr

from dfa import DFA


BDD = TypeVar('BDD')


@attr.s(frozen=True, eq=False, auto_attribs=True, repr=False)
class BNode:
    node: BDD
    parity: bool = False

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    @property
    def ref(self) -> int:
        val = self.node.node
        return val if self.parity else -val

    def __str__(self):
        return str(self.ref)

    def __hash__(self):
        return hash(str(self))

    @property
    def is_leaf(self):
        return self.node in (self.node.bdd.true, self.node.bdd.false)

    def label(self):
        if not self.is_leaf:
            return None

        return (self.node == self.node.bdd.true) ^ self.parity

    def transition(self, val):
        if self.is_leaf:
            return self

        parity = self.parity ^ self.node.negated
        node = self.node.high if val else self.node.low
        return attr.evolve(self, node=node, parity=parity)


@attr.s(frozen=True, eq=False, auto_attribs=True, repr=False)
class QNode(BNode):
    time: int = 0

    def __str__(self):
        return f"(ref={self.ref}, time={self.time})"

    def transition(self, val):
        time = max(0, self.time - 1)
        node = super().transition(val)
        return attr.evolve(node, time=time)

    def label(self):
        return None if self.time > 0 else super().label()


def to_dfa(bdd, lazy=False, qdd=True) -> DFA:
    if not qdd:
        Node = BNode
        start = BNode(node=bdd, parity=bdd.negated)
    else:
        Node = QNode
        horizon = len(bdd.manager.vars)
        start = QNode(time=horizon, node=bdd, parity=bdd.negated)

    dfa = DFA(
        start=start, inputs={True, False}, outputs={True, False, None},
        label=Node.label, transition=Node.transition,
    )

    if not lazy:
        dfa.states()  # Traverses and caches all states.

    return dfa
