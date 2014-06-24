/* global angular */

var app = angular.module('app'); 
app.factory('profileDataService', function($http) {
	return {
		getMentorProfile: function(mentorId, callable) {
			return $http({
				url: '/api/mentor/' + mentorId,
				method: 'GET',
				params: {}
			})
			.then(function(result) {
				callable(result.data);
			});
		}
	};
});