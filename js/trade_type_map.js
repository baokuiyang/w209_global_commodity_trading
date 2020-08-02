const IdToTradeType = {
    1: "Import",
    2: "Export"
    /*3: "re-Export",
    4: "re-Import"*/
};


// Invert the map.
const TradeTypeToId = {};
Object.keys(IdToTradeType).forEach(key => {TradeTypeToId[IdToTradeType[key]] = key;});
