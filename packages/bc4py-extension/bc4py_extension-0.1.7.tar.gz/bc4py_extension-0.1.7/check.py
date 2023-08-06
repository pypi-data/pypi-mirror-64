from typing import NamedTuple, List
import itertools
import random
import os
import bc4py_extension


class Unconfirmed(NamedTuple):
    hash: bytes
    depends: List[bytes]
    price: int
    time: int
    deadline: int
    size: int

    def __repr__(self):
        return "<{}..{} dep={} price={} time={} dead={} size={}>".format(
            self.hash[:8].hex(), self.hash[24:].hex(), len(self.depends), self.price, self.time, self.deadline, self.size)


def test_push_price_time(num):
    ub = bc4py_extension.MemoryPool()
    txs = dict()
    for i in range(num):
        tx = Unconfirmed(
            hash=os.urandom(32),
            depends=[],
            price=random.randint(0, 10),
            time=random.randint(0, 100),
            deadline=i,
            size=0
        )
        ub.push(tx, *tuple(tx))
        txs[tx.hash] = tx

    correct = sorted(txs.values(), key=lambda tx: (-1*tx.price, tx.time))
    library = ub.list_size_limit(800)

    for tx0, tx1 in zip(correct, library):
        assert tx0 is tx1


def test_push_time_dependent(num):
    ub = bc4py_extension.MemoryPool()
    txs = dict()
    for i in range(num):
        depends = random.choices(tuple(txs.keys()), k=random.randint(0, min(len(txs), 10)))
        tx = Unconfirmed(
            hash=i.to_bytes(32, 'big'),
            depends=depends,
            price=0,
            time=i + random.randint(0, 10),
            deadline=0,
            size=0
        )
        ub.push(tx, *tuple(tx))
        txs[tx.hash] = tx

    for tx in ub.list_size_limit(1000):
        tx: Unconfirmed
        print("tx:", tx)
        for txhash in tx.depends:
            print("   depends:", txs.get(txhash))
            assert ub.position(txhash) < ub.position(tx.hash)


def test_push_revert_dependent(num, remove_index):
    ub = bc4py_extension.MemoryPool()
    txs = dict()
    for i in range(num):
        if random.randint(0, 4):
            depends = []
        else:
            depends = random.choices(tuple(txs.keys()), k=random.randint(0, min(len(txs), 4)))
        tx = Unconfirmed(
            hash=i.to_bytes(32, 'big'),
            depends=depends,
            price=random.randint(0, 10),
            time=i + random.randint(0, 10),
            deadline=0,
            size=0
        )
        ub.push(tx, *tuple(tx))
        txs[tx.hash] = tx

    stage0 = ub.list_all_obj(False)
    stage0_copy = ub.list_all_obj(False)
    remove_hash = remove_index.to_bytes(32, 'big')
    ub.remove(remove_hash)
    print("removed")
    ub.push(txs[remove_hash], *tuple(txs[remove_hash]))
    print("pushed")
    stage2 = ub.list_all_obj(False)

    print("show")
    for tx0, tx2 in zip(stage0, stage2):
        assert tx0 == tx2
        print(tx0, tx2)

    print("check")
    for tx in stage0_copy:
        tx: Unconfirmed
        print("tx:", tx)
        for txhash in tx.depends:
            print("   depends:", txs.get(txhash))
            assert ub.position(txhash) < ub.position(tx.hash)


def test_remove_dependent(num, remove_index):
    ub = bc4py_extension.MemoryPool()
    txs = dict()
    for i in range(num):
        if random.randint(0, 1):
            depends = []
        else:
            depends = random.choices(tuple(txs.keys()), k=random.randint(0, min(len(txs), 3)))
        tx = Unconfirmed(
            hash=i.to_bytes(32, 'big'),
            depends=depends,
            price=random.randint(0, 10),
            time=i + random.randint(0, 10),
            deadline=0,
            size=0
        )
        ub.push(tx, *tuple(tx))
        txs[tx.hash] = tx

    stage0 = ub.list_all_obj(False)
    stage0_copy = ub.list_all_obj(False)
    remove_hash = remove_index.to_bytes(32, 'big')
    print("remove", txs[remove_hash])
    count = ub.remove_with_depends(remove_hash)
    print("removed", count)
    stage2 = ub.list_all_obj(False)

    print("show")
    for tx0, tx2 in itertools.zip_longest(stage0, stage2):
        print(tx0, tx2)

    print("for check", stage0_copy)
    for tx in stage0_copy:
        tx: Unconfirmed
        print("tx:", tx)
        for txhash in tx.depends:
            print("   depends:", txs.get(txhash))
    ub.clear_all()


if __name__ == '__main__':
    test_push_price_time(1000)
    test_push_time_dependent(10)
    test_push_revert_dependent(50, 8)
    test_remove_dependent(1000, 0)
