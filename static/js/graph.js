
var graphSelection = d3.select("body").append("svg").attr("width", 4000).attr("height", 4000).append("g")
    .attr("transform", "translate(" + 100 + "," + 100 + ")");;




var c10 = d3.scale.category10();

// load data nto arrays from email.json
d3.json("j", function (dataset) {
    var users = dataset.users,
        edges = dataset.edges;

    console.log(users);
    console.log(dataset);

    var force = d3.layout.force().size([2500, 1500]).nodes(users).links(edges).gravity(1).charge(-9000).linkDistance(500);

    var edge = graphSelection.selectAll(".link").data(edges).enter().append("line").attr("stroke-width", function (d) { return Math.log(d.weight)>5? Math.log(d.weight)/2:1 }).attr("stroke-opacity", function (d) {  return Math.log(d.weight)>5? 1:0.2}).attr("class", "link"); //making it part of the class link

    var nodes = graphSelection.selectAll(".node").data(users).enter().append("g").attr("class", "nodes").call(force.drag); //can be dragged
    
    var label = nodes.append("text").attr("dx", 12).attr("dy", "0.75em").style("fill","white").attr("font-size", function (d) { return Math.log(d.contact)*2}).text(function (d) { return d.name; });

    colour_index = 0;
    var circle = nodes.append("circle").attr("r", function (d) { return Math.pow(d.contact,1/3) }).attr("fill", function (_) { colour_index++; return c10(colour_index % 10); });;


    force.on("tick", function () {

        nodes.attr("r", function (d) { return d.contact; })
            .attr("cx", function (d) { return d.x; })
            .attr("cy", function (d) { return d.y; });


        edge.attr("x1", function (d) { return d.source.x; });
        edge.attr("y1", function (d) { return d.source.y; })
        edge.attr("x2", function (d) { return d.target.x; })
        edge.attr("y2", function (d) { return d.target.y; });
        //Shift node a little
        nodes.attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });
    });

    force.start();

});
