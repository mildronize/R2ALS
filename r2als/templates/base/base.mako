<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="keywords" content="<%block name='keywords'></%block>" />
	<meta name="description" content="<%block name='description'></%block>" />
    <title><%block name="title">Welcome to Pumbaa community</%block></title>
    <!--<script src="/public/components/jquery/dist/jquery.js"></script>-->
    <link rel="stylesheet" href="/public/components/bootstrap-css/css/bootstrap.min.css">
	<link rel="stylesheet" href="/public/components/bootstrap-css/css/bootstrap-theme.min.css">
	<script src="/public/components/bootstrap-css/js/bootstrap.min.js"></script>

	
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

    <%block name="addition_header"></%block>
</head>

<body>
${next.body()}
<%block name="addition_footer"></%block>
</body>

</html>
