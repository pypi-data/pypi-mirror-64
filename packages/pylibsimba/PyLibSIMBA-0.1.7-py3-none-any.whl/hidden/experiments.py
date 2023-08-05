import pprint

import requests

from pylibsimba import get_simba_instance
from pylibsimba.wallet import Wallet
from tests.examples import TestGlobals

test_globals = TestGlobals()


def startup():
    wallet = Wallet(None)
    wallet.generate_wallet('test1234')
    addr = wallet.get_address()

    test_globals.wallet = wallet

    simba = get_simba_instance(
        'https://api.simbachain.com/v1/libSimba-SimbaChat-Quorum/',
        wallet,
        '04d1729f7144873851a745d2ae85639f55c8e3de5aea626a2bcd0055c01ba6fc',
        '')
    test_globals.simba = simba


def get_called_method(page_number=None):
    startup()

    method_params = {
            'createdBy_exact': "PyLibSIMBA"
        }

    result_pages = test_globals.simba.get_method_transactions('createRoom', method_params)  # type: PagedResponse
    print("Number of results for transaction {}: {}".format('createRoom', result_pages.count()))
    print("Got data {}".format(result_pages.data()))


def get_contracts_for_org():
    startup()

    result_pages = test_globals.simba.send_transaction_request(
        'https://api.simbachain.com/v1/contract_designs/',
    )
    # print(result_pages.data())
    with open('output.json', 'w') as f1:
        f1.write(pprint.pformat(result_pages.data(), indent=4))

    if result_pages.next_page():
        pg_num = result_pages.next_page().split('?page=')[1]
        print(result_pages.next().data())
        with open('output_{}.json'.format(pg_num), 'w') as f1:
            f1.write(pprint.pformat(result_pages.next().data(), indent=4))


if __name__ == '__main__':
    get_contracts_for_org()


