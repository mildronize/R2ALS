<%inherit file="/base/default.mako"/>
<%!
	import json
	from r2als import models
%>

<%block name="addition_header">
<style type="text/css">
.reset-box-sizing,
.reset-box-sizing * {
  -webkit-box-sizing: content-box;
     -moz-box-sizing: content-box;
          box-sizing: content-box;
}
</style>

</%block>
Test data: ${test_text}
