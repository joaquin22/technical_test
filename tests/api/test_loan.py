import pytest

pytestmark = pytest.mark.django_db


class TestLoan:
    def test_create_loan(self, api_client, api_key) -> None:
        customer_dict = {"external_id": "customer_id_1", "score": 3000}
        header = {"Authorization": f"Api-Key {api_key }"}
        response = api_client().post(
            "/api/customer/",
            data=customer_dict,
            format="json",
            headers=header,
        )
        assert response.status_code == 201
        assert response.data["external_id"] == "customer_id_1"

        customer_id = response.data["external_id"]

        loan_dict = {
            "external_id": "loan_id_1",
            "customer_external_id": customer_id,
            "amount": 500,
            "outstanding": 500,
        }

        response = api_client().post(
            "/api/loan/",
            data=loan_dict,
            format="json",
            headers=header,
        )

        assert response.status_code == 201
        assert response.data["external_id"] == "loan_id_1"

    def test_activate_loan(self, api_client, api_key) -> None:
        customer_dict = {"external_id": "customer_id_1", "score": 3000}
        header = {"Authorization": f"Api-Key {api_key }"}
        response = api_client().post(
            "/api/customer/",
            data=customer_dict,
            format="json",
            headers=header,
        )
        assert response.status_code == 201
        assert response.data["external_id"] == "customer_id_1"

        customer_id = response.data["external_id"]

        loan_dict = {
            "external_id": "loan_id_1",
            "customer_external_id": customer_id,
            "amount": 500,
            "outstanding": 500,
        }

        response = api_client().post(
            "/api/loan/",
            data=loan_dict,
            format="json",
            headers=header,
        )

        assert response.status_code == 201
        assert response.data["external_id"] == "loan_id_1"

        loan_id = response.data["external_id"]

        response = api_client().post(
            f"/api/loan/{loan_id}/activate/",
            format="json",
            headers=header,
        )

        assert response.status_code == 200
        assert response.data["external_id"] == "loan_id_1"
        assert response.data["status"] == 2

    def test_get_loan_by_customer(self, api_client, api_key) -> None:
        customer_dict = {"external_id": "customer_id_1", "score": 3000}
        header = {"Authorization": f"Api-Key {api_key }"}
        response = api_client().post(
            "/api/customer/",
            data=customer_dict,
            format="json",
            headers=header,
        )
        assert response.status_code == 201
        assert response.data["external_id"] == "customer_id_1"

        customer_id = response.data["external_id"]

        loan_dict = {
            "external_id": "loan_id_1",
            "customer_external_id": customer_id,
            "amount": 500,
            "outstanding": 500,
        }

        response = api_client().post(
            "/api/loan/",
            data=loan_dict,
            format="json",
            headers=header,
        )

        assert response.status_code == 201
        assert response.data["external_id"] == "loan_id_1"

        response = api_client().get(
            f"/api/loan/{customer_id}/loan_by_customer/",
            format="json",
            headers=header,
        )

        assert response.status_code == 200
        assert response.data[0]["external_id"] == "loan_id_1"
        assert response.data[0]["customer_external_id"] == customer_id
        assert response.data[0]["amount"] == 500
        assert response.data[0]["outstanding"] == 500
        assert response.data[0]["status"] == 1
