/* global angular, document, window */

var indexApp = angular.module('indexApp'); 
indexApp.controller('IndexFormController', function($scope, $http) {
	$scope.submit = function($event) {
		var game = $scope.game;
		var region = $scope.region;
		var role = $scope.role;

		var parts = [];

		if(region && region !== 'donotknow') {
			parts.push('regions=' + region);
		}

		if(role && role !== 'donotknow') {
			parts.push('roles=' + role);
		}

		var prefix = '';
		if(parts.length > 0) {
			prefix = '?';
		}

		window.location = '/results' + prefix + parts.join('&');
	};
});