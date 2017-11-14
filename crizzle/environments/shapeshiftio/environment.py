import json
import logging
from urllib.parse import urlencode
from urllib.request import urlopen, Request

from crizzle.environments import base

logger = logging.getLogger(__name__)


class Environment(base.Environment):
    """
    Shapeshift API
    """

    def __init__(self, key_file=None):
        # TODO: simplify __init__
        self.base_url = "https://shapeshift.io"
        self._key = None
        self._secret = None
        self.url = ''

        if key_file is not None:
            self.load_api_key(key_file)

    def hashify(self, url=None, data=None):
        pass

    def query_private(self, url, data=None, params=None, headers=None):
        pass

    def query_public(self, url, data=None, params=None, headers=None):
        pass

    def query(self, url, data=None, params=None, headers=None, post=False):
        pass

    def load_api_key(self, key_file):
        with open(key_file, 'r') as key:
            lines = key.readlines()
            try:
                assert len(lines) == 2
            except AssertionError as e:
                logger.fatal('Key file must contain public and secret key on exactly two lines')
                raise e
            self._key, self._secret = key.readlines()

    def parse_returned(self, returned):
        if 'error' in returned:
            raise Exception(returned['error'])
        else:
            return returned

    def get_positions(self) -> list:
        pass

    def get_current_rate(self, pair: str):
        pass

    def get_request(self, url):
        ret = urlopen(Request(url))
        return self.parse_returned(json.loads(ret.read().decode('utf-8')))

    def post_request(self, url, postdata):
        ret = urlopen(Request(url, urlencode(postdata).encode()))
        return self.parse_returned(json.loads(ret.read().decode('utf-8')))

    def _rate(self, pair):
        """
        Gets the current rate offered by Shapeshift.
        This is an estimate because the rate can occasionally change rapidly depending on the markets.
        The rate is also a 'use-able' rate not a direct market rate.
        Meaning multiplying your input coin amount times the rate should give
        you a close approximation of what will be sent out.
        This rate does not include the transaction (miner) fee taken off every transaction.

        [pair] is any valid coin pair such as btc_ltc or ltc_btc

        Success Output:

            {
                "pair" : "btc_ltc",
                "rate" : "70.1234"
            }
        """
        self.url = self.base_url + "/rate/" + pair
        return self.get_request(self.url)

    def _market_info(self, pair):
        """
        This gets the market info (pair, rate, limit, minimum limit, miner fee)

    [pair] (OPTIONAL) is any valid coin pair such as btc_ltc or ltc_btc.
    The pair is not required and if not specified will return an array of all market infos.

    Success Output:
            {
            "pair"     : "btc_ltc",
            "rate"     : 130.12345678,
            "limit"    : 1.2345,
            "min"      : 0.002621232,
            "minerFee" : 0.0001
            }

        """
        # noinspection SpellCheckingInspection
        self.url = self.base_url + "/marketinfo/" + pair
        return self.get_request(self.url)

    def shift(self, postdata):
        # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
        """
                This is the primary data input into ShapeShift.

                data required:
                withdrawal     = the address for resulting coin to be sent to
                pair           = what coins are being exchanged in the form [input coin]_[output coin]  ie btc_ltc
                returnAddress  = (Optional) address to return deposit to if anything goes wrong with exchange
                destTag        = (Optional) Destination tag that you want appended to a Ripple payment to you
                rsAddress      = (Optional) For new NXT accounts to be funded, you supply this on NXT payment to you
                apiKey         = (Optional) Your affiliate PUBLIC KEY, for volume tracking, affiliate payments, split-shifts, etc.

                example data: {"withdrawal":"AAAAAAAAAAAAA", "pair":"btc_ltc", returnAddress:"BBBBBBBBBBB"}

                Success Output:
                    {
                        deposit: [Deposit Address (or memo field if input coin is BTS / BITUSD)],
                        depositType: [Deposit Type (input coin symbol)],
                        withdrawal: [Withdrawal Address], //-- will match address submitted in post
                        withdrawalType: [Withdrawal Type (output coin symbol)],
                        public: [NXT RS-Address pubkey (if input coin is NXT)],
                        xrpDestTag : [xrpDestTag (if input coin is XRP)],
                        apiPubKey: [public API attached to this shift, if one was given]
                    }
                """
        self.url = self.base_url + "/shift"
        return self.post_request(self.url, postdata)

    def send_amount(self, postdata):
        # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
        """
                This call allows you to request a fixed amount to be sent to the withdrawal address.
                You provide a withdrawal address and the amount you want sent to it.
                We return the amount to deposit and the address to deposit to.
                This allows you to use shapeshift as a payment mechanism.
                This call also allows you to request a quoted price on the amount of a transaction without a withdrawal address.
                //1. Send amount request

                Data required:

                    amount          = the amount to be sent to the withdrawal address
                    withdrawal      = the address for coin to be sent to
                    pair            = what coins are being exchanged in the form [input coin]_[output coin]  ie ltc_btc
                    returnAddress   = (Optional) address to return deposit to if anything goes wrong with exchange
                    destTag         = (Optional) Destination tag that you want appended to a Ripple payment to you
                    rsAddress       = (Optional) For new NXT accounts to be funded, supply this on NXT payment to you
                    apiKey          = (Optional) Your affiliate PUBLIC KEY, for volume tracking, affiliate payments, split-shifts, etc...

                example data {"amount":123, "withdrawal":"123ABC", "pair":"ltc_btc", returnAddress:"BBBBBBB"}  Success Output:

                {
                     success:
                      {
                        pair: [pair],
                        withdrawal: [Withdrawal Address], //-- will match address submitted in post
                        withdrawalAmount: [Withdrawal Amount], // Amount of the output coin you will receive
                        deposit: [Deposit Address (or memo field if input coin is BTS / BITUSD)],
                        depositAmount: [Deposit Amount], // Exact amount of input coin to send in
                        expiration: [timestamp when this will expire],
                        quotedRate: [the exchange rate to be honored]
                        apiPubKey: [public API attached to this shift, if one was given]
                      }
                }




                //2. Quoted Price request


                //Note :  This request will only return information about a quoted rate
                //         This request will NOT generate the deposit address.



                  Data required:

                    amount  = the amount to be sent to the withdrawal address
                    pair    = what coins are being exchanged in the form [input coin]_[output coin]  ie ltc_btc

                    example data {"amount":123, "pair":"ltc_btc"}


                  Success Output:

                    {
                         success:
                          {
                            pair: [pair],
                            withdrawalAmount: [Withdrawal Amount], // Amount of the output coin you will receive
                            depositAmount: [Deposit Amount], // Exact amount of input coin to send in
                            expiration: [timestamp when this will expire],
                            quotedRate: [the exchange rate to be honored]
                            minerFee: [miner fee for this transaction]
                          }
                    }
            """
        # noinspection SpellCheckingInspection
        self.url = self.base_url + "/sendamount"
        return self.post_request(self.url, postdata)

    def limit(self, pair):
        """
        Gets the current deposit limit set by Shapeshift.
        Amounts deposited over this limit will be sent to the return address if one was entered,
        otherwise the user will need to contact ShapeShift support to retrieve their coins.
        This is an estimate because a sudden market swing could move the limit.

        [pair] is any valid coin pair such as btc_ltc or ltc_btc

        Success Output:
            {
                "pair" : "btc_ltc",
                "limit" : "1.2345"
            }
        """
        self.url = self.base_url + "/limit/" + pair
        return self.get_request(self.url)

    def coin_list(self):
        """
        Allows anyone to get a list of all the currencies that Shapeshift currently supports at any given time. The list will include the name, symbol, availability status, and an icon link for each.
        Success Output:
            {
                "SYMBOL1" :
                    {
                        name: ["Currency Formal Name"],
                        symbol: <"SYMBOL1">,
                        image: ["https://shapeshift.io/images/coins/coinName.png"],
                         status: [available / unavailable]
                    }
                (one listing per supported currency)
            }

        The status can be either "available" or "unavailable". Sometimes coins become temporarily unavailable during updates or
        unexpected service issues.
        """
        # noinspection SpellCheckingInspection
        self.url = self.base_url + "/getcoins"
        return self.get_request(self.url)
