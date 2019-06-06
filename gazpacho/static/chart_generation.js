var svg = d3.select('svg');
var margin = {top: 50, right: 50, bottom: 50, left: 50}
  , width = svg.attr('width') - margin.left - margin.right // Use the window's width
  , height = svg.attr('height') - margin.top - margin.bottom; // Use the window's height

var generate_line_graph = function(url){
  // function that generates a line graph from the data provided
  d3.json(url).then(function (data) {
    console.log(data);

  // NOTE: THIS WAS ADAPTED FROM https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89

  var n = data.length;
  // set min and max
  var heart_rates = [];
  data.forEach((element) => {
    heart_rates.push(element.value);
  });

  // console.log(min,max);
  var xScale = d3.scaleLinear()
      .domain([0, n-1])
      .range([0, width]);

  var yScale = d3.scaleLinear()
      .domain([Math.min(...heart_rates), Math.max(...heart_rates)])
      .range([height, 0]);

    var x_axis = d3.axisBottom(xScale)
    .tickFormat(function(d, i) {
      console.log(d.datetime, d);
      return '';
    })
  // 7. d3's line generator
  var line = d3.line()
      .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
      .y(function(d) {
        console.log(yScale(d.value));
        return yScale(d.value); }) // set the y values for the line generator
      .curve(d3.curveMonotoneX); // apply smoothing to the line

  // 1. Add the SVG to the page and employ #2
  var svg = d3.select('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
    .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  // 3. Call the x axis in a group tag
  svg.append('g')
      .attr('class', 'x axis')
      .attr('transform', 'translate(0,' + height + ')')
      .call(x_axis); // Create an axis component with d3.axisBottom

  // 4. Call the y axis in a group tag
  svg.append('g')
      .attr('class', 'y axis')
      .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

  // 9. Append the path, bind the data, and call the line generator
  svg.append('path')
      .datum(data) // 10. Binds data to the line
      .attr('class', 'line') // Assign a class for styling
      .attr('d', line); // 11. Calls the line generator


  svg.append('text')
    .text('Heart Rate, in BPM')
    .attr('class', 'axis-title')
    .attr('x', -height/2 - 40)
    .attr('y', margin.left/2)
    .attr("transform", "rotate(-90)")



  // 12. Appends a circle for each datapoint
  svg.selectAll('.dot')
      .data(data)
    .enter().append('circle') // Uses the enter().append() method
      .attr('class', 'dot') // Assign a class for styling
      .attr('cx', function(d, i) { return xScale(i) })
      .attr('cy', function(d) { return yScale(d.value) })
      .attr('r', 5)
        .on('mouseover', function(d,i){
          // console.log(d, i);
          // focus.style('display', null);
          svg.append('text')
            .text(d.datetime)
            .attr('x', xScale(i))
            .attr('y', yScale(d.value))
            .attr('id', 'popup')
            .attr('transform', 'translate(-40,-10)');
          // console.log(xScale(i), yScale(d.value));
        })
        .on('mouseout', unhover);
});
};

var unhover = function(){
  // console.log(d3.mouse(this));
  d3.selectAll('#popup').remove();
};
