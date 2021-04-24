# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.precise import Precise


class zb(Exchange):

    def describe(self):
        return self.deep_extend(super(zb, self).describe(), {
            'id': 'zb',
            'name': 'ZB',
            'countries': ['CN'],
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'cancelOrder': True,
                'CORS': False,
                'createMarketOrder': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': True,
                'fetchDepositAddresses': True,
                'fetchDeposits': True,
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchClosedOrders': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchWithdrawals': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '3m': '3min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '6h': '6hour',
                '12h': '12hour',
                '1d': '1day',
                '3d': '3day',
                '1w': '1week',
            },
            'exceptions': {
                'exact': {
                    # '1000': 'Successful operation',
                    '1001': ExchangeError,  # 'General error message',
                    '1002': ExchangeError,  # 'Internal error',
                    '1003': AuthenticationError,  # 'Verification does not pass',
                    '1004': AuthenticationError,  # 'Funding security password lock',
                    '1005': AuthenticationError,  # 'Funds security password is incorrect, please confirm and re-enter.',
                    '1006': AuthenticationError,  # 'Real-name certification pending approval or audit does not pass',
                    '1009': ExchangeNotAvailable,  # 'This interface is under maintenance',
                    '2001': InsufficientFunds,  # 'Insufficient CNY Balance',
                    '2002': InsufficientFunds,  # 'Insufficient BTC Balance',
                    '2003': InsufficientFunds,  # 'Insufficient LTC Balance',
                    '2005': InsufficientFunds,  # 'Insufficient ETH Balance',
                    '2006': InsufficientFunds,  # 'Insufficient ETC Balance',
                    '2007': InsufficientFunds,  # 'Insufficient BTS Balance',
                    '2009': InsufficientFunds,  # 'Account balance is not enough',
                    '3001': OrderNotFound,  # 'Pending orders not found',
                    '3002': InvalidOrder,  # 'Invalid price',
                    '3003': InvalidOrder,  # 'Invalid amount',
                    '3004': AuthenticationError,  # 'User does not exist',
                    '3005': BadRequest,  # 'Invalid parameter',
                    '3006': AuthenticationError,  # 'Invalid IP or inconsistent with the bound IP',
                    '3007': AuthenticationError,  # 'The request time has expired',
                    '3008': OrderNotFound,  # 'Transaction records not found',
                    '3009': InvalidOrder,  # 'The price exceeds the limit',
                    '3011': InvalidOrder,  # 'The entrusted price is abnormal, please modify it and place order again',
                    '4001': ExchangeNotAvailable,  # 'API interface is locked or not enabled',
                    '4002': DDoSProtection,  # 'Request too often',
                },
                'broad': {
                    '提币地址有误，请先添加提币地址。': InvalidAddress,  # {"code":1001,"message":"提币地址有误，请先添加提币地址。"}
                },
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/32859187-cd5214f0-ca5e-11e7-967d-96568e2e2bd1.jpg',
                'api': {
                    'public': 'https://api.zb.today/data',
                    'private': 'https://trade.zb.today/api',
                },
                'www': 'https://www.zb.com',
                'doc': 'https://www.zb.com/i/developer',
                'fees': 'https://www.zb.com/i/rate',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'ticker',
                        'allTicker',
                        'depth',
                        'trades',
                        'kline',
                    ],
                },
                'private': {
                    'get': [
                        # spot API
                        'order',
                        'orderMoreV2',
                        'cancelOrder',
                        'getOrder',
                        'getOrders',
                        'getOrdersNew',
                        'getOrdersIgnoreTradeType',
                        'getUnfinishedOrdersIgnoreTradeType',
                        'getFinishedAndPartialOrders',
                        'getAccountInfo',
                        'getUserAddress',
                        'getPayinAddress',
                        'getWithdrawAddress',
                        'getWithdrawRecord',
                        'getChargeRecord',
                        'getCnyWithdrawRecord',
                        'getCnyChargeRecord',
                        'withdraw',
                        # sub accounts
                        'addSubUser',
                        'getSubUserList',
                        'doTransferFunds',
                        'createSubUserKey',
                        # leverage API
                        'getLeverAssetsInfo',
                        'getLeverBills',
                        'transferInLever',
                        'transferOutLever',
                        'loan',
                        'cancelLoan',
                        'getLoans',
                        'getLoanRecords',
                        'borrow',
                        'autoBorrow',
                        'repay',
                        'doAllRepay',
                        'getRepayments',
                        'getFinanceRecords',
                        'changeInvestMark',
                        'changeLoop',
                        # cross API
                        'getCrossAssets',
                        'getCrossBills',
                        'transferInCross',
                        'transferOutCross',
                        'doCrossLoan',
                        'doCrossRepay',
                        'getCrossRepayRecords',
                    ],
                },
            },
            'fees': {
                'funding': {
                    'withdraw': {
                        'BTC': 0.0001,
                        'BCH': 0.0006,
                        'LTC': 0.005,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        'BTS': 3,
                        'EOS': 1,
                        'QTUM': 0.01,
                        'HSR': 0.001,
                        'XRP': 0.1,
                        'USDT': '0.1%',
                        'QCASH': 5,
                        'DASH': 0.002,
                        'BCD': 0,
                        'UBTC': 0,
                        'SBTC': 0,
                        'INK': 20,
                        'TV': 0.1,
                        'BTH': 0,
                        'BCX': 0,
                        'LBTC': 0,
                        'CHAT': 20,
                        'bitCNY': 20,
                        'HLC': 20,
                        'BTP': 0,
                        'BCW': 0,
                    },
                },
                'trading': {
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
            },
            'commonCurrencies': {
                'ENT': 'ENTCash',
            },
        })

    async def fetch_markets(self, params={}):
        markets = await self.publicGetMarkets(params)
        #
        #     {
        #         "zb_qc":{
        #             "amountScale":2,
        #             "minAmount":0.01,
        #             "minSize":5,
        #             "priceScale":4,
        #         },
        #     }
        #
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId, quoteId = id.split('_')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            amountPrecisionString = self.safe_string(market, 'amountScale')
            pricePrecisionString = self.safe_string(market, 'priceScale')
            amountLimit = self.parse_precision(amountPrecisionString)
            priceLimit = self.parse_precision(pricePrecisionString)
            precision = {
                'amount': int(amountPrecisionString),
                'price': int(pricePrecisionString),
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': self.parse_number(amountLimit),
                        'max': None,
                    },
                    'price': {
                        'min': self.parse_number(priceLimit),
                        'max': None,
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetGetAccountInfo(params)
        # todo: use self somehow
        # permissions = response['result']['base']
        balances = self.safe_value(response['result'], 'coins')
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            #     {       enName: "BTC",
            #               freez: "0.00000000",
            #         unitDecimal:  8,  # always 8
            #              cnName: "BTC",
            #       isCanRecharge:  True,  # TODO: should use self
            #             unitTag: "฿",
            #       isCanWithdraw:  True,  # TODO: should use self
            #           available: "0.00000000",
            #                 key: "btc"         }
            account = self.account()
            currencyId = self.safe_string(balance, 'key')
            code = self.safe_currency_code(currencyId)
            account['free'] = self.safe_string(balance, 'available')
            account['used'] = self.safe_string(balance, 'freez')
            result[code] = account
        return self.parse_balance(result, False)

    def parse_deposit_address(self, depositAddress, currency=None):
        #
        # fetchDepositAddress
        #
        #     {
        #         "key": "0x0af7f36b8f09410f3df62c81e5846da673d4d9a9"
        #     }
        #
        # fetchDepositAddresses
        #
        #     {
        #         "blockChain": "btc",
        #         "isUseMemo": False,
        #         "address": "1LL5ati6pXHZnTGzHSA3rWdqi4mGGXudwM",
        #         "canWithdraw": True,
        #         "canDeposit": True
        #     }
        #     {
        #         "blockChain": "bts",
        #         "isUseMemo": True,
        #         "account": "btstest",
        #         "memo": "123",
        #         "canWithdraw": True,
        #         "canDeposit": True
        #     }
        #
        address = self.safe_string(depositAddress, 'key')
        tag = None
        memo = self.safe_string(depositAddress, 'memo')
        if memo is not None:
            tag = memo
        elif address.find('_') >= 0:
            parts = address.split('_')
            address = parts[0]  # WARNING: MAY BE tag_address INSTEAD OF address_tag FOR SOME CURRENCIESnot !
            tag = parts[1]
        currencyId = self.safe_string(depositAddress, 'blockChain')
        code = self.safe_currency_code(currencyId, currency)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': depositAddress,
        }

    async def fetch_deposit_addresses(self, codes=None, params={}):
        await self.load_markets()
        response = await self.privateGetGetPayinAddress(params)
        #
        #     {
        #         "code": 1000,
        #         "message": {
        #             "des": "success",
        #             "isSuc": True,
        #             "datas": [
        #                 {
        #                     "blockChain": "btc",
        #                     "isUseMemo": False,
        #                     "address": "1LL5ati6pXHZnTGzHSA3rWdqi4mGGXudwM",
        #                     "canWithdraw": True,
        #                     "canDeposit": True
        #                 },
        #                 {
        #                     "blockChain": "bts",
        #                     "isUseMemo": True,
        #                     "account": "btstest",
        #                     "memo": "123",
        #                     "canWithdraw": True,
        #                     "canDeposit": True
        #                 },
        #             ]
        #         }
        #     }
        #
        message = self.safe_value(response, 'message', {})
        datas = self.safe_value(message, 'datas', [])
        return self.parse_deposit_addresses(datas, codes)

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = await self.privateGetGetUserAddress(self.extend(request, params))
        #
        #     {
        #         "code": 1000,
        #         "message": {
        #             "des": "success",
        #             "isSuc": True,
        #             "datas": {
        #                 "key": "0x0af7f36b8f09410f3df62c81e5846da673d4d9a9"
        #             }
        #         }
        #     }
        #
        message = self.safe_value(response, 'message', {})
        datas = self.safe_value(message, 'datas', {})
        return self.parse_deposit_address(datas, currency)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['size'] = limit
        response = await self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response, symbol)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetAllTicker(params)
        result = {}
        anotherMarketsById = {}
        marketIds = list(self.marketsById.keys())
        for i in range(0, len(marketIds)):
            tickerId = marketIds[i].replace('_', '')
            anotherMarketsById[tickerId] = self.marketsById[marketIds[i]]
        ids = list(response.keys())
        for i in range(0, len(ids)):
            market = anotherMarketsById[ids[i]]
            result[market['symbol']] = self.parse_ticker(response[ids[i]], market)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetTicker(self.extend(request, params))
        ticker = response['ticker']
        return self.parse_ticker(ticker, market)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_number(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_number(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None):
        return [
            self.safe_integer(ohlcv, 0),
            self.safe_number(ohlcv, 1),
            self.safe_number(ohlcv, 2),
            self.safe_number(ohlcv, 3),
            self.safe_number(ohlcv, 4),
            self.safe_number(ohlcv, 5),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 1000
        request = {
            'market': market['id'],
            'type': self.timeframes[timeframe],
            'limit': limit,
        }
        if since is not None:
            request['since'] = since
        response = await self.publicGetKline(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        side = self.safe_string(trade, 'trade_type')
        side = 'buy' if (side == 'bid') else 'sell'
        id = self.safe_string(trade, 'tid')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        costString = Precise.string_mul(priceString, amountString)
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(costString)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'order': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise InvalidOrder(self.id + ' allows limit orders only')
        await self.load_markets()
        request = {
            'price': self.price_to_precision(symbol, price),
            'amount': self.amount_to_precision(symbol, amount),
            'tradeType': '1' if (side == 'buy') else '0',
            'currency': self.market_id(symbol),
        }
        response = await self.privateGetOrder(self.extend(request, params))
        return {
            'info': response,
            'id': response['id'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': str(id),
            'currency': self.market_id(symbol),
        }
        return await self.privateGetCancelOrder(self.extend(request, params))

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        await self.load_markets()
        request = {
            'id': str(id),
            'currency': self.market_id(symbol),
        }
        response = await self.privateGetGetOrder(self.extend(request, params))
        #
        #     {
        #         'total_amount': 0.01,
        #         'id': '20180910244276459',
        #         'price': 180.0,
        #         'trade_date': 1536576744960,
        #         'status': 2,
        #         'trade_money': '1.96742',
        #         'trade_amount': 0.01,
        #         'type': 0,
        #         'currency': 'eth_usdt'
        #     }
        #
        return self.parse_order(response, None)

    async def fetch_orders(self, symbol=None, since=None, limit=50, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + 'fetchOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'pageIndex': 1,  # default pageIndex is 1
            'pageSize': limit,  # default pageSize is 50
        }
        method = 'privateGetGetOrdersIgnoreTradeType'
        # tradeType 交易类型1/0[buy/sell]
        if 'tradeType' in params:
            method = 'privateGetGetOrdersNew'
        response = None
        try:
            response = await getattr(self, method)(self.extend(request, params))
        except Exception as e:
            if isinstance(e, OrderNotFound):
                return []
            raise e
        return self.parse_orders(response, market, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + 'fetchClosedOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'pageIndex': 1,  # default pageIndex is 1
            'pageSize': 10,  # default pageSize is 10, doesn't work with other values now
        }
        response = await self.privateGetGetFinishedAndPartialOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=10, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + 'fetchOpenOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'pageIndex': 1,  # default pageIndex is 1
            'pageSize': limit,  # default pageSize is 10
        }
        method = 'privateGetGetUnfinishedOrdersIgnoreTradeType'
        # tradeType 交易类型1/0[buy/sell]
        if 'tradeType' in params:
            method = 'privateGetGetOrdersNew'
        response = None
        try:
            response = await getattr(self, method)(self.extend(request, params))
        except Exception as e:
            if isinstance(e, OrderNotFound):
                return []
            raise e
        return self.parse_orders(response, market, since, limit)

    def parse_order(self, order, market=None):
        #
        #     {
        #         acctType: 0,
        #         currency: 'btc_usdt',
        #         fees: 3.6e-7,
        #         id: '202102282829772463',
        #         price: 45177.5,
        #         status: 2,
        #         total_amount: 0.0002,
        #         trade_amount: 0.0002,
        #         trade_date: 1614515104998,
        #         trade_money: 8.983712,
        #         type: 1,
        #         useZbFee: False
        #     },
        #
        side = self.safe_integer(order, 'type')
        side = 'buy' if (side == 1) else 'sell'
        type = 'limit'  # market order is not availalbe in ZB
        timestamp = self.safe_integer(order, 'trade_date')
        marketId = self.safe_string(order, 'currency')
        symbol = self.safe_symbol(marketId, market, '_')
        price = self.safe_number(order, 'price')
        filled = self.safe_number(order, 'trade_amount')
        amount = self.safe_number(order, 'total_amount')
        cost = self.safe_number(order, 'trade_money')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'id')
        feeCost = self.safe_number(order, 'fees')
        fee = None
        if feeCost is not None:
            feeCurrency = None
            zbFees = self.safe_value(order, 'useZbFee')
            if zbFees is True:
                feeCurrency = 'ZB'
            elif market is not None:
                feeCurrency = market['quote'] if (side == 'sell') else market['base']
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'average': None,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': fee,
            'trades': None,
        })

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'canceled',
            '2': 'closed',
            '3': 'open',  # partial
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction_status(self, status):
        statuses = {
            '0': 'pending',  # submitted, pending confirmation
            '1': 'failed',
            '2': 'ok',
            '3': 'canceled',
            '5': 'ok',  # confirmed
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        # withdraw
        #
        #     {
        #         "code": 1000,
        #         "message": "success",
        #         "id": "withdrawalId"
        #     }
        #
        # fetchWithdrawals
        #
        #     {
        #         "amount": 0.01,
        #         "fees": 0.001,
        #         "id": 2016042556231,
        #         "manageTime": 1461579340000,
        #         "status": 3,
        #         "submitTime": 1461579288000,
        #         "toAddress": "14fxEPirL9fyfw1i9EF439Pq6gQ5xijUmp",
        #     }
        #
        # fetchDeposits
        #
        #     {
        #         "address": "1FKN1DZqCm8HaTujDioRL2Aezdh7Qj7xxx",
        #         "amount": "1.00000000",
        #         "confirmTimes": 1,
        #         "currency": "BTC",
        #         "description": "Successfully Confirm",
        #         "hash": "7ce842de187c379abafadd64a5fe66c5c61c8a21fb04edff9532234a1dae6xxx",
        #         "id": 558,
        #         "itransfer": 1,
        #         "status": 2,
        #         "submit_time": "2016-12-07 18:51:57",
        #     }
        #
        id = self.safe_string(transaction, 'id')
        txid = self.safe_string(transaction, 'hash')
        amount = self.safe_number(transaction, 'amount')
        timestamp = self.parse8601(self.safe_string(transaction, 'submit_time'))
        timestamp = self.safe_integer(transaction, 'submitTime', timestamp)
        address = self.safe_string_2(transaction, 'toAddress', 'address')
        tag = None
        if address is not None:
            parts = address.split('_')
            address = self.safe_string(parts, 0)
            tag = self.safe_string(parts, 1)
        confirmTimes = self.safe_integer(transaction, 'confirmTimes')
        updated = self.safe_integer(transaction, 'manageTime')
        type = None
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        if address is not None:
            type = 'withdrawal' if (confirmTimes is None) else 'deposit'
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        fee = None
        feeCost = self.safe_number(transaction, 'fees')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': code,
            }
        return {
            'info': transaction,
            'id': id,
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'addressFrom': None,
            'address': address,
            'addressTo': address,
            'tagFrom': None,
            'tag': tag,
            'tagTo': tag,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': updated,
            'fee': fee,
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        password = self.safe_string(params, 'safePwd', self.password)
        if password is None:
            raise ArgumentsRequired(self.id + ' withdraw() requires exchange.password or a safePwd parameter')
        fees = self.safe_number(params, 'fees')
        if fees is None:
            raise ArgumentsRequired(self.id + ' withdraw() requires a fees parameter')
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        if tag is not None:
            address += '_' + tag
        request = {
            'amount': self.currency_to_precision(code, amount),
            'currency': currency['id'],
            'fees': self.currency_to_precision(code, fees),
            # 'itransfer': 0,  # agree for an internal transfer, 0 disagree, 1 agree, the default is to disagree
            'method': 'withdraw',
            'receiveAddr': address,
            'safePwd': password,
        }
        response = await self.privateGetWithdraw(self.extend(request, params))
        #
        #     {
        #         "code": 1000,
        #         "message": "success",
        #         "id": "withdrawalId"
        #     }
        #
        transaction = self.parse_transaction(response, currency)
        return self.extend(transaction, {
            'type': 'withdrawal',
            'address': address,
            'addressTo': address,
            'amount': amount,
        })

    async def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            # 'currency': currency['id'],
            # 'pageIndex': 1,
            # 'pageSize': limit,
        }
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if limit is not None:
            request['pageSize'] = limit
        response = await self.privateGetGetWithdrawRecord(self.extend(request, params))
        #
        #     {
        #         "code": 1000,
        #         "message": {
        #             "des": "success",
        #             "isSuc": True,
        #             "datas": {
        #                 "list": [
        #                     {
        #                         "amount": 0.01,
        #                         "fees": 0.001,
        #                         "id": 2016042556231,
        #                         "manageTime": 1461579340000,
        #                         "status": 3,
        #                         "submitTime": 1461579288000,
        #                         "toAddress": "14fxEPirL9fyfw1i9EF439Pq6gQ5xijUmp",
        #                     },
        #                 ],
        #                 "pageIndex": 1,
        #                 "pageSize": 10,
        #                 "totalCount": 4,
        #                 "totalPage": 1
        #             }
        #         }
        #     }
        #
        message = self.safe_value(response, 'message', {})
        datas = self.safe_value(message, 'datas', {})
        withdrawals = self.safe_value(datas, 'list', [])
        return self.parse_transactions(withdrawals, currency, since, limit)

    async def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            # 'currency': currency['id'],
            # 'pageIndex': 1,
            # 'pageSize': limit,
        }
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if limit is not None:
            request['pageSize'] = limit
        response = await self.privateGetGetChargeRecord(self.extend(request, params))
        #
        #     {
        #         "code": 1000,
        #         "message": {
        #             "des": "success",
        #             "isSuc": True,
        #             "datas": {
        #                 "list": [
        #                     {
        #                         "address": "1FKN1DZqCm8HaTujDioRL2Aezdh7Qj7xxx",
        #                         "amount": "1.00000000",
        #                         "confirmTimes": 1,
        #                         "currency": "BTC",
        #                         "description": "Successfully Confirm",
        #                         "hash": "7ce842de187c379abafadd64a5fe66c5c61c8a21fb04edff9532234a1dae6xxx",
        #                         "id": 558,
        #                         "itransfer": 1,
        #                         "status": 2,
        #                         "submit_time": "2016-12-07 18:51:57",
        #                     },
        #                 ],
        #                 "pageIndex": 1,
        #                 "pageSize": 10,
        #                 "total": 8
        #             }
        #         }
        #     }
        #
        message = self.safe_value(response, 'message', {})
        datas = self.safe_value(message, 'datas', {})
        deposits = self.safe_value(datas, 'list', [])
        return self.parse_transactions(deposits, currency, since, limit)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.version + '/' + path
            if params:
                url += '?' + self.urlencode(params)
        else:
            query = self.keysort(self.extend({
                'method': path,
                'accesskey': self.apiKey,
            }, params))
            nonce = self.nonce()
            query = self.keysort(query)
            auth = self.rawencode(query)
            secret = self.hash(self.encode(self.secret), 'sha1')
            signature = self.hmac(self.encode(auth), self.encode(secret), hashlib.md5)
            suffix = 'sign=' + signature + '&reqTime=' + str(nonce)
            url += '/' + path + '?' + auth + '&' + suffix
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        if body[0] == '{':
            feedback = self.id + ' ' + body
            self.throw_broadly_matched_exception(self.exceptions['broad'], body, feedback)
            if 'code' in response:
                code = self.safe_string(response, 'code')
                self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
                if code != '1000':
                    raise ExchangeError(feedback)
            # special case for {"result":false,"message":"服务端忙碌"}(a "Busy Server" reply)
            result = self.safe_value(response, 'result')
            if result is not None:
                if not result:
                    message = self.safe_string(response, 'message')
                    if message == u'服务端忙碌':
                        raise ExchangeNotAvailable(feedback)
                    else:
                        raise ExchangeError(feedback)
