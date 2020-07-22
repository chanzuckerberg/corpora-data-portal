import json
import unittest

from furl import furl

from backend.corpora.common.corpora_orm import ProjectStatus
from backend.corpora.common.entities import Project
from tests.unit.backend.chalice.api_server import BaseAPITest
from tests.unit.backend.utils import BogusProjectParams


class TestSubmission(BaseAPITest, unittest.TestCase):
    def test__list_submission__ok(self):
        path = "/v1/submission"
        headers = dict(host="localhost")
        expected_name = 'test submission'
        test_project = Project.create(**BogusProjectParams.get(name=expected_name, status=ProjectStatus.EDIT.name))

        expected_submission = {'id': test_project.id,
                               'name': expected_name,
                               'processing_state': 'IN_VALIDATION',
                               'validation_state': 'NOT_VALIDATED',
                               'owner_id': "test_user_id"
                               }
        test_url = furl(path=path)
        response = self.app.get(test_url.url, headers=headers)
        response.raise_for_status()
        actual_body = json.loads(response.body)
        actual_submission = actual_body["submissions"][0]
        self.assertEqual(expected_submission, actual_submission)

    def test__get_project_uuid__ok(self):
        """Verify the test project exists and the expected fields exist."""
        expected_body = {
            "attestation": {"needed": False, "tc_uri": "test_tc_uri"},
            "datasets": [
                {
                    "assay": "test_assay",
                    "assay_ontology": "test_assay_ontology",
                    "contributors": [
                        {
                            "email": "test_email",
                            "id": "test_contributor_id",
                            "institution": "test_institution",
                            "name": "test_contributor_name",
                        }
                    ],
                    "dataset_assets": [
                        {
                            "dataset_id": "test_dataset_id",
                            "filename": "test_filename",
                            "filetype": "H5AD",
                            "id": "test_dataset_artifact_id",
                            "s3_uri": "test_s3_uri",
                            "type": "ORIGINAL",
                            "user_submitted": True,
                        }
                    ],
                    "dataset_deployments": [
                        {
                            "dataset_id": "test_dataset_id",
                            "environment": "test",
                            "id": "test_deployment_directory_id",
                            "url": "test_url",
                        }
                    ],
                    "development_stage": "test_development_stage",
                    "development_stage_ontology": "test_development_stage_ontology",
                    "disease": "test_disease",
                    "disease_ontology": "test_disease_ontology",
                    "ethnicity": "test_ethnicity",
                    "ethnicity_ontology": "test_ethnicity_ontology",
                    "id": "test_dataset_id",
                    "name": "test_dataset_name",
                    "organism": "test_organism",
                    "organism_ontology": "test_organism_ontology",
                    "preprint_doi": {"title": "test_preprint_doi"},
                    "project_id": "test_project_id",
                    "project_status": "LIVE",
                    "publication_doi": {"title": "test_publication_doi"},
                    "revision": 0,
                    "sex": "test_sex",
                    "source_data_location": "test_source_data_location",
                    "tissue": "test_tissue",
                    "tissue_ontology": "test_tissue_ontology",
                }
            ],
            "description": "test_description",
            "id": "test_project_id",
            "links": [{"type": "RAW_DATA", "url": "test_url"}],
            "name": "test_project",
            "owner": {"email": "test_email", "id": "test_user_id", "name": "test_user", },  # noqa
            "processing_state": "NA",
            "s3_bucket_key": "test_s3_bucket",
            "status": "EDIT",
            "validation_state": "NOT_VALIDATED",
        }

        test_url = furl(path="/v1/project/test_project_id")
        response = self.app.get(test_url.url, headers=dict(host="localhost"))
        response.raise_for_status()
        actual_body = self.remove_timestamps(json.loads(response.body))
        actual_json_body = json.dumps(actual_body, sort_keys=True)
        expected_json_body = json.dumps(expected_body)
        self.assertEqual(actual_json_body, expected_json_body)

    @staticmethod
    def remove_timestamps(body: dict) -> dict:
        """
        A helper function to remove timestamps from the response body.
        :param body: The decoded json response body
        :return: The decode json response body with timestamps removed.
        """

        def _remove_timestamps(jrb):
            jrb.pop("created_at", None)
            jrb.pop("updated_at", None)
            for value in jrb.values():
                if isinstance(value, dict):
                    _remove_timestamps(value)
                elif isinstance(value, list):
                    for list_value in value:
                        _remove_timestamps(list_value)
            return jrb

        return _remove_timestamps(body)