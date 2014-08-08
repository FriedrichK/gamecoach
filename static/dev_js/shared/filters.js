/* global document, angular */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.filter('capitalize', function() {
	return function(input, scope) {
		if (input != null) {
			return input.substring(0,1).toUpperCase() + input.substring(1);
		}
	};
});

gamecoachShared.filter('percentAsString', function() {
	return function(input, precision) {
		if(!input || input == '' || isNaN(input)) {
			return null;
		}

		if(!precision) {
			precision = 0;
		}
		return (parseFloat(input)*100).toFixed(precision) + "%";
	};
});
