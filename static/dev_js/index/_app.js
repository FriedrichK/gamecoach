/* global angular */
var app = angular.module('app', ['gamecoachShared'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);