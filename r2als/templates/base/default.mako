<%inherit file="/base/base.mako"/>
<%block name="keywords">CoE, PSU, Computer Engineering, Prince of Songkla University, Community</%block>
<%block name="description">This site is for people in CoE</%block>
<%include file="/base/navigator_bar.mako"/>
    <div class="container">
      <div class="jumbotron">
        <h1 style="font-style: italic;"><a href="#">Hello, pumbaa.CoE!</a></h1>
	  </div>

${next.body()}
<%include file="/base/footer.mako"/>
	</div>