import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.geb.tests.base import BaseWebTest
from openprocurement.auctions.geb.tests.fixtures.draft import AUCTION
from openprocurement.auctions.geb.tests.blanks.migration_blanks import migrate_cancellations_document_of
from openprocurement.auctions.geb.migration import GebMigrationRunner, DocumentOfCancellationsStep
from openprocurement.auctions.geb.tests.states import ProcedureMachine
from openprocurement.api.tests.fixtures.mocks import MigrationResourcesDTO_mock


class TestDocumentOfCancellationsMigration(BaseWebTest):
    test_document_data = {
        'title': 'auction_protocol.pdf',
        'hash': 'md5:' + '0' * 32,
        'format': 'application/msword',
        "description": "auction protocol",
        "documentType": 'auctionProtocol',
        "documentOf": "cancellation"
    }
    test_migrate_cancellations_document_of = snitch(migrate_cancellations_document_of)

    def setUp(self):
        super(TestDocumentOfCancellationsMigration, self).setUp()
        self.runner = GebMigrationRunner(
            MigrationResourcesDTO_mock(
                self.db, {'openprocurement.auctions.geb': ['landlease']}
            )
        )
        self.steps = (DocumentOfCancellationsStep, )

        procedure = ProcedureMachine()
        procedure.set_db_connector(self.db)
        procedure.toggle('create')

        context = procedure.snapshot(fixture=AUCTION, dump=False)

        self.ENTRYPOINTS = {'auction_post': '/auctions'}
        self.auction = context['auction']['data']
        self.auction_id = context['auction']['data']['_id']


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDocumentOfCancellationsMigration))


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
