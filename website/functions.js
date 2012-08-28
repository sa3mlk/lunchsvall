function filter_specials(query) {
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
	// Don't include the first header tr
	var num_restaurants = $('#daily_specials tr').length - 1;
	// Select a restaurant between 1 and num_restaurants
	var random_choice = Math.ceil(Math.random() * num_restaurants);
	var query = $('#daily_specials tr:nth-child(' + random_choice + ')').find('strong').text();
	// Now filter only that restaurant
	$('.search').val(query);
	filter_specials(query);
}

function radians(n) {
	/* Converts numeric degrees to radians */
	return n * Math.PI / 180;
}

function distance(pos1, pos2) {
	/* Radius of the Earth in metres */
	var R = 6371000.0;

	var dLat = radians(pos2.lat - pos1.lat);
	var dLon = radians(pos2.lon - pos1.lon); 

	var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
			Math.cos(radians(pos1.lat)) * Math.cos(radians(pos2.lat)) * 
			Math.sin(dLon / 2) * Math.sin(dLon / 2); 

	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)); 

	/* Return the distance in metres */
	return R * c;
}

function format_distance(pos1, pos2) {
	var meters = Math.round(distance(pos1, pos2));
	return meters + " meter";
}

function sort_items_on_distance(coords) {
}

function insert_distance(coords) {
	$("#daily_specials tr:gt(0)").each(function() {
		td = $(this).find("td").eq(2);
		var split = td.text().split(",");
		if (split.length === 2) {
			td.html("<small>" + format_distance(
					{ "lat": split[0], "lon": split[1] },
					{ "lat": coords.latitude, "lon": coords.longitude }
				) + "</small>"
			);
		} else {
			td.html("<small>Okänt</small>");
		}
	});
}

$(function () {
	$("input.search").focus();

	var coords = null;

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			function (pos) {
				insert_distance(pos.coords);
			},
			function (msg) {
				alert("Error: " + msg);
			}
		);
	}

	//var data_url = "get_json.php";
	//var data_url = "2012-04-13.json";
	var data_url = "data.json";
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
						"<br/><a href=\"" + n.mapurl + "\">" +
						"<small>" + n.streetaddress + "</small></a><br/>" +
						"<td valign=\"top\">" + daily_specials + "</td>" +
						"<td valign=\"top\"><small>" + n.geopos + "</small></td>" +
						"</tr>"
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
