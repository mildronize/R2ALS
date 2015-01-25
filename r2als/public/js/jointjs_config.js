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

paper.scale(0.6, 0.6);

$(document).ready(function () {
    read(graph);

});

$('#perpendicularLinks').on('change', function() {
    paper.options.perpendicularLinks = $(this).is(':checked') ? true : false;
});

function GetURLElement(index) {
    var sPageURL = window.location.pathname;
    var sURLVariables = sPageURL.split('/');
    return sURLVariables[index]
}

//url: "./joint_semesters.json",
//apis/solution_generator/json
//http://127.0.0.1:6543/apis/solution_generator/json


function read(graph) {
    $.ajax({
      type: "GET",
      dataType: "json",
      cache: false,
      crossDomain : true,
      url: "http://127.0.0.1:6543/apis/solution_generator/"+GetURLElement(2),

      success: function (jsonString, textStatus, errorThrown) {
          graph.clear();
          console.log(jsonString);
          graph.fromJSON(jsonString);
        }
     });
    return graph
}
