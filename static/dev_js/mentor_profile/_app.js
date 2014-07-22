/* global angular */
var app = angular.module('app', ['ngAnimate', 'gamecoachShared'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);