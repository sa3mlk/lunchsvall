$(function() {
	$('input.search').focus();

	var data_url = "get_json.php";
	var no_specials_found = false;

	$.ajax({
		async: false,
		dataType: "json",
		url: data_url,
		type: "GET",
		success: function(data) {
			if (data.length == 0) {
				$("#daily_specials thead").replaceWith("<tr><td><strong>Tji fick du, hittade inga luncher idag!</strong></td></tr>");
				no_specials_found = true;
			}
			else {
				$.each(data, function(i, n) {
					var daily_specials = "";
					$.each(n.specials, function(j, m) {
						daily_specials += m + "<br/>";
					});
					$("#daily_specials > tbody:last").append(
						"<tr><td valign=\"top\">" +
						"<strong>" + n.name + "</strong>" +
						"<br/><a href=\"" + n.mapurl + "\"><small>" + n.streetaddress + "</small></td>" +
						"<td>" + daily_specials + "</td></tr>"
					);
				});
			}
		}
	});

	$('.search').keyup(function() {
			if (no_specials_found)
				return;
			var search = $(this).val();
			var num_visible = 0;
			$('#daily_specials tr').each(function() {
				// Case-insensitive match
				var regexp = new RegExp(search, "i");
				if (search.length === 0) {
					$('#daily_specials').show();
					num_visible = 1;
					$(this).show();
				} else {
					var td = $(this).find('td');
					if (td.html() !== null) {
						var restaurant = td.eq(0).text();
						var daily = td.eq(1).text();
						if (restaurant.search(regexp) !== -1 ||
							daily.search(regexp) !== -1) {
							$(this).show();
							num_visible++;
						} else {
							$(this).hide();
						}
					}
				}
			});

			if (num_visible === 0) {
				$('#daily_specials').hide();
			}
			else {
				$('#daily_specials').show();
			}

		});
});
