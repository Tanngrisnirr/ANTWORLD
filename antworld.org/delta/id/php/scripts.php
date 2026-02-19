<script type="text/javascript" src="http://palearcticantkey.eu/js/jquery_1_6_1.js"></script>
<script type="text/javascript" src="http://palearcticantkey.eu/js/jquery_1_9_1.js"></script>
<script type="text/javascript" src="http://palearcticantkey.eu/js/jquery-1.11.js"></script>
<script type="text/javascript" src="http://palearcticantkey.eu/js/jquery_1_8_13.js"></script>
<script src="mobile/fastclick/lib/fastclick.js" type="text/javascript"></script> <!-- 300ms time reduction for mobile click -->
<script type="text/javascript">
		window.addEventListener('load', function() {
		new FastClick(document.body);}, false);
</script>
<script src="http://palearcticantkey.eu/js/jquery_1_3_easing.js"></script>  <!-- Animation -->
<script>
$(document).ready(function(){
		jQuery.easing.def = 'easeInOutQuint';
        $(".h2one").animate({left: '18%', opacity: '1.0',}, 1700);
		$(".h2two").delay(500);
        $(".h2two").animate({left: '18%', opacity: '1.0',}, 1700);
		$(".h2three").delay(1000);
        $(".h2three").animate({left: '18%', opacity: '1.0',}, 1700);
        $(".pone").animate({right: '13%', opacity: '1.0',}, 2000);
		$(".ptwo").delay(500);
        $(".ptwo").animate({right: '13%', opacity: '1.0',}, 2000);
		$(".pthree").delay(1000);
        $(".pthree").animate({right: '13%', opacity: '1.0',}, 2000);
		<!--$('[data-toggle=drop-panel]').hcaptions();  Carousel caption-->
		jQuery("#waterwheel-carousel-vertical").waterwheelCarousel
		({ <!-- Carousel itself-->
		orientation: 'vertical',
		separation: 140,
		horizonOffset: 0,
		opacityMultiplier: .7
		});
});
</script>
<script src="http://palearcticantkey.eu/js/jquery_1_11_3_jquery_min.js"></script> <!-- SLIDES -->
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
<script src="http://palearcticantkey.eu/carousel/js/jquery_1_7_2.js"></script> <!-- Carousel-->
<script src="http://palearcticantkey.eu/carousel/js/waterwheel_carousel.js"></script> <!-- Carousel-->