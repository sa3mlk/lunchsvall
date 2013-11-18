function filter_specials(query) {
	"use strict";
	var search = query, num_visible = 0;
	$('#daily_specials tr').each(function () {
		// Case-insensitive match
		var regexp = new RegExp(search, "i"), td, restaurant, daily;
		if (search.length === 0) {
			$('#daily_specials').show();
			num_visible = 1;
			$(this).show();
		} else {
			td = $(this).find('td');
			if (td.html() !== null) {
				restaurant = td.eq(0).text();
				daily = td.eq(1).text();
				if (restaurant.search(regexp) !== -1 || daily.search(regexp) !== -1) {
					$(this).show();
					num_visible += 1;
				} else {
					$(this).hide();
				}
			}
		}
	});

	if (num_visible === 0) {
		$('#daily_specials').hide();
	} else {
		$('#daily_specials').show();
	}
}

function random_filter() {
	"use strict";
	// Don't include the first header tr
	var num_restaurants = $('#daily_specials tr').length - 1;
	// Select a restaurant between 1 and num_restaurants
	var random_choice = Math.ceil(Math.random() * num_restaurants);
	var query = $('#daily_specials tr:nth-child(' + random_choice + ')').find('strong').text();
	// Now filter only that restaurant
	$('.search').val(query);
	filter_specials(query);
}

$(function () {
	"use strict";
	$('input.search').focus();

	var data_url = "http://gulle.se:40000";
	var no_specials_found = false;

	$.ajax({
		async: false,
		dataType: "json",
		url: data_url,
		type: "GET",
		success: function (data) {
			if (data.length === 0) {
				$("#daily_specials thead").replaceWith("<tr><td><strong>Tji fick du, hittade inga luncher idag!</strong></td></tr>");
				no_specials_found = true;
			} else {
				$.each(data, function (i, n) {
					var daily_specials = "";
					$.each(n.specials, function (j, m) {
						daily_specials += m + "<br/>";
					});
					$("#daily_specials > tbody:last").append(
						"<tr><td valign=\"top\">" +
						"<strong><a href=\"" + n.dataurl + "\">" + n.name + "</a></strong>" +
						"<br/><a href=\"" + n.mapurl + "\"><small>" + n.streetaddress + "</small></td>" +
						"<td valign=\"top\">" + daily_specials + "</td></tr>"
					);
				});
			}
		}
	});

	var url = window.location.href;
	var pos = window.location.href.search("#");
	if (pos > 0) {
		var query = decodeURIComponent(url.substr(pos + 1));
		$('.search').val(query);
		filter_specials(query);
	}

	$('.search').keyup(function () {
		if (no_specials_found) {
			return;
		}
		filter_specials($(this).val());
	});
});
