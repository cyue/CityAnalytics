<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="../static/css/carousel.css" rel="stylesheet">


    <title>Data Layer: Dynamic Styling</title>
    <meta name="viewport" content="initial-scale=1.0">
    <meta charset="utf-8">
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
    
  </head>
  <body>
<!-- NAVBAR
================================================== -->
<div class="navbar-wrapper">
      <div class="container">

        <nav class="navbar navbar-inverse navbar-fixed-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">Home</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li><a href="/">Present</a></li>
                <li><a href="/page/description">Description</a></li>
                <li><a href="/page/reference">Reference</a></li>
              </ul>
            </div>
          </div>
        </nav>

      </div>
</div>

<hr class="featurette-divider">




    <div class="row">
  <div class="col-md-7">

<div id="map"  style="width: 100%; height: 600px;"></div>

  </div>
<div class="col-md-5">

<p id='suburb'>suburb</p>

<div class="row">
  <div class="col-md-6">
  <p><b>Top topics</b></p>
  <p></p>
<p id='topics'>topics</p>
  </div>
  <div class="col-md-6">
  <p><b>Top twitters</b></p>
  <p></p>
  <p id='twitters'>twitters</p>
  </div>
  </div>


  <div id='container'>
  	
  </div>
  </div>
</div>
    <script>
     
     $(function () {
    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Percentage of different languages in the suburb'
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
            name: 'languages',
            colorByPoint: true,
            data: [{
                name: 'en',
                y: 56.33
            }, {
                name: 'ch',
                y: 24.03,
                sliced: true,
                selected: true
            }, {
                name: 'fr',
                y: 10.38
            }]
        }]
    });
});






      var map;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 11,
          center: {lat: -37.8, lng: 144.9}
        });

        // Load GeoJSON.
        map.data.loadGeoJson('/task3data');

        // Color each letter gray. Change the color when the isColorful property
        // is set to true.
          map.data.setStyle(function(feature) {
    
          color = feature.getProperty('color');
        
        return /** @type {google.maps.Data.StyleOptions} */({
          fillColor: color,
          fillOpacity:0.1,
          strokeColor: color,
          strokeWeight: 1
        });
      });
   



 

  map.data.addListener('click', function(event) {

    //var suburb=event.feature.getProperty('suburb');
    
    //infowindow.setContent(suburb+": "+sent);
     
    document.getElementById('topics').innerHTML=event.feature.getProperty('topics');
    document.getElementById('twitters').innerHTML=event.feature.getProperty('twitters');
    document.getElementById('suburb').innerHTML=event.feature.getProperty('suburb');
    var chart = $('#container').highcharts();
    chart.series[0].setData(event.feature.getProperty('lan'));
    
     });

        
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key= AIzaSyBbIaBUcVGHz1npdnoic8kQy0n7hXG3fWg &callback=initMap">
    </script>

      <!-- FOOTER -->
      <footer>
        <p class="pull-right"><a href="#">Back to top</a></p>
        <p>&copy; 2016 University of Melbourne &middot; <a href="#">Privacy</a> &middot; <a href="#">Terms</a></p>
      </footer>
</div>



  </body>
</html>
