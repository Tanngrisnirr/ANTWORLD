<!-- jQuery 3.1.1 (single version, replaces 6 redundant versions - saves ~750KB) -->
<script src="js/jquery-3.1.1.min.js"></script>
<script src="js/jquery_1_3_easing.js"></script>  <!-- Animation easing -->
<script>
$(document).ready(function(){
	jQuery.easing.def = 'easeInOutQuint';
	$(".h2one").animate({left: '18%', opacity: '1.0',}, 1700);
	$(".h2two").delay(500);
	$(".h2two").animate({left: '18%', opacity: '1.0',}, 1700);
	$(".h2three").delay(1000);
	$(".h2three").animate({left: '18%', opacity: '1.0',}, 1700);
	$(".h2four").animate({left: '18%', opacity: '1.0',}, 1700);
	$(".pone").animate({right: '13%', opacity: '1.0',}, 2000);
	$(".ptwo").delay(500);
	$(".ptwo").animate({right: '13%', opacity: '1.0',}, 2000);
	$(".pthree").delay(1000);
	$(".pthree").animate({right: '13%', opacity: '1.0',}, 2000);
	// Carousel
	jQuery("#waterwheel-carousel-vertical").waterwheelCarousel({
		orientation: 'vertical',
		separation: 140,
		horizonOffset: 0,
		opacityMultiplier: .7
	});
});
</script>
<!-- Page interactions -->
<script>
$(document).ready(function(){
	$(".group1").hide();
	$(".group2").hide();
	$(".group3").hide();
	$(".group4").hide();
	$(".fr").hide();
	$(".active_olivier").hide();
	$(".active_example").hide();
	$("#olivier").click(function(){
		$(".all").hide();
		$(".active_example").hide();
		$(".active_olivier").fadeIn();
	});
	$("#example").click(function(){
		$(".active_olivier").hide();
		$(".all").hide();
		$(".active_example").fadeIn();
	});
	$("#all").click(function(){
		$(".active_olivier").hide();
		$(".active_example").hide();
		$(".all").fadeIn();
	});
	$("#grp1").click(function(){
		$(".group1").slideToggle("slower");
	});
	$("#grp2").click(function(){
		$(".group2").slideToggle("slower");
	});
	$(".h2two").click(function(){
		$(".icon-sort-amount-desc1").fadeOut();
		$(".group4").slideUp("fast");
		$(".group3").slideToggle("slow");
		$(".icon-sort-amount-desc2").fadeIn();
	});
	$(".h2three").click(function(){
		$(".icon-sort-amount-desc2").fadeOut();
		$(".group3").slideUp("fast");
		$(".group4").slideToggle("slow");
		$(".icon-sort-amount-desc1").fadeIn();
	});
	$("#francais").click(function(){
		$(".en").hide();
		$(".fr").fadeIn("slow");
	});
	$("#english").click(function(){
		$(".fr").hide();
		$(".en").fadeIn("slow");
	});
});
</script>
<script src="carousel/js/waterwheel_carousel.js"></script>
