<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Cluster and Cloud Computing</title>

    <!-- Bootstrap core CSS -->
    <link href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="../static/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="//cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

    <!-- Custom styles for this template -->
    <link href="../static/css/carousel.css" rel="stylesheet">
  </head>
<!-- NAVBAR
================================================== -->
  <body>
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
                <li class="active"><a href="/">Present</a></li>
                <li><a href="/description">Description</a></li>
                <li><a href="/reference">Reference</a></li>
              </ul>
            </div>
          </div>
        </nav>

      </div>
    </div>


    <!-- Carousel
    ================================================== -->
    <div id="myCarousel" class="carousel slide" data-ride="carousel">
      <!-- Indicators -->
      <ol class="carousel-indicators">
        <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
        <li data-target="#myCarousel" data-slide-to="1"></li>
        <li data-target="#myCarousel" data-slide-to="2"></li>
        <li data-target="#myCarousel" data-slide-to="3"></li>
      </ol>
      <div class="carousel-inner" role="listbox">
        <div class="item active">
          <img class="first-slide" src="../static/images/movie.png" alt="First slide">
          <div class="container">
            <div class="carousel-caption">
              <h1>Mining multiple patterns of Melbourne tweets regarding movie</h1>
              <p><a class="btn btn-lg btn-primary" href="/page/task1" role="button">Analytic Scenario 1</a></p>
            </div>
          </div>
        </div>
        <div class="item">
          <img class="second-slide" src="../static/images/income.png" alt="Second slide">
          <div class="container">
            <div class="carousel-caption">
              <h1>Mining the patterns between sentiment and household income</h1>
              <p><a class="btn btn-lg btn-primary" href="/page/task2" role="button">Analytic Scenario 2</a></p>
            </div>
          </div>
        </div>
        <div class="item">
          <img class="third-slide" src="../static/images/twitter.png" alt="Third slide">
          <div class="container">
            <div class="carousel-caption">
              <h1>Discussions of topic preference and active twitters</h1>
              <p><a class="btn btn-lg btn-primary" href="/page/task3" role="button">Analytic Scenario 3</a></p>
            </div>
          </div>
        </div>
        <div class="item">
          <img class="fourth-slide" src="../static/images/time.png" alt="Fourth slide">
          <div class="container">
            <div class="carousel-caption">
              <h1>Mining the time based sentiment pattern of Melbourne twitters </h1>
              <p><a class="btn btn-lg btn-primary" href="/page/task4" role="button">Analytic Scenario 4</a></p>
            </div>
          </div>
        </div>
 
      </div>
      <a class="left carousel-control" href="#myCarousel" role="button" data-slide="prev">
        <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
        <span class="sr-only">Previous</span>
      </a>
      <a class="right carousel-control" href="#myCarousel" role="button" data-slide="next">
        <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
        <span class="sr-only">Next</span>
      </a>
    </div><!-- /.carousel -->


    <!-- Marketing messaging and featurettes
    ================================================== -->
    <!-- Wrap the rest of the page in another container to center all the content. -->

    <div class="container marketing">

      <!-- START THE FEATURETTES -->

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">Mining multiple patterns of Melbourne tweets regarding movie</h2>
          <p class="lead">For people in Melbourne, what attitude do they hold towards some popular movie of 2015 and 2016? Do tweets regarding movie have some relationship with IMDb rating?</p>
			  <p><a class="btn btn-lg btn-default" href="/page/task1" role="button">Details</a></p>
        </div>
        <div class="col-md-5">
          <img class="featurette-image img-responsive center-block" src="../static/images/movie2.png" alt="Generic placeholder image" height="500" width="500">
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">Mining the patterns between sentiment and household income</h2>
          <p class="lead">For people in different suburbs, how does their sentiment vary with their income level changing? This task aims to discover the patterns between people’s sentiment and their income level.</p>
			  <p><a class="btn btn-lg btn-default" href="/page/task2" role="button">Details</a></p>
        </div>
        <div class="col-md-5">
          <img class="featurette-image img-responsive center-block" src="../static/images/income2.png" alt="Generic placeholder image" height="500" width="500">
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">Discussions of topic preference and active twitters</h2>
          <p class="lead">General description of the task, with painting the backgroud as a image best representing the task</p>
              <p><a class="btn btn-lg btn-default" href="/page/task3" role="button">Details</a></p>
        </div>
        <div class="col-md-5">
          <img class="featurette-image img-responsive center-block" src="../static/images/twitter2.png" alt="Generic placeholder image" height="500" width="500">
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">Mining the time based sentiment pattern of Melbourne twitters </h2>
          <p class="lead">Are Melburnians more happy on Sunday or Monday? Do they like to express their depression or anger after work?</p>
              <p><a class="btn btn-lg btn-default" href="/page/task4" role="button">Details</a></p>
        </div>
        <div class="col-md-5">
          <img class="featurette-image img-responsive center-block" src="../static/images/time2.png" alt="Generic placeholder image" height="500" width="500">
        </div>
      </div>


     <hr class="featurette-divider">

      <!-- /END THE FEATURETTES -->


      <!-- FOOTER -->
      <footer>
        <p class="pull-right"><a href="#">Back to top</a></p>
        <p>&copy; 2016 University of Melbourne &middot; <a href="#">Privacy</a> &middot; <a href="#">Terms</a></p>
      </footer>

    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
    <script src="//cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <!-- Just to make our placeholder images work. Don't actually copy the next line! -->
    <script src="../static/js/holder.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../static/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
