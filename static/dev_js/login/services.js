/* global angular */
var loginApp = angular.module('loginApp');

loginApp.factory('redirectLinkService', function($location) {
  return {
	getRedirectUrl: function() {
		console.log("loc", $location);
		return $location.search().next;
	}
  };
});