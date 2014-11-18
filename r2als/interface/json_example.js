<!DOCTYPE html>
<html>
<head>
  <title>Server Data Graph</title>
  <link rel="stylesheet" type="text/css" href="../joint.css" />
  <script type="text/javascript" src="../joint.js"></script>
</head>
<body>
  <a onclick="save();" href="#">[Save]</a><a onclick="read();" href="#">[Cancel]</a>
  <div id="graph" class="graph"></div>


  <script type="text/javascript">

    var graph = new joint.dia.Graph();
    var paper = new joint.dia.Paper({
        el: $('#graph'),
        width: 1024,
        height: 400,
        gridSize: 10,
        model: graph});

    $(document).ready(function () {
      read(graph);
     });

    function read() {

    $.ajax({
      type: "GET",
      dataType: "json",
      cache: false,
      url: "./celldata.json",
      success: function (jsonString, textStatus, errorThrown) {
         graph.clear();
         graph.fromJSON(jsonString);
        }
     });
    }

  function save() {
     document.location = 'data:Application/octet-stream,' +
                         encodeURIComponent(JSON.stringify(graph.toJSON()));
    }
   </script>
 </body>
</html>

celldata.json looks like this:

{"cells":[{"type":"basic.Rect","position":{"x":210,"y":10},"size":{"width":175,"height":50},"angle":0,"id":1,"z":0,"attrs":{"rect":{"fill":"red","data-cell-id":1}}},{"type":"basic.Rect","position":{"x":410,"y":10},"size":{"width":175,"height":50},"angle":0,"id":2,"z":0,"attrs":{"rect":{"fill":"green","data-cell-id":2}}},{"type":"basic.Rect","position":{"x":10,"y":10},"size":{"width":175,"height":50},"angle":0,"id":3,"z":0,"attrs":{"rect":{"fill":"blue","data-cell-id":3}}}]}
