from copy import deepcopy
from openprocurement.auctions.core.tests.base import (
    test_document_data
)
from openprocurement.auctions.core.utils import (
    get_now
)


def organizer_uploads_the_contract(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    document['documentType'] = 'contractSigned'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['contract_document_post'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    document = response.json['data']
    pattern = '/auctions/{}/contracts/{}/documents/{}'

    entrypoint = pattern.format(test_case.auction['data']['id'],
                                test_case.contract['data']['id'],
                                document['id']
                                )
    response = test_case.app.get(entrypoint)
    test_case.assertEqual('200 OK', response.status)


def organizer_uploads_the_contract_dump(test_case):
    expected_http_status = '201 Created'
    document = deepcopy(test_document_data)
    document['documentType'] = 'contractSigned'
    url = test_case.generate_docservice_url(),
    document['url'] = url[0]

    request_data = {'data': document}
    response = test_case.app.post_json(test_case.ENTRYPOINTS['contract_document_post'], request_data)
    test_case.assertEqual(expected_http_status, response.status)

    filename = 'docs/source/tutorial/active_awarded_organizer_contract_upload_contract.http'
    test_case.dump(response.request, response, filename)


def organizer_activate_contract(test_case):

    # check contract activation conditions

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data, status=403)
    test_case.assertEqual('403 Forbidden', response.status)

    now = get_now()
    request_data = {"data": {"dateSigned": now.isoformat()}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data)
    test_case.assertEqual('200 OK', response.status)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data)

    # check contract after activation
    response = test_case.app.get(test_case.ENTRYPOINTS['contract_get'])
    contract = response.json['data']

    # check contract status
    test_case.assertEqual(contract['status'], 'active')

    # check auction after contract activation
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'])
    contract = response.json['data']
    test_case.assertEqual(contract['status'], 'complete')


def organizer_activate_contract_dump(test_case):
    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data, status=403)
    test_case.assertEqual('403 Forbidden', response.status)

    now = get_now()
    request_data = {"data": {"dateSigned": now.isoformat()}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data)
    test_case.assertEqual('200 OK', response.status)

    filename = 'docs/source/tutorial/active_awarded_organizer_patch_contract_with_dateSigned.http'
    test_case.dump(response.request, response, filename)

    request_data = {"data": {"status": "active"}}
    response = test_case.app.patch_json(test_case.ENTRYPOINTS['contract_patch'], request_data)

    filename = 'docs/source/tutorial/active_awarded_organizer_activate_contract.http'
    test_case.dump(response.request, response, filename)

    # check contract after activation
    response = test_case.app.get(test_case.ENTRYPOINTS['contract_get'])
    contract = response.json['data']

    filename = 'docs/source/tutorial/active_awarded_contract_after_activation.http'
    test_case.dump(response.request, response, filename)

    # check auction after contract activation
    response = test_case.app.get(test_case.ENTRYPOINTS['auction_get'])
    contract = response.json['data']
    test_case.assertEqual(contract['status'], 'complete')

    filename = 'docs/source/tutorial/active_awarded_auction_after_contract_activation.http'
    test_case.dump(response.request, response, filename)

