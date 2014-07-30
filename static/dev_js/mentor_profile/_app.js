/* global angular */
var mentorProfileApp = angular.module('mentorProfileApp', ['ngAnimate', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);