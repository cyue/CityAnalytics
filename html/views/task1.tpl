<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="../static/css/carousel.css" rel="stylesheet">


    <title>Title</title>
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

<div class="row">
  <div class="col-md-8">

<div id="container1" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
  </div>
  <div  class="col-md-4">
  <!--<img src="/tmp/image.png" height="100" width="100">-->
  <div id='movie'>
  movie
</div>
    
  </div>
</div>


<div class="row">
  <div class="col-md-6">
<div id="container2" style="min-width: 310px; max-width: 600px; height: 400px; margin: 0 auto"></div>
  </div>
  <div class="col-md-6">

<div id="container3" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
  </div>
</div>



<script type="text/javascript">
    $(function () {

    $.getJSON('/task1data1', function (data) {


        var cat=[];
        var sent=[];

        data.forEach(function(d){
            cat.push(d['title']);
            sent.push({'y':d['sentiment'],'description':d['description']});
        });
       $('#container1').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Average Sentiment score of movies'
        },
        xAxis: {
            categories: cat
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Sentiment',
            data: sent,

        }],
        tooltip: {
            useHTML: true,
            formatter: function() {

                document.getElementById("movie").innerHTML ="<b>title:</b> "+this.point.description.title+"<br>"+
                "<b>rating:</b> "+this.point.description.rating+"<br>"+
                    "<b>genres:</b> "+this.point.description.genres+"<br>"+
                    "<b>outline:</b> "+this.point.description.outline+"<br>"+
                    "<b>director:</b> "+this.point.description.director+"<br>"+
                    "<b>runtimes:</b> "+this.point.description.runtimes+"<br>"+
                    "<b>cast:</b> "+this.point.description.cast+"<br>";
                return "<div style='width: 400px; white-space:normal;'>"+
                    "<b>rating:</b> "+this.point.description.rating+"<br>"+
                    "<b>genres:</b> "+this.point.description.genres+"<br>"+
                    "<b>outline:</b> "+this.point.description.outline+"<br>"+
                    "<b>director:</b> "+this.point.description.director+"<br>"+
                    "<b>runtimes:</b> "+this.point.description.runtimes+"<br>"+
                    "<b>cast:</b> "+this.point.description.cast+"<br>"+ "</div>"
            }
        },
        legend: {
            enabled: false
        }
    });
});

});


$(function () {
    $.getJSON('/task1data1', function (data) {
        var nData=[];
        var sumCount=0;
        data.forEach(function(d){
            sumCount+=d['total_tweet'];
        });
        data.forEach(function(d){
            nData.push({'name':d['title'],'y': d['total_tweet']/sumCount});
        });
    $('#container2').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Percentage of tweets for different movies'
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
            name: 'Brands',
            colorByPoint: true,
            data: nData
        }]
    });
});
});



$(function () {
    $.getJSON('/task1data2', function (data) {

         var cat=[];
         var sent=[];
         var tweet=[];
         data.forEach(function(d){
            cat.push(d['_id']);
            sent.push(d['sentiment']);
            tweet.push(d['tweets_per_movie']);
         });
$('#container3').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Sentiment and number of tweets for different ratings'
        },
        xAxis: {
            categories: cat
        },
        yAxis: [{
            
            title: {
                text: 'sentiment'
            }
        }, {
            title: {
                text: 'number of tweets'
            },
            opposite: true
        }],
        legend: {
            shadow: false
        },
        tooltip: {
            shared: true
        },
        plotOptions: {
            column: {
                grouping: false,
                shadow: false,
                borderWidth: 0
            }
        },
        series: [{
            name: 'sentiment',
            color: 'rgba(165,170,217,1)',
            data: sent,
            pointPadding: 0.3,
            pointPlacement: -0.2
        },  {
            name: 'tweets',
            color: 'rgba(248,161,63,1)',
            data: tweet,
            tooltip: {
                
            },
            pointPadding: 0.3,
            pointPlacement: 0.2,
            yAxis: 1
        }]
    });
});
});
</script>
      <!-- FOOTER -->
      <footer>
        <p class="pull-right"><a href="#">Back to top</a></p>
        <p>&copy; 2016 University of Melbourne &middot; <a href="#">Privacy</a> &middot; <a href="#">Terms</a></p>
      </footer>


</body>
</html>
