

<!DOCTYPE html>
<html>
    <head>
        <title>HFHN|Portal</title>
        <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" rel="stylesheet">
        <meta http-equiv='content-type' content='text/html; charset=utf-8' />
        <meta name='viewport' content='initial-scale=1.0 maximum-scale=1.0'>
        <style type="text/css">
        	html, body, #map { height: 97.3%; width: 100%; margin: 0; padding: 0; }
			.navbar {margin-bottom: 0px;}
        </style>
    </head>
    <body>
<!--
	    <nav class="navbar navbar-default" style="border-bottom-color:#2c3e50">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
				<img src="img/hfhn_logo.png" style="height:50px; width:auto;">
            </div>
			<b><p class="navbar-text">HFHN-Portal</p> </b>
        </div>
    </nav>
-->
	<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
	  <img src="img/hfhn_logo.png" style="height:50px; width:auto;">
      <!--<a class="navbar-brand" href="#">HFHN</a>-->
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
	  <li class="active"><a href="index.php">Map<span class="sr-only">(current)</span></a></li>
        <li><a href="data_table.php">Table<span class="sr-only">(current)</span></a></li>
        <li><a href="charts.php">More...</a></li>
      </ul>
    
     
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
            
                <div id="map"></div>
    	

      <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/2.4.1/lodash.min.js"></script>
      <script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
      <script src="https://rawgit.com/calvinmetcalf/leaflet-ajax/master/dist/leaflet.ajax.min.js"></script>
	  
	  <!--lib for opening files-->
	  <link rel="stylesheet" href="http://makinacorpus.github.io/Leaflet.FileLayer/Font-Awesome/css/font-awesome.min.css"/>
	  <script src="http://makinacorpus.github.io/Leaflet.FileLayer/leaflet.filelayer.js"></script>
		<script src="http://makinacorpus.github.io/Leaflet.FileLayer/togeojson/togeojson.js"></script>
		
	 
	  <link rel="stylesheet" href="css/MarkerCluster.css" />
	  <link rel="stylesheet" href="css/MarkerCluster.Default.css" />
	   <script src='js/leaflet.markercluster-src.js'></script>
	  
      <script src='js/controls/search.js'></script>
      <script src='js/index.js'></script>
    </body>
</html>