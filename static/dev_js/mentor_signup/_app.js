/* global angular */
var app = angular.module('app', ['angularFileUpload', 'gamecoachShared'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);