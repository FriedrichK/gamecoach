/* global document, angular */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.filter('capitalize', function() {
	return function(input, scope) {
		if (input != null) {
			return input.substring(0,1).toUpperCase() + input.substring(1);
		}
	};
});