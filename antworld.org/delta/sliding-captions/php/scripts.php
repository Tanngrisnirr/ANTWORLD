<script type="text/javascript" src="js/jquery_1_6_1.js"></script>
<script type="text/javascript" src="js/jquery_1_9_1.js"></script>
<script type="text/javascript" src="js/jquery-1.11.js"></script>
<script type="text/javascript" src="js/jquery_1_8_13.js"></script>
<script src="mobile/fastclick/lib/fastclick.js" type="text/javascript"></script> <!-- 300ms time reduction for mobile click -->
<script type="text/javascript">
		window.addEventListener('load', function() {
		new FastClick(document.body);}, false);
</script>
<script src="js/jquery_1_3_easing.js"></script>  <!-- Animation -->
<script>
$(document).ready(function(){
		jQuery.easing.def = 'easeInOutQuint';
        $(".h2one").animate({left: '18%', opacity: '1.0',}, 2000);
		$(".h2two").delay(500);
        $(".h2two").animate({left: '18%', opacity: '1.0',}, 2000);
		$(".h2three").delay(1000);
        $(".h2three").animate({left: '18%', opacity: '1.0',}, 2000);
		<!--$('[data-toggle=drop-panel]').hcaptions();  Carousel caption-->
		jQuery("#waterwheel-carousel-vertical").waterwheelCarousel({ <!-- Carousel itself-->
		orientation: 'vertical',
		separation: 140,
		horizonOffset: 0,
		opacityMultiplier: .7
  });
});
</script>
<script src="js/jquery_1_11_3_jquery_min.js"></script> <!-- SLIDES -->
<script>
$(document).ready(function(){
		$(".group1").hide();
		$(".group2").hide();
		$(".group3").hide();
		$(".group4").hide();
    $("#grp1").click(function(){
        $(".group1").slideToggle("slow");
    });
	$("#grp2").click(function(){
        $(".group2").slideToggle("slow");
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
});
</script>
<script src="carousel/js/jquery_1_7_2.js"></script> <!-- Carousel-->
<script src="carousel/js/waterwheel_carousel.js"></script> <!-- Carousel-->
<script src="js/lib/jquery-1.9.0.min.js" type="text/javascript"></script>  <!-- Image caption -->
<script src="js/jquery.easing.1.3.js" type="text/javascript"></script> <!-- Image caption -->
<script src="js/jquery.index.js" type="text/javascript"></script> <!-- Image caption -->