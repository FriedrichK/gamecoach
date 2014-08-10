/* global angular */
var genericApp = angular.module('genericApp', ['gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);