import pytest
from algokit_utils import (
    ApplicationClient,
    ApplicationSpecification,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient

from smart_contracts.junity import contract as junity_contract


@pytest.fixture(scope="session")
def junity_app_spec(algod_client: AlgodClient) -> ApplicationSpecification:
    return junity_contract.app.build(algod_client)


@pytest.fixture(scope="session")
def junity_client(
    algod_client: AlgodClient, junity_app_spec: ApplicationSpecification
) -> ApplicationClient:
    client = ApplicationClient(
        algod_client,
        app_spec=junity_app_spec,
        signer=get_localnet_default_account(algod_client),
        template_values={"UPDATABLE": 1, "DELETABLE": 1},
    )
    client.create()
    return client


def test_says_hello(junity_client: ApplicationClient) -> None:
    result = junity_client.call(junity_contract.hello, name="World")

    assert result.return_value == "Hello, World"
