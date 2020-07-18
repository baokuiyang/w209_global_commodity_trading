/* global d3, barChart, IdToCommodity, CommodityToId, IdToTradeType, TradeTypeToId, IdToCountry, CountryToId  */


/* Add 'all' as an option */
function AddAllAsAnOption(selector) {
    var opt = document.createElement("option");
    opt.value = "all";
    opt.innerHTML = "ALL";
    selector.appendChild(opt);
} 

/* Populate Reporting Countries */
var s_reporting_country = document.getElementById("s_rcountry");
AddAllAsAnOption(s_reporting_country); 
Object.keys(CountryToId).sort().forEach(key => { 
    var opt = document.createElement("option");
    opt.value = CountryToId[key];
    opt.innerHTML = key; 
    s_reporting_country.appendChild(opt);
});
s_reporting_country.addEventListener("change", processSelectionEvent);
 
/* Populate Partner Countries */
var s_partner_country = document.getElementById("s_pcountry"); 
AddAllAsAnOption(s_partner_country);
Object.keys(CountryToId).sort().forEach(key => { 
    var opt = document.createElement("option");
    opt.value = CountryToId[key];
    opt.innerHTML = key; 
    s_partner_country.appendChild(opt);
});
s_partner_country.addEventListener("change", processSelectionEvent);

/* Populate Commodities */
var s_commodity = document.getElementById("s_commodity");
AddAllAsAnOption(s_commodity);
Object.keys(IdToCommodity).forEach(key => { 
    var opt = document.createElement("option");
    opt.value = key;
    opt.innerHTML = key + " - " +  IdToCommodity[key]; 
    s_commodity.appendChild(opt);
}); 
s_commodity.addEventListener("change", processSelectionEvent);

/* Populate trade type (import / export) */
var s_trade_type = document.getElementById("s_trade_type");
AddAllAsAnOption(s_trade_type);
Object.keys(IdToTradeType).forEach(key => { 
    var opt = document.createElement("option");
    opt.value = key;
    opt.innerHTML =IdToTradeType[key]; 
    s_trade_type.appendChild(opt);
});
s_trade_type.addEventListener("change", processSelectionEvent);


/* Get selected value, i.e., id of the country/commodity/trade-type */
function getSelectedValue(selector) {
    return selector.options[selector.selectedIndex].value;
}

/* Handle selection event. */
function processSelectionEvent(_) { 
    console.log(getSelectedValue(s_reporting_country));
    console.log(getSelectedValue(s_partner_country));
    console.log(getSelectedValue(s_commodity));  
    console.log(getSelectedValue(s_trade_type)); 

    drawCharts(getSelectedValue(s_reporting_country), 
               getSelectedValue(s_partner_country),
               getSelectedValue(s_commodity),
               getSelectedValue(s_trade_type)); 
}

/* Update the map with data-array */
function updateMap(the_map, data_array, id_map) {
    for (var i = 0; i < data_array.length; i++) {
        name = id_map[parseInt(data_array[i].N, 10)];
        value = parseInt(data_array[i].V, 10);
        if (the_map.hasOwnProperty(name)) {
            the_map[name] = the_map[name] + value;
        } else {
            the_map[name] = value;
        } 
    }
}

/* Convert map to key/value array sorted by value */
function mapToSortedArray(the_map) {
    var kv_a = [];
    var keys = Object.keys(the_map);
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        kv_a.push({"key": key, "value": the_map[key]}); 
    }
    return kv_a.sort(function(e1, e2) {return e2.value - e1.value;}).slice(0, 20); 
}
 
/* Draw Charts */
function drawCharts(reporting_country, partner_country, commodity, trade_type) {
    var api_domain = "https://dream.ischool.berkeley.edu/~baokui/w209/project/TopByYear";
    var parameters = "?rCountryId=" + reporting_country + "&pCountryId=" + partner_country + "&commodityId=" + commodity + "&tradeType=" + trade_type;
    var data_url = api_domain + parameters;
    console.log(data_url);

    // Timeline char for brush.
    var chartTimeline = timeSeriesChart()
        .width(1000)
        .x(function(d) { return parseInt(d.Y, 10); })
        .y(function(d) { return parseInt(d.V, 10) / 1000000000000; });

    d3.json(data_url, function(err, data) { 
        d3.select("#timeline")
            .datum(data)
            .call(chartTimeline);
        
        var colorScale = d3.scaleOrdinal(d3.schemeCategory20); 
        
        /* Update one horizontal bar chart. */
        function updateOneChart(div_id, top_data_map) { 
            var top_data_array = mapToSortedArray(top_data_map);
            
            //set up svg using margin conventions - we'll need plenty of room on the left for labels
            var margin = {
                top: 15,
                right: 45,
                bottom: 15,
                left: 150
            };

            var width = 400 - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

            // First clear the div        
            d3.select(div_id).selectAll("*").remove();

            var svg = d3.select(div_id).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var x = d3.scaleLinear()
                .range([0, width])
                .domain([0, d3.max(top_data_array, function (d) {
                    return d.value;
                })]);

            function cutLongKey(key){
                if (key.length > 25) {
                    return key.substring(0, 25) + "...";
                } else {
                    return key;
                }
            }
            var y = d3.scaleBand()
                .rangeRound([0, height])
                .padding(0.1)
                .domain(top_data_array.map(function (d) {
                    return cutLongKey(d.key);
                }));

            //make y axis to show bar names
            var yAxis = d3.axisLeft()
                .scale(y)
                //no tick marks
                .tickSize(0);

            var gy = svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)

            var bars = svg.selectAll(".bar")
                .data(top_data_array)
                .enter()
                .append("g");

            //append rects
            bars.append("rect")
                .attr("class", "rc_bar")
                .attr("y", function (d) { 
                    return y(cutLongKey(d.key));
                })
                .attr("height", y.bandwidth())
                .attr("x", 0)
                .attr("width", function (d) {
                    return x(d.value);
                })
                .style("fill", function(d) {return colorScale(cutLongKey(d.key));});

            //add a value label to the right of each bar
            bars.append("text")
                .attr("class", "label")
                //y position of the label is halfway down the bar
                .attr("y", function (d) {
                    return y(cutLongKey(d.key)) + y.bandwidth() / 2 + 4;
                })
                //x position is 3 pixels to the right of the bar
                .attr("x", function (d) {
                    return x(d.value) + 3;
                })
                .text(function (d) {
                    return d3.format("$.02")(d.value/1000000000000) + "T";;
                });
        }

        /* Update all bar charts with the specified year range */
        function updateAllChartsWithYearRange(begin_year, end_year) {
            var r_country_map = {};
            var p_country_map = {};
            var commodity_map = {};

            for (var index = 0; index < data.length; index++) {
                var yr = parseInt(data[index].Y);
                // Check Year is in selected range.
                if (yr >= begin_year && yr <= end_year) {
                    //console.log("Yr in range: " + yr);
                    
                    // Update reporting country map.
                    rt = data[index].RT;
                    updateMap(r_country_map, rt, IdToCountry);

                    // Update partner country map.
                    pt = data[index].PT; 
                    updateMap(p_country_map, pt, IdToCountry);

                    cmd = data[index].CMD;
                    updateMap(commodity_map, cmd, IdToCommodity);
                } 
            }
            console.log("updateAllChartsWithYearRange");
            updateOneChart("#top_r_cc", r_country_map);
            updateOneChart("#top_p_cc", p_country_map);
            updateOneChart("#top_cmd", commodity_map);  
        }

        chartTimeline.onBrushed(function(selected) {
            //console.log(selected);
            /* Add / substrct 0.1 to accomodate the boundaries */
            var begin_year = selected[0] - 0.1;
            var end_year = selected[1] + 0.1;
            updateAllChartsWithYearRange(begin_year, end_year);
            //console.log(begin_year + " $$$$ " + end_year);  
            
            /*
            console.log("R-country:");
            console.log(r_country_map);
            console.log("P-country:");
            console.log(p_country_map);
            console.log("commodity_map:");
            console.log(commodity_map);
            */  
        }); 

        // Init call to draw default charts */
        updateAllChartsWithYearRange(0, 2020);
    });  // end of d3.json(...)
}

/* Explicitly call it once to set up default view */
processSelectionEvent();



