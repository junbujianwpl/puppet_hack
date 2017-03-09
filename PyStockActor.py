from puppet import puppetrader_v35
import puppet.puppetrader_v35
import ctypes
import PyStockTask
import default_handler

op = ctypes.windll.user32
my_logger = default_handler.my_logger
task_results = PyStockTask.task_results


class StockActor:
    def __init__(self, txt="网上股票交易系统5.0"):
        self.title = txt
        self.handle = op.FindWindowW(0, txt)
        print(type(self.handle))
        self.actor = puppetrader_v35.unity(self.handle)
        self.deal = {}

    def act_task(self, task):
        self.deal = {
            "sell": [self.actor.sell, (task.stock, task.price, task.amount)],
            "buy": [self.actor.buy, (task.stock, task.price, task.amount)],
            "cancel_all": [self.actor.cancel_all, tuple()],
            "cancel_buy": [self.actor.cancel_buy, tuple()],
            "cancel_sell": [self.actor.cancel_sell, tuple()],
            "balance": [self.actor.balance, tuple()],
            "get_hold": [self.actor.get_data, ('W',)],
            "get_deal": [self.actor.get_data, ('E',)],
            "get_entrust": [self.actor.get_data, ('R',)],
            "ipo": [self.actor.ipo, tuple()],
        }
        my_logger.debug(task.to_str())
        print("do task %s" % (task.to_str()))
        my_logger.debug(str("do task %s" % (task.to_str())))
        if self.deal.__contains__(task.type):
            ret = self.deal[task.type][0](*self.deal[task.type][1])
            print("do task ret:%s" % ret)
            my_logger.debug(str("do task ret:%s" % ret))
            if ret is not None and ret != "":
                task_results[task.get_id()] = ret
                task.done.set()
                print(task_results)
                print(id(task_results))
                return ret
            task.done.set()
