/* global angular, document, window, F, BaseProfileController, $ */

var conversationApp = angular.module('conversationApp'); 
conversationApp.controller('SubmissionController', function($scope) {
	$scope.submit = function() {
		console.log("click");
	};
});

conversationApp.controller('OtherUserProfileController', function($scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService) {
	var mentorId = $('input[type=hidden][name=conversationPartner]').val();
	BaseProfileController.call(this, $scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService, mentorId);
});

conversationApp.controller('MessageController', function($scope, $element, conversationService, messsageStreamService) {
	var userId = '123';
	var partnerId = "abcd";
	angular.element($element).ready(function() {
		conversationService.getConversation(userId, partnerId, function(data) {
			var stream = "main";
			$scope.messageStream = messsageStreamService.updateStream(stream, data);
		});
	});
});