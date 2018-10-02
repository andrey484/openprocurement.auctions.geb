from openprocurement.auctions.geb.tests.fixtures.draft import (
    DRAFT_AUCTION_DEFAULT_FIXTURE_WITH_INVALID_AUCTON_PERIOD,
)


def phase_commit(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']

    next_status = 'active.rectification'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))
    entrypoint = '/auctions/{}?acc_token={}'.format(auction['data']['id'],
                                                    auction['access']['token'])
    response = test_case.app.patch_json(entrypoint, request_data)
    test_case.app.authorization = auth

    test_case.assertEqual(next_status, response.json['data']['status'])


def phase_commit_invalid_auctionPeriod(test_case):

    context = test_case.procedure.snapshot(fixture=DRAFT_AUCTION_DEFAULT_FIXTURE_WITH_INVALID_AUCTON_PERIOD)
    auction = context['auction']

    expected_http_status = '422 Unprocessable Entity'
    request_data = {"data": {'status': 'active.rectification'}}
    entrypoint = '/auctions/{}?acc_token={}'.format(auction['data']['id'], auction['access']['token'])

    auth = test_case.app.authorization
    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))
    response = test_case.app.patch_json(entrypoint, request_data, status=422)
    test_case.app.authorization = auth

    test_case.assertEqual(expected_http_status, response.status)


def invalid_phase_commit(test_case):
    context = test_case.procedure.snapshot()
    auction = context['auction']

    next_status = 'active.tendering'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(auction['access']['owner']), ''))

    entrypoint = '/auctions/{}?acc_token={}'.format(auction['data']['id'],
                                                    auction['access']['token'])
    test_case.app.patch_json(entrypoint, request_data, status=403)
    test_case.app.authorization = auth


def get_auction_dump(test_case):

    entrypoint = '/auctions/{}'.format(test_case.auction['data']['id'])
    response = test_case.app.get(entrypoint)
    filename = 'docs/source/tutorial/get_draft_auction.http'

    test_case.dump(response.request, response, filename)


def phase_commit_dump(test_case):
    next_status = 'active.rectification'
    request_data = {"data": {'status': next_status}}
    auth = test_case.app.authorization

    test_case.app.authorization = ('Basic', ('{}'.format(test_case.auction['access']['owner']), ''))
    entrypoint = '/auctions/{}?acc_token={}'.format(test_case.auction['data']['id'],
                                                    test_case.auction['access']['token'])
    response = test_case.app.patch_json(entrypoint, request_data)
    filename = 'docs/source/tutorial/phase_commit.http'
    test_case.dump(response.request, response, filename)
    test_case.app.authorization = auth
