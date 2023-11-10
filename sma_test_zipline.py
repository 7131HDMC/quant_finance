%%zipline --start 2016-1-1 --end 2017-12-31 --capital-base 10000.0 -o simple_moving_average.pkl

from zipline.api import record, symbol, order_target
from zipline.finance import commission

MA_PERIODS = 20
SELECTED_STOCK = 'IBM'
N_STOCKS_TO_BUY = 20

def initialize(context):
    context.time = 0
    context.asset = symbol(SELECTED_STOCK)
    context.set_commission(commission.PerShare(cost=0.0, min_trade_cost=0))
    context.has_position = False

def handle_data(context, data):
    context.time += 1
    if context.time < MA_PERIODS:
        return

    price_history = data.history(context.asset, fields="price", bar_count=MA_PERIODS, frequency="1d")
    ma = price_history.mean()
    
    # cross up
    if (price_history[-2] < ma) & (price_history[-1] > ma) & (not context.has_position):
        order_target(context.asset, N_STOCKS_TO_BUY)
        context.has_position = True
    # cross down
    elif (price_history[-2] > ma) & (price_history[-1] < ma) & (context.has_position):
        order_target(context.asset, 0)
        context.has_position = False

    record(price=data.current(context.asset, 'price'),
           moving_average=ma)