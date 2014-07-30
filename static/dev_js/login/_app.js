/* global angular */

var loginApp = angular.module('loginApp', ['ngRoute', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);