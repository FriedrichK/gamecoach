/* global angular */
var app = angular.module('app', ['ngAnimate'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);