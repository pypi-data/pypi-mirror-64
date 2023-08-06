import vegaapiclient as vac

from .fixtures import tradingdataGRPC, tradingdataREST  # noqa: F401


def test_MarketByID(tradingdataGRPC, tradingdataREST):  # noqa: F811
    markets = tradingdataGRPC.Markets(
        vac.grpc.api.trading.MarketsResponse()).markets
    assert len(markets) > 0
    marketID = markets[0].id

    marketGRPC = tradingdataGRPC.MarketByID(
        vac.grpc.api.trading.MarketByIDRequest(marketID=marketID))
    marketREST = tradingdataREST.MarketByID(marketID)

    assert marketGRPC.SerializeToString() == marketREST.SerializeToString()


def test_Markets(tradingdataGRPC, tradingdataREST):  # noqa: F811
    marketsGRPC = tradingdataGRPC.Markets(
        vac.grpc.api.trading.MarketsResponse())
    marketsREST = tradingdataREST.Markets()
    assert marketsGRPC.SerializeToString() == marketsREST.SerializeToString()
