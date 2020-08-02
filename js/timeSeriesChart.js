/* global d3 */
function timeSeriesChart() {
  var margin = {top: 20, right: 20, bottom: 20, left: 20},
    width = 1000,
    height = 150,
    xValue = function(d) { return int(d[0]); },
    yValue = function(d) { return int(d[1]); },
    xScale = d3.scaleLinear(),
    yScale = d3.scaleLinear(),
    area = d3.area().x(X).y1(Y),
    line = d3.line().x(X).y(Y),
    onBrushed = function () {};

  function chart(selection) {
    //console.log("In chart(): ");
    //console.log(selection);

    selection.each(function(data) {
      //console.log(data);

      // Convert data to standard representation greedily;
      // this is needed for nondeterministic accessors.
      data = data.map(function(d, i) {
        return [xValue.call(data, d, i), yValue.call(data, d, i)];
      });
      //console.log("after map:");
      //console.log(data);

      // Update the x-scale.
      xScale
          .domain(d3.extent(data, function(d) { return d[0]; }))
          .range([15, width - margin.left - margin.right]);

      // Update the y-scale.
      yScale
          .domain([0, d3.max(data, function(d) { return d[1]; })])
          .range([height - margin.top - margin.bottom, 0]);

      // Select the svg element, if it exists.
      var svg = d3.select(this).selectAll("svg").data([data]);

      // Otherwise, create the skeletal chart.
      var svgEnter = svg.enter().append("svg");
      var gEnter = svgEnter.append("g");
      gEnter.append("path").attr("class", "area");
      gEnter.append("path").attr("class", "line");
      gEnter.append("g").attr("class", "x axis");
      gEnter.append("g").attr("class", "y axis");  // Added
      gEnter.append("g").attr("class", "brush");
 
      // Update the outer dimensions.
      svg.merge(svgEnter).attr("width", width)
          .attr("height", height);

      // Update the inner dimensions.
      var g = svg.merge(svgEnter).select("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // Update the area path.
      g.select(".area")
          .attr("d", area.y0(yScale.range()[0]));

      // Update the line path.
      g.select(".line")
          .attr("d", line);

      // Update the x-axis.
      g.select(".x.axis")
          .attr("transform", "translate(0," + yScale.range()[0] + ")")
          .call(d3.axisBottom(xScale).ticks(34).tickFormat(d3.format("d")).tickSize(0, 0).tickPadding(10));

      // Update the y-axis.
      g.select(".y.axis")
          .attr("transform", "translate(15," + 0 + ")") 
          .call(d3.axisLeft(yScale).ticks(4).tickFormat(function(d) { 
              if (d < 0.01 ) {
                  return d3.format("$.02")(d * 1000) + "B";
              }   
              return d3.format("$.02")(d) + "T";})
          );

      g.select(".brush").call(d3.brushX()
        .extent([
          [15, -10],
          [xScale.range()[1], yScale.range()[0] + 10]
        ])
        .on("brush", brushed)
        .on("start", brushStart)
      );
    });
  }

  function brushed() {
    if (!d3.event.sourceEvent)   return;// Only transition after input.
    if (!d3.event.selection)   return; // Ignore empty selections.
    var selection = d3.event.selection.map(xScale.invert); 
    onBrushed(selection);
  }

  function brushStart() {
     // Select the whole range to remove the filter.
     var selection = [xScale.invert(0), xScale.invert(width - margin.left - margin.right)]; 
     //console.log(xScale);
     onBrushed(selection); 
  }

  // The x-accessor for the path generator; xScale ∘ xValue.
  function X(d) {
    return xScale(d[0]);
  }

  // The y-accessor for the path generator; yScale ∘ yValue.
  function Y(d) {
    return yScale(d[1]);
  }

  chart.margin = function(_) {
    if (!arguments.length) return margin;
    margin = _;
    return chart;
  };

  chart.width = function(_) {
    if (!arguments.length) return width;
    width = _;
    return chart;
  };

  chart.height = function(_) {
    if (!arguments.length) return height;
    height = _;
    return chart;
  };

  chart.x = function(_) {
    if (!arguments.length) return xValue;
    xValue = _;
    return chart;
  };

  chart.y = function(_) {
    if (!arguments.length) return yValue;
    yValue = _;
    return chart;
  };

  chart.onBrushed = function(_) {
    if (!arguments.length) return onBrushed;
    onBrushed = _;
    return chart;
  };

  return chart;
}