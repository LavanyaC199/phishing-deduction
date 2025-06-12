<!DOCTYPE html>
<html>
<head>
  <title>Login Page</title>
   <!--Made with love by Mutiullah Samim -->
<style>   
html,body{
/*background-image: url('http://getwallpapers.com/wallpaper/full/a/5/d/544750.jpg');
*/
background-image: url('uploads/11.jpg');
background-size: cover;
background-repeat: no-repeat;
height: 100%;
font-family: 'Numans', sans-serif;
}

.container{
height: 100%;
align-content: center;
color: #37F3DF;

}

.card{
height: 370px;
margin-top: auto;
margin-bottom: auto;
width: 400px;
background-color: rgba(0,0,0,0.5) !important;
}

.social_icon span{
font-size: 60px;
margin-left: 10px;
color: #440A07 ;
}
</style>
<?php
include'header1.php';
?>
</head>
<body>
  <!--Bootsrap 4 CDN-->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    
    <!--Fontawesome CDN-->
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">

  <!--Custom styles-->
  <link rel="stylesheet" type="text/css" href="styles.css">

<div class="container">
  <div class="d-flex justify-content-center h-100">
    <div class="card">
      <div class="card-header">
        <h3>Anti Phishing</h3>
        
      </div>
      <div class="card-body">
        <form method="post" action="">
          <div class="input-group form-group">
            <div class="input-group-prepend">
              <span class="input-group-text"><i>url</i></span>
            </div>
            <input type="text" name="url" class="form-control" placeholder="enter the url">
            
          </div>
         <br>
          <div class="form-group">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="submit"  name="subm" value="Check url" class="btn float-login_btn">
          </div>
        </form>
      
      <?php

session_start();
include('conn.php');

if (isset($_POST['subm'])) 
{
  $url=$_POST['url'];
  $a=strlen($url);
  //echo $a;

  if ($a>54) {
    $label1=1;
    //echo $label1."j";
  }else{
    $label1=0;
  }

  // preg_match_all("/^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?(\w+[-_]+\w+)/i",$url,$domain);
  
  preg_match_all("/^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([-_]?\w+[-_]?\w+)/i",$url,$domain);

  //print_r($domain[1]);
  // echo(ctype_xdigit($domain[1]));
  foreach ($domain[1] as $testcase) {
  preg_match_all("/\w*[^-]*\w+/i",$testcase,$arr);
  //print_r($arr);
  $a=implode("", $arr[0]);
  //echo $a;
  
  if(ctype_xdigit($a)) {
     $label2=1;
     //echo $label2."m";     
    }else{
      $label2=0;
    }
    }
  //echo "<br>";
  $b=implode("", $domain[1]); 
    $c=preg_match_all("/([-]+\w+)/i",$b);
    //echo $c."n";
    if ($c==1) {
      $label3=1;
      //echo $label3."o";
    }else{
      $label3=0;
      //echo $label3."oo";
    }
    //echo "<br>";
    $sql="SELECT * FROM url_tb where url='$url'";
    //echo $url;
    //echo "<br>";
    $result=mysqli_query($conn,$sql);
    if (mysqli_num_rows($result)>0) {
      $label4=1;
      //echo $label4."z";
    }else{
      $label4=0;
    }
    //echo "<br>";
    //echo "<br>";
    if ($label1==1 && $label2==1) {
       echo "<b><i align-content='center'>url is phishing</i></b>";
       }elseif ($label1==1 && $label3==1) {
      echo "url is phishing";
     }elseif ($label1==1 && $label4==1) {
      echo "url is phishing";
     }elseif ($label2==1 && $label3==1) {
      echo "url is phishing";
     }elseif ($label2==1 && $label4==1) {
      echo "url is phishing";
     }elseif ($label3==1 && $label4==1) {
      echo "url is phishing";
     }
     else{
      echo "<b><i>url is not phishing</i></b>";
     }

}

?>
</div>

      <div class="card-footer">
        <div class="d-flex justify-content-center links">
          <a href="Logout.php">Logout</a>
        </div>
        <!-- <div class="d-flex justify-content-center">
          <a href="#">Forgot your password?</a>
        </div> -->
      </div>
    </div>
  </div>
</div>
</body>
</html>