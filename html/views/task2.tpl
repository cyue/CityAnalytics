<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
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
                <li><a href="/description">Description</a></li>
                <li><a href="/reference">Reference</a></li>
              </ul>
            </div>
          </div>
        </nav>

      </div>
</div>

<hr class="featurette-divider">


<div class="container">
  <div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>


<p></p>
  <div class="row">
  <div class="col-md-8 col-md-offset-2">

<div id="map"  style="width: 100%; height: 500px;"></div>
  </div>
</div>
    
    <script>
     
      

     $(function () {
    $.getJSON('/task2data1', function (data) {

      //var cat=[];
      var income=[];
      var sent=[];
      data.forEach(function(d){
        //cat.push(d['suburb']);
        income.push({'y':d['income'],'suburb':d['suburb']});
        sent.push({'y':d['avg_sentiment_score'],'suburb':d['suburb']});
      })
 $('#container').highcharts({
        title: {
            text: 'Sentiment and income comparison',
            x: -20 //center
        },
        xAxis: {
            tickInterval: 1
        },
        yAxis: [{
            title: {
                text: 'Income'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
         {
            title: {
                text: 'sentiment'
            },
            opposite: true
        }],


        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Income',
            data: income
        }, {
            name: 'Sentiment',
            data: sent,
            yAxis: 1
        }],

        tooltip: {
            useHTML: true,
            formatter: function() {

                return this.point.suburb+this.point.y;
            }
        },
    });
});
  });






      var map;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 10,
          center: {lat: -37.8, lng: 144.9}
        });

        // Load GeoJSON.
        map.data.loadGeoJson('/task2data');

        // Color each letter gray. Change the color when the isColorful property
        // is set to true.
          map.data.setStyle(function(feature) {
    
          color = feature.getProperty('color');
        
        return /** @type {google.maps.Data.StyleOptions} */({
          fillColor: color,
          fillOpacity:0.7,
          strokeColor: 'white',
          strokeWeight: 1
        });
      });
   



   var infowindow = new google.maps.InfoWindow({
  content:"Hello World!"
  });

  map.data.addListener('click', function(event) {

    var suburb=event.feature.getProperty('suburb');
    var sent=event.feature.getProperty('sent');
    infowindow.setContent(suburb+": "+sent);

    infowindow.setPosition(event.latLng);
    infowindow.open(map);
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

  </body>
