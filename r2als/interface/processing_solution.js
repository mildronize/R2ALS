// var jsonString = JSON.stringify(graph)
// ... send jsonString to the server,
// store it to the localStorage or do whatever you want
// ... later on
// graph.fromJSON(JSON.parse(jsonString))

var graph = new joint.dia.Graph;

var paper = new joint.dia.Paper({

    el: $('#paper'),
    width: 1920,
    height: 1200,
    gridSize: 1,
    perpendicularLinks: false,
    model: graph,
    linkView: joint.dia.LinkView.extend({
    	pointerdblclick: function(evt, x, y) {
    	    if (V(evt.target).hasClass('connection') || V(evt.target).hasClass('connection-wrap')) {
    		this.addVertex({ x: x, y: y });
    	    }
    	}
        }),
        interactive: function(cellView) {
    	if (cellView.model instanceof joint.dia.Link) {
                // Disable the default vertex add functionality on pointerdown.
    	    // return { vertexAdd: false };
    	}
    	return true;
        }

});

paper.scale(0.8, 0.8);

$(document).ready(function () {
    read(graph);
});

$('#perpendicularLinks').on('change', function() {
    paper.options.perpendicularLinks = $(this).is(':checked') ? true : false;
});
//url: "./joint_semesters.json",
function read() {
    $.ajax({
      type: "GET",
      dataType: "json",
      cache: false,
      crossDomain : true,
      url: "./processing_solution.json",
      success: function (jsonString, textStatus, errorThrown) {
        graph.clear();
        graph.fromJSON(jsonString);
        console.log(jsonString)
        }
     });
    return graph
}
