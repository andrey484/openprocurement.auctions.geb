from openprocurement.api.migration import (
    BaseMigrationsRunner,
    BaseMigrationStep,
    MigrationResourcesDTO,
    AliasesInfoDTO
)

PACKAGE_ALIASES = {
    'openprocurement.auctions.geb': ['landlease']
}


def migrate_cancellations_document_of_tender(auction):
    changed = False
    for cancellation in auction.get('cancellations', []):
        for document in cancellation.get('documents', []):
            if document['documentOf'] == 'cancellation':
                document.update({
                    'documentOf': 'auction'
                })
                changed = True
    return changed


class GebMigrationRunner(BaseMigrationsRunner):

    SCHEMA_VERSION = 1
    SCHEMA_DOC = 'openprocurement_auctions_dgf_schema'


class DocumentOfCancellationsStep(BaseMigrationStep):

    def setUp(self):
        self.view = 'auctions/all'
        self.procurement_method_types = self.resources.aliases_info.get_package_aliases('openprocurement.auctions.geb')

    def migrate_document(self, auction):
        if auction['procurementMethodType'] in self.procurement_method_types:
            changed = migrate_cancellations_document_of_tender(auction)
            return auction if changed else None
        return None


MIGRATION_STEPS = (DocumentOfCancellationsStep, )


def migrate(db):
    aliases_info_dto = AliasesInfoDTO(PACKAGE_ALIASES)
    migration_resource_dto = MigrationResourcesDTO(db, aliases_info_dto)

    runner = GebMigrationRunner(migration_resource_dto)
    runner.migrate(MIGRATION_STEPS)
