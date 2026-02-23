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
