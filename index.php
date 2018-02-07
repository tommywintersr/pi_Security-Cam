<html>

<?php 
	include("password_protect.php");
?>

<head>
    <title>Home Security Camera Settings</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	
	<style>

 img {
    display: block;
    margin: 0 auto;
}

</style>

<style>
.table1 {
    float: left;
    margin: 5px;
    padding: 15px;
    max-width: 300px;
    height: 300px;
    border: 1px solid black;
} 

a{
	font-size: 80%;
}
</style>
	
  </head>

    <body>
        <script src="http://cdn.pubnub.com/pubnub-3.16.4.min.js"></script>
        <link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css">
  		
		<div class="w3-container">
	<table class="table1" style="width:100%" class="w3-table-all w3-centered">
	<tr>
		<th>Cam Status</th> 
	</tr>
	
	<tr align="center">
	<td>
		<a href="http://192.168.1.68/FaceDetect/camFootage/">Gallery</a> &nbsp; &nbsp;
		<a href="http://192.168.1.68/FaceDetect/index.php?logout=1">Logout</a>
		</td>
		<td align="center">
	</tr>
		
	<tr>
		<td id="cam1" align="center">Loading...</td> 
		<td align="center">
		</td>
	  </tr>
	
	<tr>
		<td id="cam2" align="center">Loading...</td> 
		<td align="center">
		</td>
	  </tr>
	
	<tr>
		<td id="cam3" align="center">Loading...</td> 
		<td align="center">
		</td>
	  </tr>
	  
	  <tr>
		<td id="cam4" align="center"></td> 
		<td align="center">
		</td>
	  </tr>
		 
</table>
	</div>
	<br>
	<br>
		   
    </body>
</html>

<script> 
	pubnub = PUBNUB({
        publish_key : 'pub-c-64f02401-e3e9-4e9d-9842-209923bfd371',
        subscribe_key : 'sub-c-815f5228-b2f0-11e6-9ab5-0619f8945a4f'
    })
     
	var rec_channel = 'motion_detection';    

 var statuesArray = [1, 2, 3];
  var statue;
  
 	pubnub.subscribe({
    	channel  : rec_channel,
    	callback : function(text) { 
			
			var obj = null;
    		var obj = JSON.parse(text);
			console.log(obj);
			
			for(i = 0; i < statuesArray.length; i++){				
				statue = PUBNUB.$('cam' + statuesArray[i]);
				statue.innerHTML = "CAM: " + obj[ statuesArray[i] ];
				
			var pic = obj[4]
			var uri = "http://192.168.1.68/FaceDetect/" + pic;
			var res = encodeURI(uri);
			
			}	
		show_image(res, 276, 320,'Live Cam');
    	}
	});
 
	function show_image(src, width, height, alt) {
    var img = document.createElement("img");
    img.src = src;
    img.width = width;
    img.height = height;
    img.alt = alt;

    // This next line will just add it to the <body> tag
    //document.body.appendChild(img);
	document.getElementById("cam4").appendChild(img); 

}


</script>