<script>
$(document).ready(function(){

	var native_width = 0;
	var native_height = 0;

	//Now the mousemove function
	$(".magnify-1").mousemove(function(e){
		//When the user hovers on the image, the script will first calculate
		//the native dimensions if they do exist. Only after the native dimensions
		//are available, the script will show the zoomed version.
		if(!native_width && !native_height)
		{
			//This will create a new image object with the same image as that in .small
			//We cannot directly get the dimensions from .small because of the 
			//width specified to 200px in the html. To get the actual dimensions we have
			//created this image object.
			var image_object = new Image();
			image_object.src = $(".small-1").attr("src");
			
			//This code is wrapped in the .load function which is important.
			//width and height of the object would return 0 if accessed before the image gets loaded.
			native_width = image_object.width;
			native_height = image_object.height;
		}
		else
		{
			//x/y coordinates of the mouse
			//This is the position of .magnify with respect to the document.
			var magnify_offset = $(this).offset();
			//We will deduct the positions of .magnify from the mouse positions with
			//respect to the document to get the mouse positions with respect to the 
			//container(.magnify)
			var mx = e.pageX - magnify_offset.left;
			var my = e.pageY - magnify_offset.top;
			
			//Finally the code to fade out the glass if the mouse is outside the container
			if(mx < $(this).width() && my < $(this).height() && mx > 5 && my > 5 && mx<330 && my<300)
			{
				$(".large-1").fadeIn(100);
			}
			else
			{
				$(".large-1").fadeOut(100);
			}
			if($(".large-1").is(":visible"))
			{
				//The background position of .large will be changed according to the position
				//of the mouse over the .small image. So we will get the ratio of the pixel
				//under the mouse pointer with respect to the image and use that to position the 
				//large image inside the magnifying glass
				var rx = Math.round(mx/$(".small-1").width()*native_width - $(".large-1").width()/2)*-1;
				var ry = Math.round(my/$(".small-1").height()*native_height - $(".large-1").height()/2)*-1;
				var bgp = rx + "px " + ry + "px";
				
				//Time to move the magnifying glass with the mouse
				var px = mx - $(".large-1").width()/2;
				var py = my - $(".large-1").height()/2;
				//Now the glass moves with the mouse
				//The logic is to deduct half of the glass s width and height from the 
				//mouse coordinates to place it with its center at the mouse coordinates
				
				//If you hover on the image now, you should see the magnifying glass in action
				$(".large-1").css({left: px, top: py, backgroundPosition: bgp});
			}
		}
	})
	
// Second Image
//Now the mousemove function
	$(".magnify-2").mousemove(function(e){
		//When the user hovers on the image, the script will first calculate
		//the native dimensions if they do exist. Only after the native dimensions
		//are available, the script will show the zoomed version.
		if(!native_width && !native_height)
		{
			//This will create a new image object with the same image as that in .small
			//We cannot directly get the dimensions from .small because of the 
			//width specified to 200px in the html. To get the actual dimensions we have
			//created this image object.
			var image_object = new Image();
			image_object.src = $(".small-2").attr("src");
			
			//This code is wrapped in the .load function which is important.
			//width and height of the object would return 0 if accessed before 
			//the image gets loaded.
			native_width = image_object.width;
			native_height = image_object.height;
		}
		else
		{
			//x/y coordinates of the mouse
			//This is the position of .magnify with respect to the document.
			var magnify_offset = $(this).offset();
			//We will deduct the positions of .magnify from the mouse positions with
			//respect to the document to get the mouse positions with respect to the 
			//container(.magnify)
			var mx = e.pageX - magnify_offset.left;
			var my = e.pageY - magnify_offset.top;
			
			//Finally the code to fade out the glass if the mouse is outside the container
			if(mx < $(this).width() && my < $(this).height() && mx > 10 && my > 10 && mx<325 && my<200)
			{
				$(".large-2").fadeIn(100);
			}
			else
			{
				$(".large-2").fadeOut(100);
			}
			if($(".large-2").is(":visible"))
			{
				//The background position of .large will be changed according to the position
				//of the mouse over the .small image. So we will get the ratio of the pixel
				//under the mouse pointer with respect to the image and use that to position the 
				//large image inside the magnifying glass
				var rx = Math.round(mx/$(".small-2").width()*native_width - $(".large-2").width()/2)*-1;
				var ry = Math.round(my/$(".small-2").height()*native_height - $(".large-2").height()/2)*-1;
				var bgp = rx + "px " + ry + "px";
				
				//Time to move the magnifying glass with the mouse
				var px = mx - $(".large-2").width()/2;
				var py = my - $(".large-2").height()/2;
				//Now the glass moves with the mouse
				//The logic is to deduct half of the glass s width and height from the 
				//mouse coordinates to place it with its center at the mouse coordinates
				
				//If you hover on the image now, you should see the magnifying glass in action
				$(".large-2").css({left: px, top: py, backgroundPosition: bgp});
			}
		}
	})
})
</script>