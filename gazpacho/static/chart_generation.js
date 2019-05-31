var generate_line_graph = function(url){
  // function that generates a line graph from the
  d3.json(url).then(function (data) {
    console.log(data);
});
}
