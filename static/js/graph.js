
// console.log('aw bitch',d3.select('getReq'))
var graphSelection = d3.select("#getReq").append("svg")
    .attr("width", document.body.clientWidth)
    .attr("height", document.body.clientHeight)
    .call(d3.behavior.zoom().scaleExtent([0.5, 4]).on("zoom", function () {
        graphSelection.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
    })).append("g");

var c20 = d3.scale.category20b();

d3.json("graphStats", function (dataset) {
    document.getElementById("node_count").innerHTML = "Node Count: " + dataset.node_count;
    document.getElementById("edge_count").innerHTML = "Edge Count: " + dataset.edge_count;
    document.getElementById("diameter").innerHTML = "Diameter: " + dataset.diameter;
    document.getElementById("average_path_length").innerHTML = "Average Path Length: " + dataset.average_path_length;
    document.getElementById("global_clustering_coefficient").innerHTML = "Global Clustering Coefficient: " + dataset.global_clustering_coefficient;
});


// load data nto arrays from email.json
d3.json("graph", function (dataset) {
    var users = dataset.users,
        edges = dataset.edges;

    var force = d3.layout.force().size([document.body.clientWidth, document.body.clientHeight]).nodes(users).links(edges).gravity(1).charge(-7000).linkDistance(200);

    var edge = graphSelection.selectAll(".link").data(edges).enter().append("line").attr("stroke-width", function (d) { return Math.pow(d.weight, 1 / 3) * 1.1 > 10 ? Math.pow(d.weight, 1 / 3) * 1.1 : 1 }).attr("stroke-opacity", function (d) { return Math.log(d.weight) > 5 ? 1 : 0.2 }).attr("class", "link").on("click", function () {
        d3.select(this).attr("stroke-opacity", function (d) { return Math.log(d.weight) > 5 ? 1 : 0 }).on("click", function (d) {
            firstId = d.source.id
            secondId = d.target.id

            firstPersonName = firstId > secondId ? users[secondId].name : users[firstId].name;
            secondPersonName = firstId < secondId ? users[secondId].name : users[firstId].name;


            $('.carousel').carousel(2);
            document.getElementById('iframe').setAttribute('src', "edge?source=" + Math.min(firstId, secondId) + '&target=' + Math.max(firstId, secondId) + '&sourceName=' + firstPersonName + "&targetName=" + secondPersonName)
        });
    }).on("mouseover", function () {
        d3.select(this).transition()
            .duration(50).attr("stroke-width", 10).attr("stroke-opacity", 1)

    }).on("mouseout", function () {
        d3.select(this).transition()
            .duration(200).attr("stroke-width", function (d) { return Math.pow(d.weight, 1 / 3) * 1.1 > 10 ? Math.pow(d.weight, 1 / 3) * 1.1 : 0.5 })

    }); //can be dragged; //making it part of the class link


    var nodes = graphSelection.selectAll(".node").data(users).enter().append("g").attr("class", "nodes").call(force.drag)
        .on("mouseover", function (d) {
            d3.json("details?link=" + d.id, function (details) {
                // alert(JSON.stringify(details))
                document.getElementById("name").innerHTML = "Email: " + details.name;
                document.getElementById("weight").innerHTML = "Weight: " + details.weight;
                document.getElementById("neighbour_count").innerHTML = "Neighbour Count: " + details.neighbours;
                document.getElementById("clustering_coefficient").innerHTML = "Local Clustering Coefficient: " + details.clustering_coefficient;
                document.getElementById("eccentricity").innerHTML = "Eccentricity: " + details.eccentricity;
                document.getElementById("average_path_distance").innerHTML = "Average Path Distance: " + details.average_path_distance;
                document.getElementById("page_rank").innerHTML = "Page Rank: " + details.page_rank;
            });
        })
        .on("dblclick", function (d) {

            nodeId = d.id
            console.log(nodeId, d.id);
            $('.carousel').carousel(2);
            document.getElementById('iframe').setAttribute('src', "node?id=" + nodeId + '&nodeName=' + d.name)


        })

    colour_index = 0;
    var circle = nodes.append("circle").attr("r", function (d) { return Math.pow(d.contact, 1 / 2.5) }).attr("fill", function (_) { colour_index++; return c20(colour_index % 20); })
        .on("mouseover", function (d) {
            d3.select(this).transition()
                .duration(500).attr("r", function (d) { return Math.pow(d.contact, 1 / 2.5) * 1.5 });

        }).on("mouseout", function () {
            d3.select(this).transition()
                .duration(500).attr("r", function (d) { return Math.pow(d.contact, 1 / 2.5) })

        });


    var label = nodes.append("text").attr("dx", 12).attr("dy", "0.75em").style("fill", "white").attr("font-size", function (d) { return Math.log(d.contact) * 2 }).text(function (d) { return d.name; });

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

