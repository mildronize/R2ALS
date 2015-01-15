<%!
	import json
	from r2als import models
%>
<%block name="addition_header">

	<style>
		#paper {
			width: 1920px;
			height: 1200px;
			background-color: #eee;
			border: 1px solid gray;
		}
		/*.block-pointer-events {
			pointer-events: none
		}*/
		.link-tools .tool-remove { display: none }
	</style>
	<link rel="stylesheet" type="text/css" href="/public/external_components/joint/joint.css" />
</%block>


<div class="text-center">
	<label>Perpendicular links</label><input type="checkbox" id="perpendicularLinks" />
	<div id="paper"></div>
</div>


<%block name="addition_footer">
	<script src="/public/external_components/jquery.js"></script>
	<script src="/public/external_components/lodash.js"></script>
	<script src="/public/external_components/backbone.js"></script>
	<script src="/public/external_components/joint/core.js"></script>
	<script src="/public/external_components/joint/vectorizer.js"></script>
	<script src="/public/external_components/joint/geometry.js"></script>
	<script src="/public/external_components/joint/joint.dia.graph.js"></script>
	<script src="/public/external_components/joint/joint.dia.cell.js"></script>
	<script src="/public/external_components/joint/joint.dia.element.js"></script>
	<script src="/public/external_components/joint/joint.dia.link.js"></script>
	<script src="/public/external_components/joint/joint.dia.paper.js"></script>
	<script src="/public/external_components/joint/plugins/joint.shapes.basic.js"></script>
	<script src="/public/external_components/joint/plugins/routers/joint.routers.orthogonal.js"></script>
	<script src="/public/external_components/joint/plugins/routers/joint.routers.manhattan.js"></script>
	<script src="/public/external_components/joint/plugins/routers/joint.routers.metro.js"></script>
	<script src="/public/external_components/joint/plugins/connectors/joint.connectors.normal.js"></script>
	<script src="/public/external_components/joint/plugins/connectors/joint.connectors.rounded.js"></script>
	<script src="/public/external_components/joint/plugins/connectors/joint.connectors.smooth.js"></script>

	<script src="/public/js/jointjs_config.js"></script>
</%block>

