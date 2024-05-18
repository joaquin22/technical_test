import pytest

pytestmark = pytest.mark.django_db


class TestCustomers:
    def test_create_customer(self, api_client, api_key) -> None:
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

    def test_get_customers(self, api_client, api_key) -> None:
        response = api_client().get(
            "/api/customer/",
            format="json",
            headers={"Authorization": f"Api-Key {api_key }"},
        )
        assert response.status_code == 200

    def test_get_customer(self, api_client, api_key) -> None:
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
        response = api_client().get(
            f"/api/customer/{customer_id}/",
            format="json",
            headers=header,
        )
        assert response.status_code == 200
        assert response.data["external_id"] == "customer_id_1"

    def test_get_balance(self, api_client, api_key) -> None:
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
        response = api_client().get(
            f"/api/customer/{customer_id}/balance/",
            format="json",
            headers=header,
        )
        assert response.status_code == 200
        assert response.data["external_id"] == "customer_id_1"
        assert response.data["score"] == 3000
        assert response.data["total_debt"] == 0
        assert response.data["available_amount"] == 3000
