// var jsonString = JSON.stringify(graph)
// ... send jsonString to the server,
// store it to the localStorage or do whatever you want
// ... later on
// graph.fromJSON(JSON.parse(jsonString))

var graph = new joint.dia.Graph;


var paper = new joint.dia.Paper({

    el: $('#paper'),
    width: 1200,
    height: 700,
    gridSize: 1,
    perpendicularLinks: false,
    model: graph,
    linkView: joint.dia.LinkView.extend({
    	pointerdblclick: function(evt, x, y) {
    	    // if (V(evt.target).hasClass('connection') || V(evt.target).hasClass('connection-wrap')) {
    		// this.addVertex({ x: x, y: y });
    	    // }
    	}
        }),
        interactive: function(cellView) {
    	if (cellView.model instanceof joint.dia.Link) {
                // Disable the default vertex add functionality on pointerdown.
    	    return { vertexAdd: false };
    	}
    	return true;
        }

});

$('#perpendicularLinks').on('change', function() {
    paper.options.perpendicularLinks = $(this).is(':checked') ? true : false;
});

var rect = new joint.shapes.basic.Rect({
    position: { x: 100, y: 30 },
    size: { width: 100, height: 30 },
    attrs: { rect: { fill: 'blue' }, text: { text: 'Subject', fill: 'white' } }
});

var rect2 = rect.clone();
rect2.translate(300);

var rect3 = rect.clone();
rect3.translate(300,100);

var rect4 = rect.clone();
rect4.translate(0,100);

var link = new joint.dia.Link({
    source: { id: rect.id },
    target: { id: rect2.id },
    router: { name: 'manhattan' },
    connector: { name: 'rounded' }
});

graph.addCells([rect, rect2, rect3, rect4, link]);
