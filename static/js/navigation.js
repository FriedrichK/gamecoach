/* global document, angular, window */
var gamecoachNavigation = angular.module('gamecoachNavigation', []);
gamecoachNavigation.controller('NavigationController', function($scope) {
	$scope.homeLink = function() {
		window.location = '/';
	};
	$scope.registerMentorLink = function() {
		window.location = '/register/mentor';
	};
});