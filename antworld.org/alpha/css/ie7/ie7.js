/* To avoid CSS expressions while still supporting IE 7 and IE 6, use this script */
/* The script tag referencing this file must be placed before the ending body tag. */

/* Use conditional comments in order to target IE 7 and older:
	<!--[if lt IE 8]><!-->
	<script src="ie7/ie7.js"></script>
	<!--<![endif]-->
*/

(function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'icomoon\'">' + entity + '</span>' + html;
	}
	var icons = {
		'icon-home': '&#xe617;',
		'icon-pencil2': '&#xe600;',
		'icon-film': '&#xe601;',
		'icon-dice': '&#xe623;',
		'icon-book': '&#xe602;',
		'icon-books': '&#xe603;',
		'icon-library': '&#xe624;',
		'icon-files-empty': '&#xe625;',
		'icon-file-text2': '&#xe626;',
		'icon-file-picture': '&#xe627;',
		'icon-file-music': '&#xe628;',
		'icon-file-play': '&#xe629;',
		'icon-file-video': '&#xe62a;',
		'icon-price-tag': '&#xe604;',
		'icon-calculator': '&#xe621;',
		'icon-location': '&#xe605;',
		'icon-location2': '&#xe606;',
		'icon-printer': '&#xe622;',
		'icon-download': '&#xe62b;',
		'icon-upload': '&#xe62c;',
		'icon-floppy-disk': '&#xe62d;',
		'icon-database': '&#xe62e;',
		'icon-undo2': '&#xe607;',
		'icon-redo2': '&#xe608;',
		'icon-users': '&#xe609;',
		'icon-spinner': '&#xe60a;',
		'icon-zoom-in': '&#xe61b;',
		'icon-zoom-out': '&#xe61c;',
		'icon-bug': '&#xe60b;',
		'icon-pie-chart': '&#xe60c;',
		'icon-stats-dots': '&#xe60d;',
		'icon-stats-bars': '&#xe60e;',
		'icon-menu2': '&#xe60f;',
		'icon-link': '&#xe610;',
		'icon-attachment': '&#xe611;',
		'icon-blocked': '&#xe61d;',
		'icon-cross': '&#xe61e;',
		'icon-enter': '&#xe62f;',
		'icon-exit': '&#xe630;',
		'icon-loop2': '&#xe612;',
		'icon-circle-up': '&#xe61f;',
		'icon-sort-amount-desc': '&#xe613;',
		'icon-sigma': '&#xe614;',
		'icon-mail4': '&#xe615;',
		'icon-google-plus3': '&#xe616;',
		'icon-facebook3': '&#xe618;',
		'icon-twitter3': '&#xe619;',
		'icon-linkedin': '&#xe61a;',
		'icon-yelp': '&#xe631;',
		'icon-file-pdf': '&#xe620;',
		'0': 0
		},
		els = document.getElementsByTagName('*'),
		i, c, el;
	for (i = 0; ; i += 1) {
		el = els[i];
		if(!el) {
			break;
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
}());
