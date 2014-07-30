/* global angular */
var mentorSignupApp = angular.module('mentorSignupApp', ['angularFileUpload', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);