import datetime
import os
from unittest import TestCase

from webpub_manifest_parser.odl.parsers import ODLDocumentParserFactory
from webpub_manifest_parser.opds2.ast import OPDS2FeedMetadata
from webpub_manifest_parser.opds2.registry import OPDS2LinkRelationsRegistry
from webpub_manifest_parser.utils import first_or_default


class ODLParserTest(TestCase):
    def test(self):
        # Arrange
        parser_factory = ODLDocumentParserFactory()
        parser = parser_factory.create()
        input_file_path = os.path.join(
            os.path.dirname(__file__), "../../files/odl/feed.json"
        )

        # Act
        feed = parser.parse_file(input_file_path)

        # Assert
        self.assertIsInstance(feed.metadata, OPDS2FeedMetadata)
        self.assertEqual("Test", feed.metadata.title)

        self.assertEqual(1, len(feed.publications))
        [publication] = feed.publications

        self.assertEqual(1, len(publication.licenses))
        [license] = publication.licenses

        self.assertEqual(
            "urn:uuid:f7847120-fc6f-11e3-8158-56847afe9799", license.metadata.identifier
        )
        self.assertEqual(["application/epub+zip"], license.metadata.formats)

        self.assertEqual("USD", license.metadata.price.currency)
        self.assertEqual(7.99, license.metadata.price.value)

        self.assertEqual(
            datetime.datetime(2014, 4, 25, 10, 25, 21), license.metadata.created
        )

        self.assertEqual(30, license.metadata.terms.checkouts)
        self.assertEqual(
            datetime.datetime(2016, 4, 25, 10, 25, 21), license.metadata.terms.expires
        )
        self.assertEqual(10, license.metadata.terms.concurrency)
        self.assertEqual(5097600, license.metadata.terms.length)

        self.assertEqual(
            [
                u"application/vnd.adobe.adept+xml",
                u"application/vnd.readium.lcp.license.v1.0+json",
            ],
            license.metadata.protection.formats,
        )
        self.assertEqual(6, license.metadata.protection.devices)
        self.assertEqual(False, license.metadata.protection.copy_allowed)
        self.assertEqual(False, license.metadata.protection.print_allowed)
        self.assertEqual(False, license.metadata.protection.tts_allowed)

        self.assertEqual(2, len(license.links))
        borrow_link = first_or_default(
            license.links.get_by_rel(OPDS2LinkRelationsRegistry.BORROW.key)
        )
        self.assertEqual(
            "application/vnd.readium.license.status.v1.0+json", borrow_link.type
        )

        self_link = first_or_default(
            license.links.get_by_rel(OPDS2LinkRelationsRegistry.SELF.key)
        )
        self.assertEqual("application/vnd.odl.info+json", self_link.type)
