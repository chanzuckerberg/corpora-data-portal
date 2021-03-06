import json
import typing

from backend.corpora.common.corpora_orm import CollectionVisibility, CollectionLinkType
from backend.corpora.common.entities import Collection
from tests.unit.backend.chalice.api_server.base_api_test import BaseAuthAPITest
from tests.unit.backend.fixtures.generate_data_mixin import GenerateDataMixin
from tests.unit.backend.chalice.api_server.mock_auth import get_auth_token


class TestPublish(GenerateDataMixin, BaseAuthAPITest):
    def verify_publish_collection(
        self, collection_id: str, dataset_ids: typing.List[str] = None, link_names: typing.List[str] = None
    ):
        path = f"/dp/v1/collections/{collection_id}/publish"
        headers = {"host": "localhost", "Content-Type": "application/json", "Cookie": get_auth_token(self.app)}
        response = self.app.post(path, headers)
        response.raise_for_status()
        self.assertEqual(202, response.status_code)
        self.assertDictEqual({"collection_uuid": collection_id, "visibility": "PUBLIC"}, json.loads(response.body))
        self.addCleanup(Collection.get([collection_id, "PUBLIC"]).delete)

        # cannot call twice
        response = self.app.post(path, headers)
        self.assertEqual(403, response.status_code)

        # check if the collection is listed
        path = "/dp/v1/collections"
        headers = {"host": "localhost", "Content-Type": "application/json"}
        response = self.app.get(path, headers)
        response.raise_for_status()
        ids = [col["id"] for col in json.loads(response.body)["collections"]]
        self.assertIn(collection_id, ids)

        # check get collection_uuid
        path = f"/dp/v1/collections/{collection_id}"
        headers = {"host": "localhost", "Content-Type": "application/json"}
        response = self.app.get(path, headers)
        response.raise_for_status()
        actual = json.loads(response.body)
        self.assertEqual("PUBLIC", actual["visibility"])
        self.assertEqual(collection_id, actual["id"])
        if dataset_ids:
            actual_datasets = [d["id"] for d in actual["datasets"]]
            self.assertListEqual(dataset_ids, actual_datasets)
        if link_names:
            actual_links = [link["link_name"] for link in actual["links"]]
            self.assertListEqual(link_names, actual_links)

    def test__OK(self):
        collection_id = self.generate_collection().id
        self.verify_publish_collection(collection_id)

    def test__with_datasets__OK(self):
        collection_id = self.generate_collection().id
        dataset_ids = [
            self.generate_dataset(
                collection_id=collection_id, collection_visibility=CollectionVisibility.PRIVATE.name
            ).id
        ]
        self.verify_publish_collection(collection_id, dataset_ids)

    def test__with_links__OK(self):
        collection = self.generate_collection(
            links=[
                {"link_name": "test_link", "link_type": CollectionLinkType.PROTOCOL, "link_url": "https://link.link"}
            ]
        )
        link_names = [link.link_name for link in collection.links]
        dataset_ids = [
            self.generate_dataset(
                collection_id=collection.id, collection_visibility=CollectionVisibility.PRIVATE.name
            ).id
        ]
        self.verify_publish_collection(collection.id, dataset_ids, link_names)

    def test__not_owner__403(self):
        collection_id = self.generate_collection(owner="someone_else").id
        path = f"/dp/v1/collections/{collection_id}/publish"
        headers = {"host": "localhost", "Content-Type": "application/json", "Cookie": get_auth_token(self.app)}
        response = self.app.post(path, headers)
        self.assertEqual(403, response.status_code)

    def test__bad_uuid__403(self):
        collection_id = "bad_uuid"
        path = f"/dp/v1/collections/{collection_id}/publish"
        headers = {"host": "localhost", "Content-Type": "application/json", "Cookie": get_auth_token(self.app)}
        response = self.app.post(path, headers)
        self.assertEqual(403, response.status_code)
