/* global angular */
var studentOrMentorApp = angular.module('studentOrMentorApp', ['ngRoute', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);