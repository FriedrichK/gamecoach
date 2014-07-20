/* global angular */
var app = angular.module('app', ['angularFileUpload'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);