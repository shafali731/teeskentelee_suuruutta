var unhover = function(){
  // console.log(d3.mouse(this));
  d3.selectAll('#popup').remove();
};

var draw_animation = function(svg, width, height){
  // makes a drawing-line animation
  // adapted from http://bl.ocks.org/markmarkoh/8700606
  var curtain = svg.append('rect')
    .attr('x', -1 * width)
    .attr('y', -1 * height)
    .attr('height', height + 10)
    .attr('width', width)
    .attr('class', 'curtain')
    .attr('transform', 'rotate(180)')
    .style('fill', '#ffffff');

  var t = svg.transition()
    .duration(1800);

  t.select('rect.curtain')
    .attr('width', 0);

  d3.select("#show_guideline").on("change", function(e) {
    curtain.attr("opacity", this.checked ? 0.75 : 1);
  });
};

var generate_heart_graph = function(url){
  var svg = d3.select('.heart-chart');
  var margin = {top: 50, right: 50, bottom: 50, left: 50}
    , width = svg.attr('width') - margin.left - margin.right // Use the window's width
    , height = svg.attr('height') - margin.top - margin.bottom; // Use the window's height

  // function that generates a line graph from the data provided
  d3.json(url).then(function (data) {
    // console.log(data);

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
      // console.log(d.dateTime, d);
      return '';
    })
  // 7. d3's line generator
  var line = d3.line()
      .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
      .y(function(d) {
        // console.log(yScale(d.value));
        return yScale(d.value); }) // set the y values for the line generator
      .curve(d3.curveMonotoneX); // apply smoothing to the line

  // 1. Add the SVG to the page and employ #2
  var svg = d3.select('.heart-chart')
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
            .text(d.dateTime)
            .attr('x', xScale(i))
            .attr('y', yScale(d.value))
            .attr('id', 'popup')
            .attr('transform', 'translate(-40,-10)');
          // console.log(xScale(i), yScale(d.value));
        })
        .on('mouseout', unhover);
  draw_animation(svg, width, height);
});
};

var generate_steps_graph = function(url){
  var svg = d3.select('.steps-chart');
  var margin = {top: 50, right: 50, bottom: 50, left: 50}
    , width = svg.attr('width') - margin.left - margin.right // Use the window's width
    , height = svg.attr('height') - margin.top - margin.bottom; // Use the window's height

  // function that generates a line graph from the data provided
  d3.json(url).then(function (data) {
    // console.log(data);

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
        // console.log(d.dateTime, d);
        return '';
      });

    var y_axis = d3.axisLeft(yScale)
      .tickFormat(function(d,i){
        // console.log(d / 100);
        return d/100 >= 10 ? d/1000 + 'k' : d;
      });

  // 7. d3's line generator
  var line = d3.line()
      .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
      .y(function(d) {
        // console.log(yScale(d.value));
        return yScale(d.value); }) // set the y values for the line generator
      .curve(d3.curveMonotoneX); // apply smoothing to the line

  // 1. Add the SVG to the page and employ #2
  var svg = d3.select('.steps-chart')
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
      .call(y_axis); // Create an axis component with d3.axisLeft

  // 9. Append the path, bind the data, and call the line generator
  svg.append('path')
      .datum(data) // 10. Binds data to the line
      .attr('class', 'line') // Assign a class for styling
      .attr('d', line); // 11. Calls the line generator


  svg.append('text')
    .text('Number of Steps Taken')
    .attr('class', 'axis-title')
    .attr('x', -height/2 - 60)
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
            .text(d.value + ', ' + d.dateTime)
            .attr('x', xScale(i))
            .attr('y', yScale(d.value))
            .attr('id', 'popup')
            .attr('transform', 'translate(-55,-10)');
          // console.log(xScale(i), yScale(d.value));
        })
        .on('mouseout', unhover);
  draw_animation(svg, width, height);
});
};

var generate_food_graph = function(url){
  var svg = d3.select('.food-chart');
  var margin = {top: 50, right: 50, bottom: 50, left: 50}
    , width = svg.attr('width') - margin.left - margin.right // Use the window's width
    , height = svg.attr('height') - margin.top - margin.bottom; // Use the window's height

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
      // console.log(d.dateTime, d);
      return '';
    })
  // 7. d3's line generator
  var line = d3.line()
      .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
      .y(function(d) {
        // console.log(yScale(d.value));
        return yScale(d.value); }) // set the y values for the line generator
      .curve(d3.curveMonotoneX); // apply smoothing to the line

  // 1. Add the SVG to the page and employ #2
  var svg = d3.select('.food-chart')
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
    .text('Calorie Consumption, in cal')
    .attr('class', 'axis-title')
    .attr('x', -height/2 - 80)
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
            .text(d.value + ', ' + d.dateTime)
            .attr('x', xScale(i))
            .attr('y', yScale(d.value))
            .attr('id', 'popup')
            .attr('transform', 'translate(-90,-10)');
          // console.log(xScale(i), yScale(d.value));
        })
        .on('mouseout', unhover);
  draw_animation(svg, width, height);
});
};
