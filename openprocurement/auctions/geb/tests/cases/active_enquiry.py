
# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.geb.tests.base import (
    BaseWebTest
)
from openprocurement.auctions.geb.tests.states import (
    ProcedureMachine
)
from openprocurement.auctions.geb.tests.blanks.mixins import (
    CancellationWorkFlowMixin,
    CancellationWorkFlowWithoutDSMixin,
    CancellationDocumentsWorkFlowMixin,
    CancellationDocumentsWorkFlowWithoutDSMixin,
    BaseAdministratorTestMixin
)
from openprocurement.auctions.geb.tests.fixtures.active_enquiry import (
    AUCTION_WITH_BIDS_WITH_CANCELLATION,
    AUCTION_WITH_BID_ACTIVE,
    AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT,
    AUCTION_WITH_BID_PENDING,
    AUCTION_WITH_BID_PENDING_WITH_DOCUMENT,
    AUCTION_WITH_CANCELLATION,
    AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS,
    AUCTION_WITH_OFFLINE_DOCUMENTS,
    AUCTION_WITH_DOCUMENTS,
    AUCTION_WITH_QUESTIONS
)

from openprocurement.auctions.geb.tests.blanks.active_enquiry import (
    auction_auction_get,
    auction_bid_post,
    auction_document_download,
    auction_document_patch,
    auction_document_post,
    auction_document_post_offline,
    auction_document_post_without_ds,
    auction_document_put,
    auction_document_put_offline,
    auction_document_put_without_ds,
    auction_patch,
    auction_question_post,
    bid_active_get_document,
    bid_active_patch_document,
    bid_delete_in_active_status,
    bid_delete_in_pending_status,
    bid_document_post,
    bid_document_post_without_ds,
    bid_document_put_without_ds,
    bid_get_in_active_status,
    bid_get_in_pending_status,
    bid_make_activate,
    bid_patch_in_active_status,
    bid_patch_in_pending_status,
    bid_pending_get_document,
    bid_pending_patch_document,
    item_question_post,
    question_get,
    question_patch
)
from openprocurement.auctions.geb.tests.blanks.cancellations import (
    cancellation_make_clean_bids
)


class ActiveEnquiryTest(BaseWebTest):
    docservice = True

    test_auction_bid_post = snitch(auction_bid_post)
    test_auction_question_post = snitch(auction_question_post)
    test_auction_auction_get = snitch(auction_auction_get)
    test_auction_document_post = snitch(auction_document_post)
    test_auction_document_post_offline = snitch(auction_document_post_offline)
    test_item_question_post = snitch(item_question_post)
    test_auction_patch = snitch(auction_patch)

    def setUp(self):
        super(ActiveEnquiryTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}
        entrypoints['patch_auction'] = '/auctions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                          self.auction['access']['token'])
        entrypoints['get_auction'] = '/auctions/{}'.format(self.auction['data']['id'])
        entrypoints['questions'] = '/auctions/{}/questions'.format(self.auction['data']['id'])
        entrypoints['bids'] = '/auctions/{}/bids'.format(self.auction['data']['id'])
        entrypoints['documents'] = '/auctions/{}/documents?acc_token={}'.format(self.auction['data']['id'],
                                                                                self.auction['access']['token'])
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryWithoutDSTest(BaseWebTest):
    docservice = False

    test_auction_document_post_without_ds = snitch(auction_document_post_without_ds)

    def setUp(self):
        super(ActiveEnquiryWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot()

        self.auction = context['auction']

        entrypoints = {}

        entrypoint_pattern = '/auctions/{}/documents?acc_token={}'
        entrypoints['documents'] = entrypoint_pattern.format(self.auction['data']['id'], self.auction['access']['token'])

        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryQuestionsTest(BaseWebTest):

    test_question_patch = snitch(question_patch)
    test_question_get = snitch(question_get)

    def setUp(self):
        super(ActiveEnquiryQuestionsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_QUESTIONS)

        self.auction = context['auction']
        self.question = context['questions'][0]

        entrypoints = {}

        entrypoints['patch_question'] = '/auctions/{}/questions/{}?acc_token={}'.format(self.auction['data']['id'],
                                                                                        self.question['data']['id'],
                                                                                        self.auction['access']['token'])

        entrypoints['get_question'] = '/auctions/{}/questions/{}'.format(self.auction['data']['id'],
                                                                         self.question['data']['id'])
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryBidsPendingTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)
    test_bid_make_activate = snitch(bid_make_activate)
    test_bid_document_post = snitch(bid_document_post)
    test_bid_delete_in_pending_status = snitch(bid_delete_in_pending_status)
    test_bid_get_in_pending_status = snitch(bid_get_in_pending_status)
    test_bid_patch_in_pending_status = snitch(bid_patch_in_pending_status)

    def setUp(self):
        super(ActiveEnquiryBidsPendingTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryBidsPendingWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_post_without_ds = snitch(bid_document_post_without_ds)

    def setUp(self):
        super(ActiveEnquiryBidsPendingWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryBidsActiveTest(BaseWebTest):
    docservice = True

    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)
    test_bid_document_post = snitch(bid_document_post)
    test_bid_delete_in_active_status = snitch(bid_delete_in_active_status)
    test_bid_get_in_active_status = snitch(bid_get_in_active_status)
    test_bid_patch_in_active_status = snitch(bid_patch_in_active_status)

    def setUp(self):
        super(ActiveEnquiryBidsActiveTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}?acc_token={token}'
        entrypoints['bid'] = pattern.format(auction=auction['data']['id'],
                                            bid=bid['data']['id'],
                                            token=bid['access']['token'])

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryBidsActiveWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_post_without_ds = snitch(bid_document_post_without_ds)

    def setUp(self):
        super(ActiveEnquiryBidsActiveWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE)

        auction = context['auction']
        bid = context['bids'][0]

        entrypoints = {}

        pattern = '/auctions/{auction}/bids/{bid}/documents?acc_token={token}'
        entrypoints['add_bid_document'] = pattern.format(auction=auction['data']['id'],
                                                         bid=bid['data']['id'],
                                                         token=bid['access']['token'])
        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryDocumentsTest(BaseWebTest):
    docservice = True

    test_auction_document_patch = snitch(auction_document_patch)
    test_auction_document_download = snitch(auction_document_download)
    test_auction_document_put = snitch(auction_document_put)

    def setUp(self):
        super(ActiveEnquiryDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}
        entrypoints['document_patch'] = '/auctions/{}/documents/{}?acc_token={}'.format(auction['data']['id'],
                                                                                        document['data']['id'],
                                                                                        auction['access']['token'])

        entrypoints['document_get'] = '/auctions/{}/documents/{}'.format(auction['data']['id'],
                                                                         document['data']['id'])
        entrypoints['document_put'] = entrypoints['document_patch']

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryOfflineDocumentsTest(BaseWebTest):
    docservice = True

    test_auction_document_put_offline = snitch(auction_document_put_offline)

    def setUp(self):
        super(ActiveEnquiryOfflineDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_OFFLINE_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}
        entrypoint_pattern = '/auctions/{}/documents/{}?acc_token={}'
        entrypoints['document_patch'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'], auction['access']['token'])

        entrypoint_pattern = '/auctions/{}/documents/{}'
        entrypoints['document_get'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'])

        entrypoints['document_put'] = entrypoints['document_patch']

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryDocumentWithoutDSTest(BaseWebTest):
    docservice = False

    test_auction_document_put_without_ds = snitch(auction_document_put_without_ds)

    def setUp(self):
        super(ActiveEnquiryDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enqiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_DOCUMENTS)

        auction = context['auction']
        document = context['documents'][0]

        entrypoints = {}

        entrypoint_pattern = '/auctions/{}/documents/{}?acc_token={}'
        entrypoints['document_patch'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'], auction['access']['token'])

        entrypoint_pattern = '/auctions/{}/documents/{}'
        entrypoints['document_get'] = entrypoint_pattern.format(auction['data']['id'], document['data']['id'])

        entrypoints['document_put'] = entrypoints['document_patch']

        self.document = document
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryCancellationsTest(BaseWebTest, CancellationWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveEnquiryCancellationsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION)

        auction = context['auction']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])

        entrypoints['patch_cancellation'] = '/auctions/{}/cancellations/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                cancellation['data']['id'],
                                                                                                auction['access']['token'])

        entrypoints['get_cancellation'] = '/auctions/{}/cancellations/{}'.format(auction['data']['id'],
                                                                                 cancellation['data']['id'])

        entrypoints['cancellation_document_post'] = '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                                                  cancellation['data']['id'],
                                                                                                                  auction['access']['token'])
        entrypoints['get_cancellations_listing'] = '/auctions/{}/cancellations'.format(auction['data']['id'])

        self.auction = auction
        self.cancellation = cancellation
        self.cancellations = context['cancellations']
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryCancellationsWithoutDSTest(BaseWebTest, CancellationWorkFlowWithoutDSMixin):

    def setUp(self):
        super(ActiveEnquiryCancellationsWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION)

        auction = context['auction']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoint_pattern = '/auctions/{}/cancellations/{}/documents?acc_token={}'
        entrypoints['cancellation_document_post'] = entrypoint_pattern.format(auction['data']['id'],
                                                                              cancellation['data']['id'],
                                                                              auction['access']['token'])

        self.auction = auction
        self.cancellation = cancellation
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryCancellationsWithBidsTest(BaseWebTest):
    test_cancellation_make_clean_bids = snitch(cancellation_make_clean_bids)

    def setUp(self):
        super(ActiveEnquiryCancellationsWithBidsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BIDS_WITH_CANCELLATION)

        auction = context['auction']
        bids = context['bids']
        cancellation = context['cancellations'][0]

        entrypoints = {}
        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_cancellation'] = '/auctions/{}/cancellations/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                cancellation['data']['id'],
                                                                                                auction['access']['token'])

        self.auction = auction
        self.bids = bids
        self.cancellation = cancellation
        self.cancellations = context['cancellations']
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryBidsPendingWithDocumentTest(BaseWebTest):

    test_bid_pending_get_document = snitch(bid_pending_get_document)
    test_bid_pending_patch_document = snitch(bid_pending_patch_document)

    def setUp(self):
        super(ActiveEnquiryBidsPendingWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryBidsPendingWithDocumentWithoutDSTest(BaseWebTest):
    docservice = False

    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveEnquiryBidsPendingWithDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_PENDING_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryBidsActiveWithDocumentTest(BaseWebTest):

    test_bid_active_get_document = snitch(bid_active_get_document)
    test_bid_active_patch_document = snitch(bid_active_patch_document)

    def setUp(self):
        super(ActiveEnquiryBidsActiveWithDocumentTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryBidsActiveWithDocumentWithoutDSTest(BaseWebTest):

    docservice = False

    test_bid_document_put_without_ds = snitch(bid_document_put_without_ds)

    def setUp(self):
        super(ActiveEnquiryBidsActiveWithDocumentWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_BID_ACTIVE_WITH_DOCUMENT)
        auction = context['auction']
        bid = context['bids'][0]
        bid_document = bid['data']['documents'][0]
        entrypoints = {}
        pattern = '/auctions/{}/bids/{}/documents/{}?acc_token={}'
        entrypoints['bid_document'] = pattern.format(auction['data']['id'],
                                                     bid['data']['id'],
                                                     bid_document['data']['id'],
                                                     bid['access']['token'])

        self.ENTRYPOINTS = entrypoints
        self.bid = bid
        self.auction = auction


class ActiveEnquiryCancellationsDocumentsTest(BaseWebTest, CancellationDocumentsWorkFlowMixin):
    docservice = True

    def setUp(self):
        super(ActiveEnquiryCancellationsDocumentsTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('draft')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS)

        auction = context['auction']
        cancellation = context['cancellations'][0]
        document = cancellation['data']['documents'][0]
        documents = cancellation['data']['documents']

        entrypoints = {}
        entrypoints['cancellation_document_listing'] = '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(auction['data']['id'],
                                                                                                                     cancellation['data']['id'],
                                                                                                                     auction['access']['token'])

        entrypoints['cancellation_document'] = '/auctions/{}/cancellations/{}/documents/{}?acc_token={}'.format(auction['data']['id'],
                                                                                                                cancellation['data']['id'],
                                                                                                                document['id'],
                                                                                                                auction['access']['token'])

        self.auction = auction
        self.cancellation = cancellation
        self.documents = documents
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryCancellationsDocumentsWithoutDSTest(BaseWebTest, CancellationDocumentsWorkFlowWithoutDSMixin):

    def setUp(self):
        super(ActiveEnquiryCancellationsDocumentsWithoutDSTest, self).setUp()

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.enquiry')
        context = procedure.snapshot(fixture=AUCTION_WITH_CANCELLATION_WITH_DOCUMENTS)

        auction = context['auction']
        cancellation = context['cancellations'][0]
        document = cancellation['data']['documents'][0]

        entrypoints = {}
        entrypoint_pattern = '/auctions/{}/cancellations/{}/documents/{}?acc_token={}'
        entrypoints['cancellation_document'] = entrypoint_pattern.format(auction['data']['id'],
                                                                         cancellation['data']['id'],
                                                                         document['id'],
                                                                         auction['access']['token'])

        self.auction = auction
        self.document = document
        self.ENTRYPOINTS = entrypoints


class ActiveEnquiryAdministratorTest(BaseWebTest, BaseAdministratorTestMixin):

    def setUp(self):
        super(ActiveEnquiryAdministratorTest, self).setUp()
        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('active.tendering')
        context = procedure.snapshot()

        auction = context['auction']

        entrypoints = {}

        entrypoints['get_auction'] = '/auctions/{}'.format(auction['data']['id'])
        entrypoints['patch_auction'] = '/auctions/{}'.format(auction['data']['id'])
        self.auction = auction
        self.ENTRYPOINTS = entrypoints


def suite():
    suite = unittest.TestSuite()
    # auction tests
    suite.addTest(unittest.makeSuite(ActiveEnquiryAdministratorTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryWithoutDSTest))
    # questions test
    suite.addTest(unittest.makeSuite(ActiveEnquiryQuestionsTest))
    # auction with documents tests
    suite.addTest(unittest.makeSuite(ActiveEnquiryDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryOfflineDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryDocumentWithoutDSTest))
    # cancellations tests
    suite.addTest(unittest.makeSuite(ActiveEnquiryCancellationsTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryCancellationsWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryCancellationsWithBidsTest))

    # cancellations with documents tests
    suite.addTest(unittest.makeSuite(ActiveEnquiryCancellationsDocumentsTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryCancellationsDocumentsWithoutDSTest))
    # bids tests
    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsPendingTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsActiveTest))

    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsPendingWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsActiveWithoutDSTest))
    # bids with documents tests
    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsPendingWithDocumentTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsActiveWithDocumentTest))

    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsPendingWithDocumentWithoutDSTest))
    suite.addTest(unittest.makeSuite(ActiveEnquiryBidsActiveWithDocumentWithoutDSTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
