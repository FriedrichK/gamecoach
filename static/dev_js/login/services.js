/* global angular */
var loginApp = angular.module('loginApp');

loginApp.factory('redirectLinkService', function($location) {
  return {
	getRedirectUrl: function() {
		return $location.search().next;
	}
  };
});