$(document).ready(function(){


	$(".magnify-1").mousemove(function(e){
		var $small = $(this).find(".small-1");
		var $large = $(this).find(".large-1");


		var native_width = $small[0].naturalWidth || $small.width();
		var native_height = $small[0].naturalHeight || $small.height();

		if(!native_width || !native_height) return;

		var magnify_offset = $(this).offset();
		var mx = e.pageX - magnify_offset.left;
		var my = e.pageY - magnify_offset.top;


		if(mx > 5 && my > 5 && mx < $(this).width() - 5 && my < $(this).height() - 5) {
			$large.fadeIn(100);
		} else {
			$large.fadeOut(100);
		}

		if($large.is(":visible")) {

			var rx = Math.round(mx / $small.width() * native_width - $large.width() / 2) * -1;
			var ry = Math.round(my / $small.height() * native_height - $large.height() / 2) * -1;
			var bgp = rx + "px " + ry + "px";


			var px = mx - $large.width() / 2;
			var py = my - $large.height() / 2;

			$large.css({left: px, top: py, backgroundPosition: bgp});
		}
	}).mouseleave(function(){
		$(this).find(".large-1").fadeOut(100);
	});


	$(".magnify-2").mousemove(function(e){
		var $small = $(this).find(".small-2");
		var $large = $(this).find(".large-2");


		var native_width = $small[0].naturalWidth || $small.width();
		var native_height = $small[0].naturalHeight || $small.height();

		if(!native_width || !native_height) return;

		var magnify_offset = $(this).offset();
		var mx = e.pageX - magnify_offset.left;
		var my = e.pageY - magnify_offset.top;


		if(mx > 5 && my > 5 && mx < $(this).width() - 5 && my < $(this).height() - 5) {
			$large.fadeIn(100);
		} else {
			$large.fadeOut(100);
		}

		if($large.is(":visible")) {

			var rx = Math.round(mx / $small.width() * native_width - $large.width() / 2) * -1;
			var ry = Math.round(my / $small.height() * native_height - $large.height() / 2) * -1;
			var bgp = rx + "px " + ry + "px";


			var px = mx - $large.width() / 2;
			var py = my - $large.height() / 2;

			$large.css({left: px, top: py, backgroundPosition: bgp});
		}
	}).mouseleave(function(){
		$(this).find(".large-2").fadeOut(100);
	});
});
