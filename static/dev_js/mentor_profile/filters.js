/* global document, angular */

var app = angular.module('app'); 
app.filter('percentAsString', function() {
	return function(input) {
		return Math.round(input * 100, 0) + "%";
	};
});
