from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)

# NOTE: disable this after launch.
CORS(app)


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
#DATA_FILE_PATH = "/~baokui/w209/static/data/all_merged_cl_ix_id_only.csv"
DATA_FILE_PATH = "/home/baokui/w209/static/project/data/all_merged_cl_ix_id_only.csv"
print("Start loading data at: " + DATA_FILE_PATH)
tradeDF = pd.read_csv(DATA_FILE_PATH)
print("Data loading finished! DF Shape: " + str(tradeDF.shape))

tradeDF_x_pCountry = tradeDF.groupby(["yr", "rgCode", "rtCode", "cmdCode"], as_index=False).sum()
tradeDF_x_rCountry = tradeDF.groupby(["yr", "rgCode", "ptCode", "cmdCode"], as_index=False).sum()
tradeDF_x_yr = tradeDF.groupby(["rgCode", "rtCode", "ptCode", "cmdCode"], as_index=False).sum()
tradeDF_x_cmdCode = tradeDF.groupby(["yr", "rgCode", "rtCode", "ptCode"], as_index=False).sum()
tradeDF_x_rgCode = tradeDF.groupby(["yr", "rtCode", "ptCode", 'cmdCode'], as_index=False).sum()
print("tradeDF_x_pCountry shape: " + str(tradeDF_x_pCountry.shape))
print("tradeDF_x_rCountry shape: " + str(tradeDF_x_rCountry.shape))
print("tradeDF_x_yr shape: " + str(tradeDF_x_yr.shape))
print("tradeDF_x_cmdCode shape: " + str(tradeDF_x_cmdCode.shape))
print("tradeDF_x_rgCode shape: " + str(tradeDF_x_rgCode.shape))

#tradeDF = None 

# Filter the data frame with following parameters.
#   - beginYear, first year in year range.
#   - endYear, last year in year range.
#   - rCountryId, the reporting country id, can be 'all'.
#   - pCountryId, the partner country id, can be 'all'.
#   - commodityId, the 2-digit id of the commodity, can be 'all'
#
# Those URL parameters must be explicitly provided.
#
# Parameter:
#   - request_dim, the requested dimention, could be 'Year', 'rCountry', 'pCountry', 'Commodity', 'tradeType'
#
# Returns [filteredDF, error-message]
def getFilteredDF(request_dim):
    # Get request parameters.
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

    # Find the best data set to use, this will make it run 3x~40X faster.
    if pCountryId == 'all' and request_dim != 'pCountry':
        target_df = tradeDF_x_pCountry
    elif rCountryId == 'all' and request_dim != 'rCountry':
        target_df = tradeDF_x_rCountry
    elif commodityId == 'all' and request_dim != 'Commodity':
        target_df = tradeDF_x_cmdCode
    elif beginYear <= 1988 and endYear >= 2019 and request_dim != 'Year':
        target_df = tradeDF_x_yr
    elif tradetype == 'all' and request_dim != 'tradeType':
        target_df = tradeDF_x_rgCode
    else:
        target_df = tradeDF


    selected = ((target_df.yr >= int(beginYear)) & (target_df.yr <= int(endYear)))
    if rCountryId != "all":
        print("not all in rCountry")
        selected = selected & (target_df.rtCode == int(rCountryId))
    if pCountryId != "all":
        print("not all in pCountry") 
        selected = selected & (target_df.ptCode == int(pCountryId)) 
    if commodityId != "all":
        print("not all in cmd")
        selected = selected & (target_df.cmdCode == int(commodityId)) 
    if tradeType != "all":
        print("not all in tradeType")
        selected = selected & (target_df.rgCode == int(tradeType)) 

    return [target_df[selected], 
            "OK-" + beginYear + "#" + endYear + "#" + rCountryId + "#" + pCountryId + "#" + commodityId]


# Convert '{ k1: v1, k2: v2, ...}' to [{key:k1, value:v1}, {key:k2, value:v2}, ...]'
def convertToArray(dict):
    result = []
    for k, v in dict.items():
        result.append({'key': k, 'value': v})
    return json.dumps(result)


@app.route('/project/ByYear')
def ByYear():
    (df, err_msg) = getFilteredDF('Year') 
    print(err_msg + " ### " + str(df.shape))
    if df is not None:
        df_dict = df[["yr", "TradeValue"]].groupby(["yr"]).sum()["TradeValue"]
        return convertToArray(df_dict)
    else:    
        return err_msg   


@app.route('/project/ByCommodity')
def ByCommodity():
    (df, err_msg) = getFilteredDF('Commodity') 
    if df is not None:
        df_dict = df[["cmdCode", "TradeValue"]].groupby(["cmdCode"]).sum()["TradeValue"]
        return convertToArray(df_dict)
    else:    
        return err_msg    

@app.route('/project/ByRCountry')
def ByRCountry():
    (df, err_msg) = getFilteredDF('rCountry') 
    if df is not None:
        df_dict = df[["rtCode", "TradeValue"]].groupby(["rtCode"]).sum()["TradeValue"]
        return convertToArray(df_dict)
    else:    
        return err_msg   

@app.route('/project/ByPCountry')
def ByPCountry():
    (df, err_msg) = getFilteredDF('pCountry') 
    if df is not None:
        df_dict = df[["ptCode", "TradeValue"]].groupby(["ptCode"]).sum()["TradeValue"]
        return convertToArray(df_dict)  
    else:    
        return err_msg    

@app.route("/project")
def w209_project():
    return render_template("project/index.html")

#############################################################
# A1 below this
#############################################################

@app.route("/old/")
def w209_old():
    file="about9.jpg"
    return render_template("w209.html",file=file)
    #return render_template("index.html",file=file)

@app.route("/")
def w209():
    file="about9.jpg"
    #return render_template("w209.html",file=file)
    return render_template("index.html",file=file)


if __name__ == "__main__":
    app.run()
