# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection


class btcmarkets(Exchange):

    def describe(self):
        return self.deep_extend(super(btcmarkets, self).describe(), {
            'id': 'btcmarkets',
            'name': 'BTC Markets',
            'countries': ['AU'],  # Australia
            'rateLimit': 1000,  # market data cached for 1 second(trades cached for 2 seconds)
            'version': 'v3',
            'has': {
                'cancelOrder': True,
                'cancelOrders': True,
                'CORS': None,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': 'emulated',
                'fetchDeposits': True,
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchTicker': True,
                'fetchTime': True,
                'fetchTrades': True,
                'fetchTransactions': True,
                'fetchWithdrawals': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/89731817-b3fb8480-da52-11ea-817f-783b08aaf32b.jpg',
                'api': {
                    'public': 'https://api.btcmarkets.net',
                    'private': 'https://api.btcmarkets.net',
                },
                'www': 'https://btcmarkets.net',
                'doc': [
                    'https://api.btcmarkets.net/doc/v3',
                    'https://github.com/BTCMarkets/API',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'markets/{marketId}/ticker',
                        'markets/{marketId}/trades',
                        'markets/{marketId}/orderbook',
                        'markets/{marketId}/candles',
                        'markets/tickers',
                        'markets/orderbooks',
                        'time',
                    ],
                },
                'private': {
                    'get': [
                        'orders',
                        'orders/{id}',
                        'batchorders/{ids}',
                        'trades',
                        'trades/{id}',
                        'withdrawals',
                        'withdrawals/{id}',
                        'deposits',
                        'deposits/{id}',
                        'transfers',
                        'transfers/{id}',
                        'addresses',
                        'withdrawal-fees',
                        'assets',
                        'accounts/me/trading-fees',
                        'accounts/me/withdrawal-limits',
                        'accounts/me/balances',
                        'accounts/me/transactions',
                        'reports/{id}',
                    ],
                    'post': [
                        'orders',
                        'batchorders',
                        'withdrawals',
                        'reports',
                    ],
                    'delete': [
                        'orders',
                        'orders/{id}',
                        'batchorders/{ids}',
                    ],
                    'put': [
                        'orders/{id}',
                    ],
                },
            },
            'timeframes': {
                '1m': '1m',
                '1h': '1h',
                '1d': '1d',
            },
            'exceptions': {
                '3': InvalidOrder,
                '6': DDoSProtection,
                'InsufficientFund': InsufficientFunds,
                'InvalidPrice': InvalidOrder,
                'InvalidAmount': InvalidOrder,
                'MissingArgument': InvalidOrder,
                'OrderAlreadyCancelled': InvalidOrder,
                'OrderNotFound': OrderNotFound,
                'OrderStatusIsFinal': InvalidOrder,
                'InvalidPaginationParameter': BadRequest,
            },
            'fees': {
                'percentage': True,
                'tierBased': True,
                'maker': self.parse_number('-0.0005'),
                'taker': self.parse_number('0.0020'),
            },
            'options': {
                'fees': {
                    'AUD': {
                        'maker': 0.85 / 100,
                        'taker': 0.85 / 100,
                    },
                },
            },
        })

    async def fetch_transactions_with_method(self, method, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        if since is not None:
            request['after'] = since
        currency = None
        if code is not None:
            currency = self.currency(code)
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_transactions(response, currency, since, limit)

    async def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        return await self.fetch_transactions_with_method('privateGetTransfers', code, since, limit, params)

    async def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        return await self.fetch_transactions_with_method('privateGetDeposits', code, since, limit, params)

    async def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        return await self.fetch_transactions_with_method('privateGetWithdrawals', code, since, limit, params)

    def parse_transaction_status(self, status):
        # todo: find more statuses
        statuses = {
            'Complete': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction_type(self, type):
        statuses = {
            'Withdraw': 'withdrawal',
            'Deposit': 'deposit',
        }
        return self.safe_string(statuses, type, type)

    def parse_transaction(self, transaction, currency=None):
        #
        #    {
        #         "id": "6500230339",
        #         "assetName": "XRP",
        #         "amount": "500",
        #         "type": "Deposit",
        #         "creationTime": "2020-07-27T07:52:08.640000Z",
        #         "status": "Complete",
        #         "description": "RIPPLE Deposit, XRP 500",
        #         "fee": "0",
        #         "lastUpdate": "2020-07-27T07:52:08.665000Z",
        #         "paymentDetail": {
        #             "txId": "lsjflsjdfljsd",
        #             "address": "kjasfkjsdf?dt=873874545"
        #         }
        #    }
        #
        #    {
        #         "id": "500985282",
        #         "assetName": "BTC",
        #         "amount": "0.42570126",
        #         "type": "Withdraw",
        #         "creationTime": "2017-07-29T12:49:03.931000Z",
        #         "status": "Complete",
        #         "description": "BTC withdraw from [nick-btcmarkets@snowmonkey.co.uk] to Address: 1B9DsnSYQ54VMqFHVJYdGoLMCYzFwrQzsj amount: 0.42570126 fee: 0.00000000",
        #         "fee": "0.0005",
        #         "lastUpdate": "2017-07-29T12:52:20.676000Z",
        #         "paymentDetail": {
        #             "txId": "fkjdsfjsfljsdfl",
        #             "address": "a;daddjas;djas"
        #         }
        #    }
        #
        #    {
        #         "id": "505102262",
        #         "assetName": "XRP",
        #         "amount": "979.836",
        #         "type": "Deposit",
        #         "creationTime": "2017-07-31T08:50:01.053000Z",
        #         "status": "Complete",
        #         "description": "Ripple Deposit, X 979.8360",
        #         "fee": "0",
        #         "lastUpdate": "2017-07-31T08:50:01.290000Z"
        #     }
        #
        timestamp = self.parse8601(self.safe_string(transaction, 'creationTime'))
        lastUpdate = self.parse8601(self.safe_string(transaction, 'lastUpdate'))
        type = self.parse_transaction_type(self.safe_string_lower(transaction, 'type'))
        if type == 'withdraw':
            type = 'withdrawal'
        cryptoPaymentDetail = self.safe_value(transaction, 'paymentDetail', {})
        txid = self.safe_string(cryptoPaymentDetail, 'txId')
        address = self.safe_string(cryptoPaymentDetail, 'address')
        tag = None
        if address is not None:
            addressParts = address.split('?dt=')
            numParts = len(addressParts)
            if numParts > 1:
                address = addressParts[0]
                tag = addressParts[1]
        addressTo = address
        tagTo = tag
        addressFrom = None
        tagFrom = None
        fee = self.safe_number(transaction, 'fee')
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        currencyId = self.safe_string(transaction, 'assetName')
        code = self.safe_currency_code(currencyId)
        amount = self.safe_number(transaction, 'amount')
        if fee:
            amount -= fee
        return {
            'id': self.safe_string(transaction, 'id'),
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'network': None,
            'address': address,
            'addressTo': addressTo,
            'addressFrom': addressFrom,
            'tag': tag,
            'tagTo': tagTo,
            'tagFrom': tagFrom,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': lastUpdate,
            'fee': {
                'currency': code,
                'cost': fee,
            },
            'info': transaction,
        }

    async def fetch_markets(self, params={}):
        response = await self.publicGetMarkets(params)
        #
        #     [
        #         {
        #             "marketId":"COMP-AUD",
        #             "baseAssetName":"COMP",
        #             "quoteAssetName":"AUD",
        #             "minOrderAmount":"0.00007",
        #             "maxOrderAmount":"1000000",
        #             "amountDecimals":"8",
        #             "priceDecimals":"2"
        #         }
        #     ]
        #
        result = []
        for i in range(0, len(response)):
            market = response[i]
            baseId = self.safe_string(market, 'baseAssetName')
            quoteId = self.safe_string(market, 'quoteAssetName')
            id = self.safe_string(market, 'marketId')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            fees = self.safe_value(self.safe_value(self.options, 'fees', {}), quote, self.fees)
            pricePrecision = self.safe_integer(market, 'priceDecimals')
            amountPrecision = self.safe_integer(market, 'amountDecimals')
            minAmount = self.safe_number(market, 'minOrderAmount')
            maxAmount = self.safe_number(market, 'maxOrderAmount')
            minPrice = None
            if quote == 'AUD':
                minPrice = math.pow(10, -pricePrecision)
            precision = {
                'amount': amountPrecision,
                'price': pricePrecision,
            }
            limits = {
                'amount': {
                    'min': minAmount,
                    'max': maxAmount,
                },
                'price': {
                    'min': minPrice,
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            result.append({
                'info': market,
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'type': 'spot',
                'spot': True,
                'active': None,
                'maker': fees['maker'],
                'taker': fees['taker'],
                'limits': limits,
                'precision': precision,
            })
        return result

    async def fetch_time(self, params={}):
        response = await self.publicGetTime(params)
        #
        #     {
        #         "timestamp": "2019-09-01T18:34:27.045000Z"
        #     }
        #
        return self.parse8601(self.safe_string(response, 'timestamp'))

    def parse_balance(self, response):
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'assetName')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['used'] = self.safe_string(balance, 'locked')
            account['total'] = self.safe_string(balance, 'balance')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetAccountsMeBalances(params)
        return self.parse_balance(response)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         "2020-09-12T18:30:00.000000Z",
        #         "14409.45",  # open
        #         "14409.45",  # high
        #         "14403.91",  # low
        #         "14403.91",  # close
        #         "0.01571701"  # volume
        #     ]
        #
        return [
            self.parse8601(self.safe_string(ohlcv, 0)),
            self.safe_number(ohlcv, 1),  # open
            self.safe_number(ohlcv, 2),  # high
            self.safe_number(ohlcv, 3),  # low
            self.safe_number(ohlcv, 4),  # close
            self.safe_number(ohlcv, 5),  # volume
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'marketId': market['id'],
            'timeWindow': self.timeframes[timeframe],
            # 'from': self.iso8601(since),
            # 'to': self.iso8601(self.milliseconds()),
            # 'before': 1234567890123,
            # 'after': 1234567890123,
            # 'limit': limit,  # default 10, max 200
        }
        if since is not None:
            request['from'] = self.iso8601(since)
        if limit is not None:
            request['limit'] = limit  # default is 10, max 200
        response = await self.publicGetMarketsMarketIdCandles(self.extend(request, params))
        #
        #     [
        #         ["2020-09-12T18:30:00.000000Z","14409.45","14409.45","14403.91","14403.91","0.01571701"],
        #         ["2020-09-12T18:21:00.000000Z","14409.45","14409.45","14409.45","14409.45","0.0035"],
        #         ["2020-09-12T18:03:00.000000Z","14361.37","14361.37","14361.37","14361.37","0.00345221"],
        #     ]
        #
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'marketId': market['id'],
        }
        response = await self.publicGetMarketsMarketIdOrderbook(self.extend(request, params))
        #
        #     {
        #         "marketId":"BTC-AUD",
        #         "snapshotId":1599936148941000,
        #         "asks":[
        #             ["14459.45","0.00456475"],
        #             ["14463.56","2"],
        #             ["14470.91","0.98"],
        #         ],
        #         "bids":[
        #             ["14421.01","0.52"],
        #             ["14421","0.75"],
        #             ["14418","0.3521"],
        #         ]
        #     }
        #
        timestamp = self.safe_integer_product(response, 'snapshotId', 0.001)
        orderbook = self.parse_order_book(response, symbol, timestamp)
        orderbook['nonce'] = self.safe_integer(response, 'snapshotId')
        return orderbook

    def parse_ticker(self, ticker, market=None):
        #
        # fetchTicker
        #
        #     {
        #         "marketId":"BAT-AUD",
        #         "bestBid":"0.3751",
        #         "bestAsk":"0.377",
        #         "lastPrice":"0.3769",
        #         "volume24h":"56192.97613335",
        #         "volumeQte24h":"21179.13270465",
        #         "price24h":"0.0119",
        #         "pricePct24h":"3.26",
        #         "low24h":"0.3611",
        #         "high24h":"0.3799",
        #         "timestamp":"2020-08-09T18:28:23.280000Z"
        #     }
        #
        symbol = None
        marketId = self.safe_string(ticker, 'marketId')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId, quoteId = marketId.split('-')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(ticker, 'timestamp'))
        last = self.safe_number(ticker, 'lastPrice')
        baseVolume = self.safe_number(ticker, 'volume24h')
        quoteVolume = self.safe_number(ticker, 'volumeQte24h')
        vwap = self.vwap(baseVolume, quoteVolume)
        change = self.safe_number(ticker, 'price24h')
        percentage = self.safe_number(ticker, 'pricePct24h')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high24h'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'bestBid'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'bestAsk'),
            'askVolume': None,
            'vwap': vwap,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'marketId': market['id'],
        }
        response = await self.publicGetMarketsMarketIdTicker(self.extend(request, params))
        #
        #     {
        #         "marketId":"BAT-AUD",
        #         "bestBid":"0.3751",
        #         "bestAsk":"0.377",
        #         "lastPrice":"0.3769",
        #         "volume24h":"56192.97613335",
        #         "volumeQte24h":"21179.13270465",
        #         "price24h":"0.0119",
        #         "pricePct24h":"3.26",
        #         "low24h":"0.3611",
        #         "high24h":"0.3799",
        #         "timestamp":"2020-08-09T18:28:23.280000Z"
        #     }
        #
        return self.parse_ticker(response, market)

    async def fetch_ticker2(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = await self.publicGetMarketIdTick(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        #
        # public fetchTrades
        #
        #     {
        #         "id":"6191646611",
        #         "price":"539.98",
        #         "amount":"0.5",
        #         "timestamp":"2020-08-09T15:21:05.016000Z",
        #         "side":"Ask"
        #     }
        #
        # private fetchMyTrades
        #
        #     {
        #         "id": "36014819",
        #         "marketId": "XRP-AUD",
        #         "timestamp": "2019-06-25T16:01:02.977000Z",
        #         "price": "0.67",
        #         "amount": "1.50533262",
        #         "side": "Ask",
        #         "fee": "0.00857285",
        #         "orderId": "3648306",
        #         "liquidityType": "Taker",
        #         "clientOrderId": "48"
        #     }
        #
        timestamp = self.parse8601(self.safe_string(trade, 'timestamp'))
        marketId = self.safe_string(trade, 'marketId')
        symbol = None
        base = None
        quote = None
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId, quoteId = marketId.split('-')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
            base = market['base']
            quote = market['quote']
        feeCurrencyCode = None
        if quote == 'AUD':
            feeCurrencyCode = quote
        else:
            feeCurrencyCode = base
        side = self.safe_string(trade, 'side')
        if side == 'Bid':
            side = 'buy'
        elif side == 'Ask':
            side = 'sell'
        id = self.safe_string(trade, 'id')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        orderId = self.safe_string(trade, 'orderId')
        fee = None
        feeCostString = self.safe_string(trade, 'fee')
        if feeCostString is not None:
            fee = {
                'cost': feeCostString,
                'currency': feeCurrencyCode,
            }
        takerOrMaker = self.safe_string_lower(trade, 'liquidityType')
        return self.safe_trade({
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': orderId,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'takerOrMaker': takerOrMaker,
            'fee': fee,
        }, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            # 'since': 59868345231,
            'marketId': market['id'],
        }
        response = await self.publicGetMarketsMarketIdTrades(self.extend(request, params))
        #
        #     [
        #         {"id":"6191646611","price":"539.98","amount":"0.5","timestamp":"2020-08-09T15:21:05.016000Z","side":"Ask"},
        #         {"id":"6191646610","price":"539.99","amount":"0.5","timestamp":"2020-08-09T15:21:05.015000Z","side":"Ask"},
        #         {"id":"6191646590","price":"540","amount":"0.00233785","timestamp":"2020-08-09T15:21:04.171000Z","side":"Bid"},
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'marketId': market['id'],
            # 'price': self.price_to_precision(symbol, price),
            'amount': self.amount_to_precision(symbol, amount),
            # 'type': 'Limit',  # "Limit", "Market", "Stop Limit", "Stop", "Take Profit"
            'side': 'Bid' if (side == 'buy') else 'Ask',
            # 'triggerPrice': self.price_to_precision(symbol, triggerPrice),  # required for Stop, Stop Limit, Take Profit orders
            # 'targetAmount': self.amount_to_precision(symbol, targetAmount),  # target amount when a desired target outcome is required for order execution
            # 'timeInForce': 'GTC',  # GTC, FOK, IOC
            # 'postOnly': False,  # boolean if self is a post-only order
            # 'selfTrade': 'A',  # A = allow, P = prevent
            # 'clientOrderId': self.uuid(),
        }
        lowercaseType = type.lower()
        orderTypes = self.safe_value(self.options, 'orderTypes', {
            'limit': 'Limit',
            'market': 'Market',
            'stop': 'Stop',
            'stop limit': 'Stop Limit',
            'take profit': 'Take Profit',
        })
        request['type'] = self.safe_string(orderTypes, lowercaseType, type)
        priceIsRequired = False
        triggerPriceIsRequired = False
        if lowercaseType == 'limit':
            priceIsRequired = True
        # elif lowercaseType == 'market':
        #     ...
        # }
        elif lowercaseType == 'stop limit':
            triggerPriceIsRequired = True
            priceIsRequired = True
        elif lowercaseType == 'take profit':
            triggerPriceIsRequired = True
        elif lowercaseType == 'stop':
            triggerPriceIsRequired = True
        if priceIsRequired:
            if price is None:
                raise ArgumentsRequired(self.id + ' createOrder() requires a price argument for a ' + type + 'order')
            else:
                request['price'] = self.price_to_precision(symbol, price)
        if triggerPriceIsRequired:
            triggerPrice = self.safe_number(params, 'triggerPrice')
            params = self.omit(params, 'triggerPrice')
            if triggerPrice is None:
                raise ArgumentsRequired(self.id + ' createOrder() requires a triggerPrice parameter for a ' + type + 'order')
            else:
                request['triggerPrice'] = self.price_to_precision(symbol, triggerPrice)
        clientOrderId = self.safe_string(params, 'clientOrderId')
        if clientOrderId is not None:
            request['clientOrderId'] = clientOrderId
        params = self.omit(params, 'clientOrderId')
        response = await self.privatePostOrders(self.extend(request, params))
        #
        #     {
        #         "orderId": "7524",
        #         "marketId": "BTC-AUD",
        #         "side": "Bid",
        #         "type": "Limit",
        #         "creationTime": "2019-08-30T11:08:21.956000Z",
        #         "price": "100.12",
        #         "amount": "1.034",
        #         "openAmount": "1.034",
        #         "status": "Accepted",
        #         "clientOrderId": "1234-5678",
        #         "timeInForce": "IOC",
        #         "postOnly": False,
        #         "selfTrade": "P",
        #         "triggerAmount": "105",
        #         "targetAmount": "1000"
        #     }
        #
        return self.parse_order(response, market)

    async def cancel_orders(self, ids, symbol=None, params={}):
        await self.load_markets()
        for i in range(0, len(ids)):
            ids[i] = int(ids[i])
        request = {
            'ids': ids,
        }
        return await self.privateDeleteBatchordersIds(self.extend(request, params))

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        return await self.privateDeleteOrdersId(self.extend(request, params))

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        rate = market[takerOrMaker]
        currency = None
        cost = None
        if market['quote'] == 'AUD':
            currency = market['quote']
            cost = float(self.cost_to_precision(symbol, amount * price))
        else:
            currency = market['base']
            cost = float(self.amount_to_precision(symbol, amount))
        return {
            'type': takerOrMaker,
            'currency': currency,
            'rate': rate,
            'cost': float(self.fee_to_precision(symbol, rate * cost)),
        }

    def parse_order_status(self, status):
        statuses = {
            'Accepted': 'open',
            'Placed': 'open',
            'Partially Matched': 'open',
            'Fully Matched': 'closed',
            'Cancelled': 'canceled',
            'Partially Cancelled': 'canceled',
            'Failed': 'rejected',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "orderId": "7524",
        #         "marketId": "BTC-AUD",
        #         "side": "Bid",
        #         "type": "Limit",
        #         "creationTime": "2019-08-30T11:08:21.956000Z",
        #         "price": "100.12",
        #         "amount": "1.034",
        #         "openAmount": "1.034",
        #         "status": "Accepted",
        #         "clientOrderId": "1234-5678",
        #         "timeInForce": "IOC",
        #         "postOnly": False,
        #         "selfTrade": "P",
        #         "triggerAmount": "105",
        #         "targetAmount": "1000"
        #     }
        #
        timestamp = self.parse8601(self.safe_string(order, 'creationTime'))
        marketId = self.safe_string(order, 'marketId')
        symbol = None
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId, quoteId = marketId.split('-')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        side = self.safe_string(order, 'side')
        if side == 'Bid':
            side = 'buy'
        elif side == 'Ask':
            side = 'sell'
        type = self.safe_string_lower(order, 'type')
        price = self.safe_string(order, 'price')
        amount = self.safe_string(order, 'amount')
        remaining = self.safe_string(order, 'openAmount')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'orderId')
        clientOrderId = self.safe_string(order, 'clientOrderId')
        timeInForce = self.safe_string(order, 'timeInForce')
        stopPrice = self.safe_number(order, 'triggerPrice')
        postOnly = self.safe_value(order, 'postOnly')
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'timeInForce': timeInForce,
            'postOnly': postOnly,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'cost': None,
            'amount': amount,
            'filled': None,
            'remaining': remaining,
            'average': None,
            'status': status,
            'trades': None,
            'fee': None,
        }, market)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        response = await self.privateGetOrdersId(self.extend(request, params))
        return self.parse_order(response)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'status': 'all',
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['marketId'] = market['id']
        if since is not None:
            request['after'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {'status': 'open'}
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = await self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['marketId'] = market['id']
        if since is not None:
            request['after'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetTrades(self.extend(request, params))
        #
        #     [
        #         {
        #             "id": "36014819",
        #             "marketId": "XRP-AUD",
        #             "timestamp": "2019-06-25T16:01:02.977000Z",
        #             "price": "0.67",
        #             "amount": "1.50533262",
        #             "side": "Ask",
        #             "fee": "0.00857285",
        #             "orderId": "3648306",
        #             "liquidityType": "Taker",
        #             "clientOrderId": "48"
        #         },
        #         {
        #             "id": "3568960",
        #             "marketId": "GNT-AUD",
        #             "timestamp": "2019-06-20T08:44:04.488000Z",
        #             "price": "0.1362",
        #             "amount": "0.85",
        #             "side": "Bid",
        #             "fee": "0.00098404",
        #             "orderId": "3543015",
        #             "liquidityType": "Maker"
        #         }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    def lookup_symbol_from_market_id(self, marketId):
        market = None
        symbol = None
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId, quoteId = marketId.split('-')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        return symbol

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.version + '/' + self.implode_params(path, params)
        query = self.keysort(self.omit(params, self.extract_params(path)))
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            secret = self.base64_to_binary(self.encode(self.secret))
            auth = method + request + nonce
            if (method == 'GET') or (method == 'DELETE'):
                if query:
                    request += '?' + self.urlencode(query)
            else:
                body = self.json(query)
                auth += body
            signature = self.hmac(self.encode(auth), secret, hashlib.sha512, 'base64')
            headers = {
                'Accept': 'application/json',
                'Accept-Charset': 'UTF-8',
                'Content-Type': 'application/json',
                'BM-AUTH-APIKEY': self.apiKey,
                'BM-AUTH-TIMESTAMP': nonce,
                'BM-AUTH-SIGNATURE': signature,
            }
        elif api == 'public':
            if query:
                request += '?' + self.urlencode(query)
        url = self.urls['api'][api] + request
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        if 'success' in response:
            if not response['success']:
                error = self.safe_string(response, 'errorCode')
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions, error, feedback)
                raise ExchangeError(feedback)
        # v3 api errors
        if code >= 400:
            errorCode = self.safe_string(response, 'code')
            message = self.safe_string(response, 'message')
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
            self.throw_exactly_matched_exception(self.exceptions, message, feedback)
            raise ExchangeError(feedback)
