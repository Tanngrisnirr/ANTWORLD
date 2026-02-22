<!-- jQuery 3.1.1 -->
<?php
$inSpecies = strpos($_SERVER['REQUEST_URI'], '/id/species/') !== false;
$inId = strpos($_SERVER['REQUEST_URI'], '/id/') !== false && !$inSpecies;
if ($inSpecies) {
    $jsPath = '../../js/';
} elseif ($inId) {
    $jsPath = '../js/';
} else {
    $jsPath = 'js/';
}
?>
<script src="<?php echo $jsPath; ?>jquery-3.1.1.min.js"></script>
<script>
$(document).ready(function(){
	// Simple easing fallback if plugin not loaded
	if (!jQuery.easing.easeInOutQuint) {
		jQuery.easing.easeInOutQuint = function(x, t, b, c, d) {
			if ((t/=d/2) < 1) return c/2*t*t*t*t*t + b;
			return c/2*((t-=2)*t*t*t*t + 2) + b;
		};
	}
	jQuery.easing.def = 'easeInOutQuint';

	// Animations
	$(".h2one").animate({left: '18%', opacity: '1.0'}, 1700);
	$(".h2two").delay(500).animate({left: '18%', opacity: '1.0'}, 1700);
	$(".h2three").delay(1000).animate({left: '18%', opacity: '1.0'}, 1700);
	$(".h2four").animate({left: '18%', opacity: '1.0'}, 1700);
	$(".pone").animate({right: '13%', opacity: '1.0'}, 2000);
	$(".ptwo").delay(500).animate({right: '13%', opacity: '1.0'}, 2000);
	$(".pthree").delay(1000).animate({right: '13%', opacity: '1.0'}, 2000);

	// Page interactions
	$(".group1, .group2, .group3, .group4, .fr, .active_olivier, .active_example").hide();

	$("#olivier").click(function(){
		$(".all, .active_example").hide();
		$(".active_olivier").fadeIn();
	});
	$("#example").click(function(){
		$(".active_olivier, .all").hide();
		$(".active_example").fadeIn();
	});
	$("#all").click(function(){
		$(".active_olivier, .active_example").hide();
		$(".all").fadeIn();
	});
	$("#grp1").click(function(){ $(".group1").slideToggle("slower"); });
	$("#grp2").click(function(){ $(".group2").slideToggle("slower"); });
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
	$("#francais").click(function(){ $(".en").hide(); $(".fr").fadeIn("slow"); });
	$("#english").click(function(){ $(".fr").hide(); $(".en").fadeIn("slow"); });
});
</script>
