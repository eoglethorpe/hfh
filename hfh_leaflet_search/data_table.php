<!DOCTYPE html>
<html lang="en">
<head>
	<title>HFHN|Portal</title>
	  <link rel="stylesheet" href="css/bootstrap.min.css"/>
	  <link rel="stylesheet" href="css/jquery.dataTables.min.css"/>
	  <link rel="stylesheet" href="css/buttons.dataTables.min.css"/>
	  
	  <script src="js/jquery-1.11.1.min.js"></script>
	  <script src="js/bootstrap.min.js"></script>
	  <script src="js/jquery.dataTables.min.js"></script>
	  
	  <script src="https://cdn.datatables.net/buttons/1.2.2/js/dataTables.buttons.min.js"></script>
	  <script src="//cdn.datatables.net/buttons/1.2.2/js/buttons.flash.min.js"></script>
	  <script src="//cdnjs.cloudflare.com/ajax/libs/jszip/2.5.0/jszip.min.js"></script>
	  <script src="//cdn.rawgit.com/bpampuch/pdfmake/0.1.18/build/pdfmake.min.js"></script>
	  <script src="//cdn.rawgit.com/bpampuch/pdfmake/0.1.18/build/vfs_fonts.js"></script>
	  <script src="//cdn.datatables.net/buttons/1.2.2/js/buttons.html5.min.js"></script>
	  <script src="//cdn.datatables.net/buttons/1.2.2/js/buttons.print.min.js"></script>
</head>
<script>
	$(document).ready(function() {
    $('#example').DataTable( {
		dom: 'Blfrtip',
		buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "bProcessing": true,
        "bServerSide": true,
        "sAjaxSource": "data_table/data_table_lib.php"
    } );
} );
</script>
<body class="page-body">
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
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
	  <li><a href="index.php">Map<span class="sr-only">(current)</span></a></li>
        <li class="active"><a href="data_table.php">Table<span class="sr-only">(current)</span></a></li>
        <li><a href="charts.php">More...</a></li>
      </ul>
    
     
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
   <div class="container">        
<table id="example" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Name</th>
                <th>Registration No</th>
                <th>District</th>
                <th>VDC/Municipality</th>
                <th>Tole</th>
                <th>Damage Type</th>
            </tr>
        </thead>
        <tfoot>
            <tr>
                <th>Name</th>
                <th>Registration No</th>
                <th>District</th>
                <th>VDC/Municipality</th>
                <th>Tole</th>
                <th>Damage Type</th>
            </tr>
        </tfoot>
    </table>
</div>	
</body>
</html>
