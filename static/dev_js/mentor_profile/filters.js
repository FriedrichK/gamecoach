/* global document, angular */

var mentorProfileApp = angular.module('mentorProfileApp'); 
mentorProfileApp.filter('percentAsString', function() {
	return function(input) {
		return Math.round(input * 100, 0) + "%";
	};
});
