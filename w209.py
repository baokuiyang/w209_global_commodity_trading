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
DATA_FILE_PATH = "./all_merged_cl_ix.csv"
#DATA_FILE_PATH = "./all_merged_cl_ix_id_only.csv"

#DATA_FILE_PATH = "/home/baokui/w209/static/project/data/all_merged_cl_ix_id_only.csv"
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

def getFilteredDFNoOp():
    # Get request parameters.
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
    target_df = tradeDF 

    selected = (target_df.yr >= 0)
    if rCountryId != "all":
        # print("not all in rCountry")
        selected = selected & (target_df.rtCode == int(rCountryId))
    if pCountryId != "all":
        # print("not all in pCountry") 
        selected = selected & (target_df.ptCode == int(pCountryId)) 
    if commodityId != "all":
        # print("not all in cmd")
        selected = selected & (target_df.cmdCode == int(commodityId)) 
    if tradeType != "all":
        # print("not all in tradeType")
        selected = selected & (target_df.rgCode == int(tradeType)) 

    return [target_df[selected], 
            "OK-" + rCountryId + "#" + pCountryId + "#" + commodityId + "#" + tradeType]

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

# For each year, get the top values for the column of 'by_column'.
# Returns a map with key/value as the following:
# - Key: year
# - Value: top 30 reporting countries, partner countries, or commodities, depending on 'by_column'
def getYearMap(by_column, DF):
    tf = DF.groupby(["yr", by_column], as_index=False).agg({"TradeValue": sum})
    rtf = tf.sort_values(['yr', 'TradeValue'], ascending=False).groupby(["yr"]).head(30)
    # print(rtf.head(10))
    rtf_map = {}
    for index, row in rtf.iterrows():
        yr = row['yr']
        pair = { "N": str(row[by_column]), "V": str(row['TradeValue']) }
        if yr in rtf_map:
            rtf_map[yr].append(pair)
        else:
            rtf_map[yr] = [pair]
    return rtf_map

# Get trade value for each year.
def getYearVolume(DF):
    tf = DF.groupby(["yr"], as_index=False).agg({"TradeValue": sum}) 
    rtf_map = {}
    for index, row in tf.iterrows():
        yr = row['yr']
        value = str(row['TradeValue']) 
        rtf_map[yr] = value
    return rtf_map

# Get top rtCode, ptCode, cmdCode.
def findTop(DF):
    rt_map = getYearMap("rtCode", DF)
    pt_map = getYearMap("ptCode", DF)
    cmd_map = getYearMap("cmdCode", DF)
    yr_v_map = getYearVolume(DF)

    response = []
    for i in range(1998, 2020):
        yr = i

        value = "0"
        if i in yr_v_map:
            value = yr_v_map[yr]

        top_rt = []
        if i in rt_map:
            top_rt = rt_map[i]

        top_cmd = []
        if i in cmd_map:
            top_cmd = cmd_map[i]

        top_pt = []
        if i in pt_map:
            top_pt = pt_map[i]

        yr_rec = {"Y": str(yr), "V": value, "RT": top_rt, "PT": top_pt, "CMD": top_cmd}
        response.append(yr_rec)

    res_json = json.dumps(response)
    return res_json

# Cached results for TopByYear when:
# - rCountryId=all & pCountryId=all & commodityId=all & tradeType=all
# - rCountryId=all & pCountryId=all & commodityId=all & tradeType=1
# - rCountryId=all & pCountryId=all & commodityId=all & tradeType=2 
#
CACHE_ALL_ALL = findTop(tradeDF)
CACHE_ALL_IMPORT = findTop(tradeDF[tradeDF.rgCode == 1])
CACHE_ALL_EXPORT = findTop(tradeDF[tradeDF.rgCode == 2])

@app.route('/project/TopByYear')
def TopByYear():
    # Check the cached results first before caculating the results.
    if request.args.get('rCountryId') == 'all' and request.args.get('pCountryId') == 'all' and request.args.get('commodityId') == 'all': 
        if request.args.get('tradeType') == 'all':
            # print("cached ALL")
            return CACHE_ALL_ALL 
        elif request.args.get('tradeType') == '1':
            # print("cached IMPORT")
            return CACHE_ALL_IMPORT
        elif request.args.get('tradeType') == '2':
            # print("cached EXPORT")
            return CACHE_ALL_EXPORT
        else:
            pass
    else:
        [DF, err_msg] = getFilteredDFNoOp()
        if DF is None:
            return err_msg
    
    return findTop(DF)  

@app.route("/project")
def w209_project():
    return render_template("index.html")

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
