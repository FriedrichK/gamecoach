/* global document, angular, window */

var app = angular.module('app');
app.controller('NavigationController', function($scope) {
	$scope.homeLink = function() {
		window.location = '/';
	};
	$scope.registerMentorLink = function() {
		window.location = '/register/mentor';
	};
});