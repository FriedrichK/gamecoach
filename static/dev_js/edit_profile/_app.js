/* global angular */
var editProfileApp = angular.module('editProfileApp', ['angularFileUpload', 'lr.upload', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);