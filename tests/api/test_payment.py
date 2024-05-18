import pytest

pytestmark = pytest.mark.django_db


class TestPayment:
    def test_create_payment(self, api_client, api_key) -> None:
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

        payment_dict = {
            "external_id": "payment_id_1",
            "customer_external_id": customer_id,
            "payment_amount": 200,
        }

        response = api_client().post(
            "/api/payment/",
            data=payment_dict,
            format="json",
            headers=header,
        )

        assert response.status_code == 201
        assert response.data["external_id"] == "payment_id_1"
