/* global angular */
var mentorResultsApp = angular.module('mentorResultsApp', ['ngAnimate', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);