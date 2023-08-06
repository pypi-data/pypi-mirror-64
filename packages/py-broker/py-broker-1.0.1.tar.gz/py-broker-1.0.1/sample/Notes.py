import requests
import json
import getpass
import pickle

from ApiBase import ApiBase
from Url import Url

class Quote:
    def __init__(self, obj):
        self.price = float(obj['last_trade_price'])
        self.bid_price = float(obj['bid_price'])
        self.bid_size = obj['bid_size']
        self.ask_price = float(obj['ask_price'])
        self.ask_size = obj['ask_size']
        
    def __str__(self):
        return "{ " + "price: " + str(self.price) + ", bid_price: " + str(self.bid_price) + ", bid_size: " \
            + str(self.bid_size) + ", ask_price: " + str(self.ask_price) + ", ask_size: " + str(self.ask_size) + " }"

class Configuration:
    def __init__(self):
        self.username = None
        self.password = None
        self.device_id = None
    
class Client(ApiBase):
    DEBUG = False
    INSECURE = False
    VERSION = "1.0"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Robinhood-API-Version': '1.275.0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'TE': 'Trailers'
        }
        self.client_id = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"
        self.refresh_token = None
        self.account = None
        self.logged_in = False
        self.instruments = {}
        self.stock_ids = {}
        self.symbols = {}
        self.pending_orders = []
    
    # action get login page
    # return nothing
    def get_device_token(self):
        resp = self.session.get(Url.login_page())
    
    # action SMS confirm login, then save login info
    # return nothing
    def sms_confirm(self, username, password):
        resp = self.session.post(Url.login(), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        resp = self.session.post(Url.challenge(c_id), data=json.dumps(data_resp), headers={'Content-Type': 'application/json'})
        resp = self.session.post(Url.login(), data=json.dumps(data), headers={'Content-Type': 'application/json', 'X-ROBINHOOD-CHALLENGE-RESPONSE-ID': c_id})
    
    # action call login_page, call sms_confirm
    def login(self, username, password):
        self.get_device_token()
        self.sms_confirm(username, password)
        
    # 
    # return nothing
    def insecure_login(self):
        self.prompt_login()

        resp = self.session.post(Url.login(), data=json.dumps(data), headers={'Content-Type': 'application/json'})

        self.logged_in = True
        # make account request to get current info
        self.account = self.account_info()['results'][0]

    '''
    account_info: requires to be logged in
    return: json object of /accounts/ request
    '''
    def account_info(self):
        if not self.logged_in:
            return None
        resp = self.session.get(Url.accounts())
        if Client.DEBUG:
            Client.log_response(resp)
        return json.loads(resp.text)

    '''
    logout: requires to be logged in, requests token to be removed
    TODO: which token is used???
    '''
    def logout(self):
        if not self.logged_in:
            return
        data = {
            "client_id":self.client_id,
            "token":self.refresh_token
        }
        resp = self.session.post(Url.logout(), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        if Client.DEBUG:
            Client.log_response(resp)
        self.logged_in = False

    '''
    limit_buy: buy a stock at a limit price (usually lower than current price)
    symbol: "ABC"
    price: "10.01"
    quantity: "10"
    extended: True
    cancel: "gtc"
    '''
    def limit_buy(self, symbol, price, quantity, extended=False, cancel=None):
        if not self.logged_in:
            self.prompt_login()
        # This also will update stock_ids
        symbol = symbol.upper()
        instrument = self.get_instrument(symbol)
        if cancel is None:
            cancel = "gfd"
        data = {
            "time_in_force":cancel,
            "price":price,
            "quantity":quantity,
            "side":"buy",
            "trigger":"immediate",
            "type":"limit",
            "account":self.account['url'],
            "instrument":instrument,
            "symbol":symbol,
            # "ref_id":"",
            "extended_hours":extended
        }
        if Client.DEBUG:
            print(data)
        
        resp = self.session.post(Url.order(), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.pending_orders.append(json.loads(resp.text))
        if Client.DEBUG:
            Client.log_response(resp)
    
    def buy(self, symbol, quantity, extended=False, cancel=None):
        if not self.logged_in:
            self.prompt_login()
        # This also updates stock_ids
        symbol = symbol.upper()
        instrument = self.get_instrument(symbol)
        if cancel is None:
            cancel = "gfd"
        price = float(self.get_quote(symbol).price)
        data = {
            "time_in_force":cancel,
            "price":"{0:.2f}".format(price),
            "quantity":quantity,
            "side":"buy",
            "trigger":"immediate",
            "type":"market",
            "account":self.account['url'],
            "instrument":instrument,
            "symbol":symbol,
            # "ref_id":"",
            "extended_hours":extended
        }
        if Client.DEBUG:
            print(data)
        
        resp = self.session.post(Url.order(), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.pending_orders.append(json.loads(resp.text))
        if Client.DEBUG:
            Client.log_response(resp)
    
    def limit_sell(self, symbol, price, quantity, extended=False, cancel=None):
        if not self.logged_in:
            self.prompt_login()
        # This also will update stock_ids
        symbol = symbol.upper()
        instrument = self.get_instrument(symbol)
        if cancel is None:
            cancel = "gfd"
        data = {
            "time_in_force":cancel,
            "price":price,
            "quantity":quantity,
            "side":"sell",
            "trigger":"immediate",
            "type":"limit",
            "account":self.account['url'],
            "instrument":instrument,
            "symbol":symbol,
            # "ref_id":"",
            "extended_hours":extended
        }
        if Client.DEBUG:
            print(data)
        
        resp = self.session.post(Url.order(), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.pending_orders.append(json.loads(resp.text))
        if Client.DEBUG:
            Client.log_response(resp)
    
    def sell(self, symbol, quantity, extended=False, cancel=None):
        if not self.logged_in:
            self.prompt_login()
        # This also updates stock_ids
        symbol = symbol.upper()
        instrument = self.get_instrument(symbol)
        if cancel is None:
            cancel = "gfd"
        price = float(self.get_quote(symbol).price)
        
        data = {
            "time_in_force":cancel,
            "price":"{0:.2f}".format(price),
            "quantity":quantity,
            "side":"sell",
            "trigger":"immediate",
            "type":"market",
            "account":self.account['url'],
            "instrument":instrument,
            "symbol":symbol,
            # "ref_id":"",
            "extended_hours":extended
        }
        if Client.DEBUG:
            print(data)
        
        resp = self.session.post(Url.order(), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.pending_orders.append(json.loads(resp.text))
        if Client.DEBUG:
            Client.log_response(resp)
    
    def get_instrument(self, symbol):
        if symbol in self.instruments.keys():
            return self.instruments[symbol]
        else:
            resp = self.session.get(Url.instruments(symbol=symbol))
            if Client.DEBUG:
                Client.log_response(resp)
            obj = json.loads(resp.text)
            url = obj['results'][0]['url']
            self.instruments[symbol] = url
            self.stock_ids[symbol] = obj['results'][0]['id']
            self.symbols[obj['results'][0]['id']] = symbol
            return url
    
    '''
    get_quote: returns quote
    symbol: Tradable stock symbol name
    {
      "ask_price": "48.190000",
      "ask_size": 2300,
      "bid_price": "48.180000",
      "bid_size": 2900,
      "last_trade_price": "48.309300",
      "last_extended_hours_trade_price": null,
      "previous_close": "46.850000",
      "adjusted_previous_close": "46.850000",
      "previous_close_date": "2019-06-25",
      "symbol": "INTC",
      "trading_halted": false,
      "has_traded": true,
      "last_trade_price_source": "nls",
      "updated_at": "2019-06-26T17:52:07Z",
      "instrument": "https:\/\/api.robinhood.com\/instruments\/ad059c69-0c1c-4c6b-8322-f53f1bbd69d4\/"
    }
    '''
    def get_quote(self, symbol):
        symbol = symbol.upper()
        self.get_instrument(symbol)
        # stock_ids is updated
        s_id = self.stock_ids[symbol]
        resp = self.session.get(Url.quote(s_id))
        if Client.DEBUG:
            Client.log_response(resp)
        return Quote(json.loads(resp.text))
    
    '''
    'bids' {
        [{'side': 'bid', 'price': {'amount': '198.000000', 'currency_code': 'USD'}, 'quantity': 500}]
    },
    'asks' {
        [{'side': 'ask', 'price': {'amount': '198.010000', 'currency_code': 'USD'}, 'quantity': 500}]
    }
    '''
    def get_book(self, symbol):
        if not self.logged_in:
            return None
        symbol = symbol.upper()
        self.get_instrument(symbol)
        resp = self.session.get(Url.book(self.stock_ids[symbol]))
        if Client.DEBUG:
            Client.log_response(resp)
        return json.loads(resp.text)
    
    '''
    {
      "shares_held_for_stock_grants": "0.0000",
      "account": "https:\/\/api.robinhood.com\/accounts\/5RX37639\/",
      "pending_average_buy_price": "160.7200",
      "shares_held_for_options_events": "0.0000",
      "intraday_average_buy_price": "0.0000",
      "url": "https:\/\/api.robinhood.com\/positions\/5RX37639\/9c53326c-d07e-4b82-82d2-b108ec5d9530\/",
      "shares_held_for_options_collateral": "0.0000",
      "created_at": "2018-04-03T17:15:10.913191Z",
      "updated_at": "2018-04-03T17:18:47.026106Z",
      "shares_held_for_buys": "0.0000",
      "average_buy_price": "160.7200",
      "instrument": "https:\/\/api.robinhood.com\/instruments\/9c53326c-d07e-4b82-82d2-b108ec5d9530\/",
      "intraday_quantity": "0.0000",
      "shares_held_for_sells": "0.0000",
      "shares_pending_from_options_events": "0.0000",
      "quantity": "1.0000"
    }
    '''
    def get_positions(self):
        if not self.logged_in:
            return None
        resp = self.session.get(Url.positions())
        return json.loads(resp.text)['results']
    
    def get_symbol_from_instrument(self, instrument):
        # 9c53326c-d07e-4b82-82d2-b108ec5d9530
        length = len(instrument)
        START_INDEX = 37
        END_INDEX = 1
        string = instrument[length - START_INDEX:length - END_INDEX]
        if string in self.symbols.keys():
            return self.symbols[string]
        else:
            resp = self.session.get(instrument)
            if Client.DEBUG:
                Client.log_response(resp)
            obj = json.loads(resp.text)
            self.symbols[string] = obj['symbol']
            self.instruments[obj['symbol']] = instrument
            self.stock_ids[obj['symbol']] = string
            return obj['symbol']
    
    def cancel_order(self, order_pos):
        if order_pos >= len(self.pending_orders):
            return
        
        resp = self.session.post(self.pending_orders[order_pos]['cancel'])
        if Client.DEBUG:
            Client.log_response(resp)
        del self.pending_orders[order_pos]
    
    def log_response(resp):
        print("--------START--------")
        print(resp.status_code)
        print(resp.reason)
        print(resp.headers)
        print(resp.text)
        print("---------END---------")