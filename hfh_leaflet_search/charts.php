<!DOCTYPE html>
<html lang="en">
<head>
	<title>HFHN|Portal</title>
	  <link rel="stylesheet" href="css/bootstrap.min.css"/>
	  
	  <script src="js/jquery-1.11.1.min.js"></script>
	  <script src="js/bootstrap.min.js"></script>

        <script src="js/highcharts.js"></script>
        <script src="js/highcharts-more.js"></script>





     <script type="text/javascript">
$(function () {
        $('#container1').highcharts({
            title: {
                text: 'Beneficiary Count by Ward',
                x: -20 //center
            },
			chart: {
                        type: 'spline'
                    },
            subtitle: {
                text: 'Beneficiaries distribution in each ward',
                x: -20
            },
            xAxis: {
                categories: ['Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6','Ward 7', 'Ward 8', 'Ward 9']
            },
            yAxis: {
                title: {
                    text: 'Number of families'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: ''
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'Beneficiary',
                data: [26, 42, 29, 76, 77, 34, 41, 107, 107]
            }
			]
        });
    });
		
						
//------------------------------------chart 2
$(function () {
    $('#container2').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Damages on houses'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: 'Damages',
            colorByPoint: true,
            data: [{
                name: 'Destruction(G5)',
                y: 79.97
            }, {
                name: 'Moderate Damage (G2)',
                y: 1.71
            }, {
                name: 'Negligible Slight Damage (G1)',
                y: 6.34
            }, {
                name: 'Sustainable to Heavy Damage (G3)',
                y: 2.74
            }, {
                name: 'Very Heavy Damage (G4)',
                y: 9.25
            }]
        }]
    });
});
		
		//------------------------------------chart 3
$(function () {
    $('#container3').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Current Residing Location'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: 'Residing Location',
            colorByPoint: true,
            data: [{
                name: 'Temporary Shelter',
                y: 65.07
            }, {
                name: 'Tent',
                y: 2.23
            }, {
                name: 'Farm House',
                y: 1.37
            }, {
                name: 'Not Shifted',
                y: 25.34
            }, {
                name: 'Others',
                y: 3.42
            }, {
                name: 'Relative\'s house',
                y: 2.57
            }]
        }]
    });
});
		
//------------------------------------chart 4

$(function () {
        $('#container4').highcharts({
            title: {
                text: 'Income-Expenditure-Loan',
                x: -20 //center
            },
			chart: {
                        type: 'column'
                    },
            subtitle: {
                text: '',
                x: -20
            },
            xAxis: {
                categories: ['Above 40k', 'Below 10k', 'Between 10k and 20k','Between 20k and 30k']
            },
            yAxis: {
                title: {
                    text: 'Number of families'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: ''
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'Monthly Income',
                data: [133, 256, 151, 42]
            },
			{
                name: 'Monthly Expenditure',
                data: [133, 255, 151, 42]
            },
			{
                name: 'Loan',
                data: [81,140,98,25]
            }
			]
        });
    });		
				

     </script>
	
</head>
<script>
	
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
        <li><a href="data_table.php">Table<span class="sr-only">(current)</span></a></li>
        <li class="active"><a href="charts.php">More...</a></li>
      </ul>
    
     
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
   <div class="container"> 
	<div class="row well">
		<div class="col-sm-12">
			<div id="container1" style="height: 300px; width: auto; margin: 0 auto"></div>
		</div>
	</div>	
	
	<div class="row well">
		<div class="col-sm-6">
			<div id="container2" style="height: 350px; width: auto; margin: 0 auto"></div>
		</div>
		<div class="col-sm-6">
			<div id="container3" style="height: 350px; width: auto; margin: 0 auto"></div>
		</div>
	</div>	
	
	
	
	
	<div class="row well">
		<div class="col-sm-12">
			<div id="container4" style="height: 300px; width: auto; margin: 0 auto"></div>
		</div>
	</div>	
	
</div>	
</body>
</html>
