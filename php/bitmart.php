<?php

namespace ccxtpro;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import
use \ccxt\AuthenticationError;
use \ccxt\ArgumentsRequired;

class bitmart extends \ccxt\async\bitmart {

    use ClientTrait;

    public function describe() {
        return $this->deep_extend(parent::describe (), array(
            'has' => array(
                'ws' => true,
                'watchTicker' => true,
                'watchOrderBook' => true,
                'watchOrders' => true,
                'watchTrades' => true,
                'watchOHLCV' => true,
            ),
            'urls' => array(
                'api' => array(
                    'ws' => array(
                        'public' => 'wss://ws-manager-compress.{hostname}/api?protocol=1.1',
                        'private' => 'wss://ws-manager-compress.{hostname}/user?protocol=1.1',
                    ),
                ),
            ),
            'options' => array(
                'defaultType' => 'spot',
                'watchOrderBook' => array(
                    'depth' => 'depth5', // depth5, depth400
                ),
                'ws' => array(
                    'inflate' => true,
                ),
                'timeframes' => array(
                    '1m' => '1m',
                    '3m' => '3m',
                    '5m' => '5m',
                    '15m' => '15m',
                    '30m' => '30m',
                    '45m' => '45m',
                    '1h' => '1H',
                    '2h' => '2H',
                    '3h' => '3H',
                    '4h' => '4H',
                    '1d' => '1D',
                    '1w' => '1W',
                    '1M' => '1M',
                ),
            ),
            'streaming' => array(
                'keepAlive' => 15000,
            ),
        ));
    }

    public function subscribe($channel, $symbol, $params = array ()) {
        yield $this->load_markets();
        $market = $this->market($symbol);
        $url = $this->implode_hostname($this->urls['api']['ws']['public']);
        $messageHash = $market['type'] . '/' . $channel . ':' . $market['id'];
        $request = array(
            'op' => 'subscribe',
            'args' => array( $messageHash ),
        );
        return yield $this->watch($url, $messageHash, $this->deep_extend($request, $params), $messageHash);
    }

    public function subscribe_private($channel, $symbol, $params = array ()) {
        yield $this->load_markets();
        $market = $this->market($symbol);
        $url = $this->implode_hostname($this->urls['api']['ws']['private']);
        $messageHash = $channel . ':' . $market['id'];
        yield $this->authenticate();
        $request = array(
            'op' => 'subscribe',
            'args' => array( $messageHash ),
        );
        return yield $this->watch($url, $messageHash, $this->deep_extend($request, $params), $messageHash);
    }

    public function watch_trades($symbol, $since = null, $limit = null, $params = array ()) {
        $trades = yield $this->subscribe('trade', $symbol, $params);
        if ($this->newUpdates) {
            $limit = $trades->getLimit ($symbol, $limit);
        }
        return $this->filter_by_since_limit($trades, $since, $limit, 'timestamp', true);
    }

    public function watch_ticker($symbol, $params = array ()) {
        return yield $this->subscribe('ticker', $symbol, $params);
    }

    public function watch_orders($symbol = null, $since = null, $limit = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' watchOrders requires a $symbol argument');
        }
        yield $this->load_markets();
        $market = $this->market($symbol);
        if ($market['type'] !== 'spot') {
            throw new ArgumentsRequired($this->id . ' watchOrders supports spot markets only');
        }
        $channel = 'spot/user/order';
        $orders = yield $this->subscribe_private($channel, $symbol, $params);
        if ($this->newUpdates) {
            $limit = $orders->getLimit ($symbol, $limit);
        }
        return $this->filter_by_symbol_since_limit($orders, $symbol, $since, $limit, true);
    }

    public function handle_orders($client, $message) {
        //
        // {
        //     "data":array(
        //         {
        //             $symbol => 'LTC_USDT',
        //             notional => '',
        //             side => 'buy',
        //             last_fill_time => '0',
        //             ms_t => '1646216634000',
        //             type => 'limit',
        //             filled_notional => '0.000000000000000000000000000000',
        //             last_fill_price => '0',
        //             size => '0.500000000000000000000000000000',
        //             price => '50.000000000000000000000000000000',
        //             last_fill_count => '0',
        //             filled_size => '0.000000000000000000000000000000',
        //             margin_trading => '0',
        //             state => '8',
        //             order_id => '24807076628',
        //             order_type => '0'
        //           }
        //     ),
        //     "table":"spot/user/order"
        // }
        //
        $channel = $this->safe_string($message, 'table');
        $orders = $this->safe_value($message, 'data', array());
        $ordersLength = count($orders);
        if ($ordersLength > 0) {
            $limit = $this->safe_integer($this->options, 'ordersLimit', 1000);
            if ($this->orders === null) {
                $this->orders = new ArrayCacheBySymbolById ($limit);
            }
            $stored = $this->orders;
            $marketIds = array();
            for ($i = 0; $i < count($orders); $i++) {
                $order = $this->parse_ws_order($orders[$i]);
                $stored->append ($order);
                $symbol = $order['symbol'];
                $market = $this->market($symbol);
                $marketIds[] = $market['id'];
            }
            for ($i = 0; $i < count($marketIds); $i++) {
                $messageHash = $channel . ':' . $marketIds[$i];
                $client->resolve ($this->orders, $messageHash);
            }
        }
    }

    public function parse_ws_order($order, $market = null) {
        //
        // {
        //     $symbol => 'LTC_USDT',
        //     notional => '',
        //     $side => 'buy',
        //     last_fill_time => '0',
        //     ms_t => '1646216634000',
        //     $type => 'limit',
        //     filled_notional => '0.000000000000000000000000000000',
        //     last_fill_price => '0',
        //     size => '0.500000000000000000000000000000',
        //     $price => '50.000000000000000000000000000000',
        //     last_fill_count => '0',
        //     filled_size => '0.000000000000000000000000000000',
        //     margin_trading => '0',
        //     state => '8',
        //     order_id => '24807076628',
        //     order_type => '0'
        //   }
        //
        $marketId = $this->safe_string($order, 'symbol');
        $market = $this->safe_market($marketId, $market);
        $id = $this->safe_string($order, 'order_id');
        $clientOrderId = $this->safe_string($order, 'clientOid');
        $price = $this->safe_string($order, 'price');
        $filled = $this->safe_string($order, 'filled_size');
        $amount = $this->safe_string($order, 'size');
        $type = $this->safe_string($order, 'type');
        $rawState = $this->safe_string($order, 'state');
        $status = $this->parseOrderStatusByType ($market['type'], $rawState);
        $timestamp = $this->safe_integer($order, 'ms_t');
        $symbol = $market['symbol'];
        $side = $this->safe_string_lower($order, 'side');
        return $this->safe_order(array(
            'info' => $order,
            'symbol' => $symbol,
            'id' => $id,
            'clientOrderId' => $clientOrderId,
            'timestamp' => null,
            'datetime' => null,
            'lastTradeTimestamp' => $timestamp,
            'type' => $type,
            'timeInForce' => null,
            'postOnly' => null,
            'side' => $side,
            'price' => $price,
            'stopPrice' => null,
            'amount' => $amount,
            'cost' => null,
            'average' => null,
            'filled' => $filled,
            'remaining' => null,
            'status' => $status,
            'fee' => null,
            'trades' => null,
        ), $market);
    }

    public function handle_trade($client, $message) {
        //
        //     {
        //         $table => 'spot/trade',
        //         $data => array(
        //             array(
        //                 price => '52700.50',
        //                 s_t => 1630982050,
        //                 side => 'buy',
        //                 size => '0.00112',
        //                 $symbol => 'BTC_USDT'
        //             ),
        //         )
        //     }
        //
        $table = $this->safe_string($message, 'table');
        $data = $this->safe_value($message, 'data', array());
        $tradesLimit = $this->safe_integer($this->options, 'tradesLimit', 1000);
        for ($i = 0; $i < count($data); $i++) {
            $trade = $this->parse_trade($data[$i]);
            $symbol = $trade['symbol'];
            $marketId = $this->safe_string($trade['info'], 'symbol');
            $messageHash = $table . ':' . $marketId;
            $stored = $this->safe_value($this->trades, $symbol);
            if ($stored === null) {
                $stored = new ArrayCache ($tradesLimit);
                $this->trades[$symbol] = $stored;
            }
            $stored->append ($trade);
            $client->resolve ($stored, $messageHash);
        }
        return $message;
    }

    public function handle_ticker($client, $message) {
        //
        //     {
        //         $data => array(
        //             {
        //                 base_volume_24h => '78615593.81',
        //                 high_24h => '52756.97',
        //                 last_price => '52638.31',
        //                 low_24h => '50991.35',
        //                 open_24h => '51692.03',
        //                 s_t => 1630981727,
        //                 $symbol => 'BTC_USDT'
        //             }
        //         ),
        //         $table => 'spot/ticker'
        //     }
        //
        $table = $this->safe_string($message, 'table');
        $data = $this->safe_value($message, 'data', array());
        for ($i = 0; $i < count($data); $i++) {
            $ticker = $this->parse_ticker($data[$i]);
            $symbol = $ticker['symbol'];
            $marketId = $this->safe_string($ticker['info'], 'symbol');
            $messageHash = $table . ':' . $marketId;
            $this->tickers[$symbol] = $ticker;
            $client->resolve ($ticker, $messageHash);
        }
        return $message;
    }

    public function watch_ohlcv($symbol, $timeframe = '1m', $since = null, $limit = null, $params = array ()) {
        $timeframes = $this->safe_value($this->options, 'timeframes', array());
        $interval = $this->safe_string($timeframes, $timeframe);
        $name = 'kline' . $interval;
        $ohlcv = yield $this->subscribe($name, $symbol, $params);
        if ($this->newUpdates) {
            $limit = $ohlcv->getLimit ($symbol, $limit);
        }
        return $this->filter_by_since_limit($ohlcv, $since, $limit, 0, true);
    }

    public function handle_ohlcv($client, $message) {
        //
        //     {
        //         $data => array(
        //             {
        //                 $candle => array(
        //                     1631056350,
        //                     '46532.83',
        //                     '46555.71',
        //                     '46511.41',
        //                     '46555.71',
        //                     '0.25'
        //                 ),
        //                 $symbol => 'BTC_USDT'
        //             }
        //         ),
        //         $table => 'spot/kline1m'
        //     }
        //
        $table = $this->safe_string($message, 'table');
        $data = $this->safe_value($message, 'data', array());
        $parts = explode('/', $table);
        $part1 = $this->safe_string($parts, 1);
        $interval = str_replace('kline', '', $part1);
        // use a reverse lookup in a static map instead
        $timeframes = $this->safe_value($this->options, 'timeframes', array());
        $timeframe = $this->find_timeframe($interval, $timeframes);
        $duration = $this->parse_timeframe($timeframe);
        $durationInMs = $duration * 1000;
        for ($i = 0; $i < count($data); $i++) {
            $marketId = $this->safe_string($data[$i], 'symbol');
            $candle = $this->safe_value($data[$i], 'candle');
            $market = $this->safe_market($marketId);
            $symbol = $market['symbol'];
            $parsed = $this->parse_ohlcv($candle, $market);
            $parsed[0] = intval($parsed[0] / $durationInMs) * $durationInMs;
            $this->ohlcvs[$symbol] = $this->safe_value($this->ohlcvs, $symbol, array());
            $stored = $this->safe_value($this->ohlcvs[$symbol], $timeframe);
            if ($stored === null) {
                $limit = $this->safe_integer($this->options, 'OHLCVLimit', 1000);
                $stored = new ArrayCacheByTimestamp ($limit);
                $this->ohlcvs[$symbol][$timeframe] = $stored;
            }
            $stored->append ($parsed);
            $messageHash = $table . ':' . $marketId;
            $client->resolve ($stored, $messageHash);
        }
    }

    public function watch_order_book($symbol, $limit = null, $params = array ()) {
        $options = $this->safe_value($this->options, 'watchOrderBook', array());
        $depth = $this->safe_string($options, 'depth', 'depth400');
        $orderbook = yield $this->subscribe($depth, $symbol, $params);
        return $orderbook->limit ($limit);
    }

    public function handle_delta($bookside, $delta) {
        $price = $this->safe_float($delta, 0);
        $amount = $this->safe_float($delta, 1);
        $bookside->store ($price, $amount);
    }

    public function handle_deltas($bookside, $deltas) {
        for ($i = 0; $i < count($deltas); $i++) {
            $this->handle_delta($bookside, $deltas[$i]);
        }
    }

    public function handle_order_book_message($client, $message, $orderbook) {
        //
        //     {
        //         $asks => array(
        //             array( '46828.38', '0.21847' ),
        //             array( '46830.68', '0.08232' ),
        //             array( '46832.08', '0.09285' ),
        //             array( '46837.82', '0.02028' ),
        //             array( '46839.43', '0.15068' )
        //         ),
        //         $bids => array(
        //             array( '46820.78', '0.00444' ),
        //             array( '46814.33', '0.00234' ),
        //             array( '46813.50', '0.05021' ),
        //             array( '46808.14', '0.00217' ),
        //             array( '46808.04', '0.00013' )
        //         ),
        //         ms_t => 1631044962431,
        //         $symbol => 'BTC_USDT'
        //     }
        //
        $asks = $this->safe_value($message, 'asks', array());
        $bids = $this->safe_value($message, 'bids', array());
        $this->handle_deltas($orderbook['asks'], $asks);
        $this->handle_deltas($orderbook['bids'], $bids);
        $timestamp = $this->safe_integer($message, 'ms_t');
        $marketId = $this->safe_string($message, 'symbol');
        $symbol = $this->safe_symbol($marketId);
        $orderbook['symbol'] = $symbol;
        $orderbook['timestamp'] = $timestamp;
        $orderbook['datetime'] = $this->iso8601($timestamp);
        return $orderbook;
    }

    public function handle_order_book($client, $message) {
        //
        //     {
        //         $data => array(
        //             {
        //                 asks => array(
        //                     array( '46828.38', '0.21847' ),
        //                     array( '46830.68', '0.08232' ),
        //                     array( '46832.08', '0.09285' ),
        //                     array( '46837.82', '0.02028' ),
        //                     array( '46839.43', '0.15068' )
        //                 ),
        //                 bids => array(
        //                     array( '46820.78', '0.00444' ),
        //                     array( '46814.33', '0.00234' ),
        //                     array( '46813.50', '0.05021' ),
        //                     array( '46808.14', '0.00217' ),
        //                     array( '46808.04', '0.00013' )
        //                 ),
        //                 ms_t => 1631044962431,
        //                 $symbol => 'BTC_USDT'
        //             }
        //         ),
        //         $table => 'spot/depth5'
        //     }
        //
        $data = $this->safe_value($message, 'data', array());
        $table = $this->safe_string($message, 'table');
        $parts = explode('/', $table);
        $lastPart = $this->safe_string($parts, 1);
        $limitString = str_replace('depth', '', $lastPart);
        $limit = intval($limitString);
        for ($i = 0; $i < count($data); $i++) {
            $update = $data[$i];
            $marketId = $this->safe_string($update, 'symbol');
            $symbol = $this->safe_symbol($marketId);
            $orderbook = $this->safe_value($this->orderbooks, $symbol);
            if ($orderbook === null) {
                $orderbook = $this->order_book(array(), $limit);
                $this->orderbooks[$symbol] = $orderbook;
            }
            $orderbook->reset (array());
            $this->handle_order_book_message($client, $update, $orderbook);
            $messageHash = $table . ':' . $marketId;
            $client->resolve ($orderbook, $messageHash);
        }
        return $message;
    }

    public function authenticate($params = array ()) {
        $this->check_required_credentials();
        $url = $this->implode_hostname($this->urls['api']['ws']['private']);
        $messageHash = 'login';
        $client = $this->client($url);
        $future = $this->safe_value($client->subscriptions, $messageHash);
        if ($future === null) {
            $future = $client->future ('authenticated');
            $timestamp = (string) $this->milliseconds();
            $memo = $this->uid;
            $path = 'bitmart.WebSocket';
            $auth = $timestamp . '#' . $memo . '#' . $path;
            $signature = $this->hmac($this->encode($auth), $this->encode($this->secret), 'sha256');
            $request = array(
                'op' => $messageHash,
                'args' => array(
                    $this->apiKey,
                    $timestamp,
                    $signature,
                ),
            );
            $this->spawn(array($this, 'watch'), $url, $messageHash, $request, $messageHash, $future);
        }
        return yield $future;
    }

    public function handle_subscription_status($client, $message) {
        //
        //     array("event":"subscribe","channel":"spot/depth:BTC-USDT")
        //
        return $message;
    }

    public function handle_authenticate($client, $message) {
        //
        //     array( event => 'login', success => true )
        //
        $client->resolve ($message, 'authenticated');
        return $message;
    }

    public function handle_error_message($client, $message) {
        //
        //     array( event => 'error', $message => 'Invalid sign', $errorCode => 30013 )
        //     array("event":"error","message":"Unrecognized request => array(\"event\":\"subscribe\",\"channel\":\"spot/depth:BTC-USDT\")","errorCode":30039)
        //
        $errorCode = $this->safe_string($message, 'errorCode');
        try {
            if ($errorCode !== null) {
                $feedback = $this->id . ' ' . $this->json($message);
                $this->throw_exactly_matched_exception($this->exceptions['exact'], $errorCode, $feedback);
                $messageString = $this->safe_value($message, 'message');
                if ($messageString !== null) {
                    $this->throw_broadly_matched_exception($this->exceptions['broad'], $messageString, $feedback);
                }
            }
        } catch (Exception $e) {
            if ($e instanceof AuthenticationError) {
                $client->reject ($e, 'authenticated');
                $method = 'login';
                if (is_array($client->subscriptions) && array_key_exists($method, $client->subscriptions)) {
                    unset($client->subscriptions[$method]);
                }
                return false;
            }
        }
        return $message;
    }

    public function handle_message($client, $message) {
        if (!$this->handle_error_message($client, $message)) {
            return;
        }
        //
        //     array("event":"error","message":"Unrecognized request => array(\"event\":\"subscribe\",\"channel\":\"spot/depth:BTC-USDT\")","errorCode":30039)
        //     array("event":"subscribe","channel":"spot/depth:BTC-USDT")
        //     {
        //         $table => "spot/depth",
        //         action => "partial",
        //         data => [
        //             {
        //                 instrument_id =>   "BTC-USDT",
        //                 asks => [
        //                     ["5301.8", "0.03763319", "1"],
        //                     ["5302.4", "0.00305", "2"],
        //                 ],
        //                 bids => [
        //                     ["5301.7", "0.58911427", "6"],
        //                     ["5301.6", "0.01222922", "4"],
        //                 ],
        //                 timestamp => "2020-03-16T03:25:00.440Z",
        //                 checksum => -2088736623
        //             }
        //         ]
        //     }
        //
        //     array( data => '', $table => 'spot/user/order' )
        //
        $table = $this->safe_string($message, 'table');
        if ($table === null) {
            $event = $this->safe_string($message, 'event');
            if ($event !== null) {
                $methods = array(
                    // 'info' => $this->handleSystemStatus,
                    // 'book' => 'handleOrderBook',
                    'login' => array($this, 'handle_authenticate'),
                    'subscribe' => array($this, 'handle_subscription_status'),
                );
                $method = $this->safe_value($methods, $event);
                if ($method === null) {
                    return $message;
                } else {
                    return $method($client, $message);
                }
            }
        } else {
            $parts = explode('/', $table);
            $name = $this->safe_string($parts, 1);
            $methods = array(
                'depth' => array($this, 'handle_order_book'),
                'depth5' => array($this, 'handle_order_book'),
                'depth400' => array($this, 'handle_order_book'),
                'ticker' => array($this, 'handle_ticker'),
                'trade' => array($this, 'handle_trade'),
                // ...
            );
            $method = $this->safe_value($methods, $name);
            if (mb_strpos($name, 'kline') !== false) {
                $method = array($this, 'handle_ohlcv');
            }
            $privateName = $this->safe_string($parts, 2);
            if ($privateName === 'order') {
                $method = array($this, 'handle_orders');
            }
            if ($method === null) {
                return $message;
            } else {
                return $method($client, $message);
            }
        }
    }
}
