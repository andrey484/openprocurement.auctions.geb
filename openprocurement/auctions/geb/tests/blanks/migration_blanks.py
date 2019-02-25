from uuid import uuid4


def migrate_cancellations_document_of(self):

    id = uuid4().hex
    self.auction['cancellations'] = [{
        "reason": "cancellation reason",
        "id": id,
        "documents": [self.test_document_data, self.test_document_data],
    }]

    self.auction.update(self.auction)
    self.db.save(self.auction)

    response = self.app.get('/auctions/{}/cancellations/{}/documents'.format(self.auction_id, id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 2)
    self.assertEqual(response.json['data'][0]['documentOf'], 'cancellation')
    self.assertEqual(response.json['data'][1]['documentOf'], 'cancellation')

    self.runner.migrate(self.steps)

    response = self.app.get('/auctions/{}/cancellations/{}/documents'.format(self.auction_id, id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 2)
    self.assertEqual(response.json['data'][0]['documentOf'], 'auction')
    self.assertEqual(response.json['data'][1]['documentOf'], 'auction')
