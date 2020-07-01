from flask import Flask
from flask import request
import pandas as pd

app = Flask(__name__)

# Load the global trading data, the file size is ~750MB with ~32M records.
#
# You may want to change the data path accordingly.
#
# Here's a few sample lines of the data:
# yr  rgCode  rtCode  ptCode  cmdCode TradeValue
# 2011    2   784 300 01  3138
# 2012    1   858 208 15  18652592
# 2007    2   231 894 92  348
# 
# More in here:
# https://github.com/baokuiyang/w209_global_commodity_trading/blob/master/data/sample_data_1000_records_id_only.csv
#
#DATA_FILE_PATH = "./sample_data_1000_records_id_only.csv"
DATA_FILE_PATH = "./all_merged_cl_ix_id_only.csv"
tradeDF = pd.read_csv(DATA_FILE_PATH)

# Filter the data frame with following parameters.
#   - beginYear, first year in year range.
#   - endYear, last year in year range.
#   - rCountryId, the reporting country id, can be 'all'.
#   - pCountryId, the partner country id, can be 'all'.
#   - commodityId, the 2-digit id of the commodity, can be 'all'.
#   - tradeType, 1:Import, 2:Export, can be 'all'.
#
# Those URL parameters must be explicitly provided.
#
# Returns [filteredDF, error-message]
def getFilteredDF():
    if not "beginYear" in request.args:
        return [None, "beginYear must be specified!"]
    beginYear = request.args.get('beginYear')

    if not "endYear" in request.args:
        return [None, "endYear must be specified!"]
    endYear = request.args.get('endYear')

    if not "rCountryId" in request.args:
        return [None, "rCountryId must be specified!"]
    rCountryId = request.args.get('rCountryId')
    
    if not "pCountryId" in request.args:
        return [None, "pCountryId must be specified!"]
    pCountryId = request.args.get('pCountryId')

    if not "commodityId" in request.args:
        return [None, "commodityId must be specified!"]
    commodityId = request.args.get('commodityId') 

    if not "tradeType" in request.args:
        return [None, "tradeType must be specified (1: Import, 2:Export)!"]
    tradeType = request.args.get('tradeType') 

    selected = ((tradeDF.yr >= int(beginYear)) & (tradeDF.yr <= int(endYear)))
    if rCountryId != "all":
        selected = selected & (tradeDF.rtCode == int(rCountryId))
    if pCountryId != "all":
        selected = selected & (tradeDF.ptCode == int(pCountryId)) 
    if commodityId != "all":
        selected = selected & (tradeDF.cmdCode == int(commodityId)) 
    if tradeType != "all":
        selected = selected & (tradeDF.rgCode == int(tradeType)) 

    return [tradeDF[selected], 
            "OK-" + beginYear + "#" + endYear + "#" + rCountryId + "#" + pCountryId + "#" + commodityId]


@app.route('/ByYear')
def ByYear():
    (df, err_msg) = getFilteredDF() 
    #print(err_msg + " ### " + str(df.shape))
    if df is not None:
        return df[["yr", "TradeValue"]].groupby(["yr"]).sum()["TradeValue"].to_json()
    else:    
        return err_msg   

@app.route('/ByCommodity')
def ByCommodity():
    (df, err_msg) = getFilteredDF() 
    if df is not None:
        return df[["cmdCode", "TradeValue"]].groupby(["cmdCode"]).sum()["TradeValue"].to_json()
    else:    
        return err_msg    

@app.route('/ByRCountry')
def ByRCountry():
    (df, err_msg) = getFilteredDF() 
    if df is not None:
        return df[["rtCode", "TradeValue"]].groupby(["rtCode"]).sum()["TradeValue"].to_json()
    else:    
        return err_msg   

@app.route('/ByPCountry')
def ByPCountry():
    (df, err_msg) = getFilteredDF() 
    if df is not None:
        return df[["ptCode", "TradeValue"]].groupby(["ptCode"]).sum()["TradeValue"].to_json()
    else:    
        return err_msg    

@app.route('/')
def hello_world():
    return str(tradeDF.describe())
