<?php
// Set headers to prevent caching
header('Content-Type: image/png');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');


// INIT IMAGE AND VARIABLES
$IMAGE_WIDTH = isset($_GET['width']) ? max(1, min(1920, intval($_GET['width']))) : 640;
$IMAGE_HEIGHT = isset($_GET['height']) ? max(1, min(1920, intval($_GET['height']))) : 480;
$DISHES_COUNT = isset($_GET['count']) ? max(0, min(100, intval($_GET['count']))) : 3;
$FONT_SIZE = isset($_GET['fontsize']) ? max(2, min(32, intval($_GET['fontsize']))) : 14;
$DEFAULT_RESTAURANTS = array(
	"Invito",
	"Opus Restaurang & Pianobar",
	"Bryners Kök",
	"Oscar Matsal & Bar"
);

// Create the image
$im = imagecreatetruecolor($IMAGE_WIDTH, $IMAGE_HEIGHT);

// Create some colors
$white = imagecolorallocate($im, 255, 255, 255);
$gray = imagecolorallocate($im, 128, 128, 128);
$black = imagecolorallocate($im, 0, 0, 0);

imagefilledrectangle($im, 0, 0, $IMAGE_WIDTH, $IMAGE_HEIGHT, $white);

// Replace path by your own font path
$font = './arial.ttf';
$fontBold = './arialbd.ttf';


// Function to wrap text to a specific width
function makeTextBlock($text, $fontfile, $fontsize, $width) {
	$words = explode(' ', $text);
	$lines = array($words[0]);
	$currentLine = 0;

	for($i = 1; $i < count($words); $i++) {
		$lineSize = imagettfbbox($fontsize, 0, $fontfile, $lines[$currentLine] . ' ' . $words[$i]);

		if($lineSize[2] - $lineSize[0] < $width) {
			$lines[$currentLine] .= ' ' . $words[$i];
		} else {
			$currentLine++;
			$lines[$currentLine] = $words[$i];
		}
	}

	return array(
		"text" => implode("\n", $lines),
		"lines" => count($lines)
	);
}


try {
	///////////////////////////////////////////
	// GET DATA FROM API
	///////////////////////////////////////////
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_URL, 'https://gulle.se/api/lunch/');
	$result = curl_exec($ch);
	curl_close($ch);

	$data = json_decode($result, true);

	// Figure out what restaurants to use
	$restaurants = array();

	foreach ($data as $restaurant) {
		$tmpRestaurant = null;

		if (isset($_GET['filter_specials']) && $_GET['filter_specials'] == 'huhtalo' && $restaurant['name'] == 'Spisa hos Liza') {
			$DISHES_COUNT = 100;
			$tmpRestaurant = $restaurant;

		} else if (isset($_GET['filter_specials']) && strlen($_GET['filter_specials']) > 0) {
			$tmpSpecials = [];
			foreach ($restaurant['specials'] as $special) {
				if (stripos(html_entity_decode($special), rawurldecode($_GET['filter_specials'])) !== false) {
					$tmpSpecials[] = $special;
				}
			}

			if (count($tmpSpecials) > 0) {
				$tmpRestaurant = $restaurant;
				$tmpRestaurant['specials'] = $tmpSpecials;
			}

		} else if (isset($_GET['filter_restaurant']) && strlen($_GET['filter_restaurant']) > 0) {
			if (stripos(html_entity_decode($restaurant['name']), rawurldecode($_GET['filter_restaurant'])) !== false) {
				$tmpRestaurant = $restaurant;
			}

		} else if (isset($_GET['restaurants']) && is_array($_GET['restaurants'])) {
			// if we use asterisk, we take them all
			if (isset($_GET['restaurants'][0]) && $_GET['restaurants'][0] == "*") {
				$tmpRestaurant = $restaurant;

			} else {
				// take only the one that matches
				foreach ($_GET['restaurants'] as $targetRestaurantName) {
					if (html_entity_decode($restaurant['name']) == rawurldecode($targetRestaurantName)) {
						$tmpRestaurant = $restaurant;
					}
				}
			}

		} else {
			// take default ones
			if (in_array($restaurant['name'], $DEFAULT_RESTAURANTS)) {
				$tmpRestaurant = $restaurant;
			}
		}


		if ($tmpRestaurant) {
			$restaurants[] = $tmpRestaurant;
		}
	}

	// sort by name
	function cmp($a, $b) {
		return strcmp($a['name'], $b['name']);
	}

	usort($restaurants, "cmp");


	///////////////////////////////////////////
	// BEGIN IMAGE DRAWING
	///////////////////////////////////////////
	$CURSOR_X = 10;
	$CURSOR_Y = $FONT_SIZE + 10;

	imagettftext($im, 8, 0, $IMAGE_WIDTH-94, 18, $gray, $font, date('Y-m-d H:i', strtotime('now')));

	if (count($restaurants) == 0) {
		imagettftext($im, 14, 0, 10, 24, $black, $font, "Inga restauranger matchade ditt sökresultat.");

	} else {
		for ($i=0; $i<count($restaurants); $i++) {
			$restaurant = $restaurants[$i];

			// restaurant name
			imagettftext($im, $FONT_SIZE, 0, $CURSOR_X, $CURSOR_Y, $black, $fontBold, $restaurant['name']);
			$CURSOR_Y += ($FONT_SIZE + ($FONT_SIZE/2));

			// specials
			$CURSOR_X += $FONT_SIZE/2;
			for ($j=0; $j<$DISHES_COUNT; $j++) {
				if (isset($restaurant['specials'][$j]) && strlen($restaurant['specials'][$j]) > 0) {
					$text = html_entity_decode("&bull; " . trim($restaurant['specials'][$j]));
					$block = makeTextBlock($text, $font, $FONT_SIZE-2, $IMAGE_WIDTH-30);

					imagettftext($im, $FONT_SIZE-2, 0, $CURSOR_X, $CURSOR_Y, $black, $font, $block['text']);

					$CURSOR_Y += ($FONT_SIZE + ($FONT_SIZE/2)) * $block['lines'];
				}
			}

			$CURSOR_X -= $FONT_SIZE/2;
			$CURSOR_Y += ($FONT_SIZE + 4);
		}
	}
} catch (Exception $e) {
	imagefilledrectangle($im, 0, 0, $IMAGE_WIDTH, $IMAGE_HEIGHT, $white);

	imagettftext($im, 12, 0, 10, 22, $black, $font, "Error drawing image:\n");
	imagettftext($im, 12, 0, 10, 40, $black, $font, $e->getMessage());
}


// Using imagepng() results in clearer text compared with imagejpeg()
imagepng($im);
imagedestroy($im);
?>