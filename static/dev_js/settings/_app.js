/* global angular */
var editSettingsApp = angular.module('editSettingsApp', ['gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);