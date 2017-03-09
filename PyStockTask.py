import multiprocessing
import default_handler
import time

tasks = []
task_results = dict()
task_come_evt = multiprocessing.Event()
my_logger = default_handler.my_logger
print("task_result:%d" % id(task_results))


class Task:
    id = 0

    def __init__(self, task_type="sell", stock="", price="", amount=""):
        """

        :param task_type:
        :param stock:
        :param price:
        :param amount:
        """
        self.done = multiprocessing.Event()
        self.type = task_type
        self.stock = stock
        self.price = price
        self.amount = amount
        self.__id = Task.id
        Task.id += 1
        task_come_evt.set()
        my_logger.debug("创建任务:%s" % self.to_str())

    def get_id(self):
        return self.__id

    def to_str(self):
        return str("%s %s %s %s id:%d" % (self.type, self.stock, self.price, self.amount, self.__id))


class StockTask(Task):
    def __init__(self, op_type="sell", stock="", price="", amount=""):
        super().__init__(op_type, stock, price, amount)


# 持仓 证券代码\t证券名称\t股票余额\t可用余额\t冻结数量\t参考盈亏\t参考成本价\t参考盈亏比例(%)\t市价\t市值\t买入成本\t市场代码\t交易市场\t股东帐户\t实际数量
# 打新 '证券代码\t证券名称\t备注\t委托数量\t成交数量\t委托价格\t成交均价\t操作\t委托时间\t委托日期\t合同编号\t交易市场\t股东帐户\t详细内容\
def analyze_position(position):
    lines = str(position).split("\r\n")
    print(lines)
    ret = dict()
    if len(lines) > 1:
        heads = lines[0].split("\t")
        for line in lines[1:]:
            val = dict()
            for (i, j) in zip(heads, line.split("\t")):
                val[i] = j
            ret[line.split("\t")[0]] = val
    print(ret)
    return ret


def sell_bonus(position, ratio=1.05, amount_ratio=1.0):
    hold = analyze_position(position)
    amount_ratio = 1 if amount_ratio > 1 else amount_ratio
    for (k, v) in dict(hold).items():
        sell_price = float(dict(v).get("买入成本")) * ratio
        sell_amount = int(int(dict(v).get("可用余额")) * amount_ratio)
        if sell_amount > 0:
            tasks.append(Task("sell", k, str("%.2f" % sell_price), str(sell_amount)))


def tasks_entry():
    print("entry sub process")
    pos = Task("get_hold")
    tasks.append(pos)
    tasks.append(Task("get_entrust"))
    print(time.time())
    print(task_results)
    pos.done.wait(10000)
    print(task_results)
    sell_bonus(task_results.get(pos.get_id()))
    # analyze_position(task_results.get(pos.get_id()))


if __name__ == "__main__":
    pass
