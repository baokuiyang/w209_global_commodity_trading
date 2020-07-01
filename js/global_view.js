/* global d3, barChart, IdToCommodity, CommodityToId, IdToTradeType, TradeTypeToId, IdToCountry, CountryToId  */
d3.json("https://dream.ischool.berkeley.edu/~baokui/w209/project/ByRCountry?beginYear=0&endYear=2030&rCountryId=all&pCountryId=all&commodityId=all&tradeType=all",
        function(err, data) {
            if (err) throw err;

            // Convert id to name.
            for (var i = 0; i < data.length; i++) {
                data[i].key = IdToCountry[data[i].key];
            }
            console.log(data);

            // Set up the SVG canvas.
            var width = 800,
                height = 500;

            var margin = ({ top: 30, right: 100, bottom: 50, left: 40 }),
                iwidth = width - margin.left - margin.right,
                iheight = height - margin.top - margin.bottom;

            var svg = d3.select("#GlobalViewChart")
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            var gDrawing = svg.append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // Set up Y axis, which is the flights of stairs climbed each month.
            var y = d3.scaleLinear()
                .domain([d3.extent(data, function(d) { return d.value; })[0] - 20,
                    d3.extent(data, function(d) { return d.value; })[1]
                ])
                .range([iheight, 0]);

            // Draw the bars.
            gDrawing.selectAll("rect")
                .data(data)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("width", function(d) { return 16; })
                .attr("height", function(d) { return iheight - y(d.value); })
                .style("fill", "green")
                .attr("transform",
                    function(d, i) { return "translate(" + (i * iwidth / 26 - 6) + "," + y(d.value) + ")"; })
                // Set up mouse events.
                .on("mouseover", function(d, i) {
                    console.log(d);
                    d3.select(this).transition().duration('50').attr('opacity', '0.85'); 
                })
                .on("mouseout", function(d, i) {
                    console.log("aaaaaa");
                    d3.select(this).transition().duration('50').attr('opacity', '1.0'); 
                }); 

    }
);    