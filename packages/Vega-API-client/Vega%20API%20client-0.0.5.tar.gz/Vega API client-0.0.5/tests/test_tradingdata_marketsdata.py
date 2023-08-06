import vegaapiclient as vac

from .fixtures import tradingdataGRPC, tradingdataREST  # noqa: F401


def test_MarketsData(tradingdataGRPC, tradingdataREST):  # noqa: F811
    g = tradingdataGRPC.MarketsData(vac.grpc.api.trading.MarketsDataResponse())
    r = tradingdataREST.MarketsData()

    # The order (of MarketData objects in the list) is not guaranteed.
    gIDs = set(md.market for md in g.marketsData)
    rIDs = set(md.market for md in r.marketsData)
    assert gIDs == rIDs
