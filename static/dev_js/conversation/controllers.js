/* global angular, document, window, F, BaseProfileController, $ */

var conversationApp = angular.module('conversationApp'); 
conversationApp.controller('SubmissionController', function($rootScope, $scope, messageService) {
	$scope.submit = function() {
		var mentorId = $('input[type=hidden][name=conversationPartner]').val();
		var message = angular.element('textarea[name=field]').val();
		if(!message || message === '') {
			return;
		}
		messageService.postMessage(mentorId, message, function(result) {
			if(result.status === 200) {
				angular.element('textarea[name=field]').val('');
				$rootScope.$broadcast('newMessageSuccessfullySent');
			}
		});
	};
});

conversationApp.controller('OtherUserProfileController', function($scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService) {
	var mentorId = $('input[type=hidden][name=conversationPartner]').val();
	BaseProfileController.call(this, $scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService, mentorId);
	$scope.goToProfile = function() {
		window.location = '/mentor/' + mentorId;
	};
});

conversationApp.controller('MessageController', function($scope, $element, conversationService, messageStreamFormattingService) {
	var partnerId = $('input[type=hidden][name=conversationPartner]').val();
	var updateMessages = function() {
		conversationService.getConversation(null, partnerId, function(data) {
			var stream = "main";
			$scope.messageStream = messageStreamFormattingService.format(data);
		});
	};
	angular.element($element).ready(function() {
		updateMessages();
	});
	$scope.$on('newMessageSuccessfullySent', function(event) {
		updateMessages();
	});
});

conversationApp.controller('InboxController', function($scope, $element, inboxService, messageStreamFormattingService) {
	var updateInbox = function() {
		inboxService.getInbox(function(data) {
			$scope.inbox = messageStreamFormattingService.format(data);
		});
	};
	angular.element($element).ready(function() {
		updateInbox();
	});
	$scope.goToConversation = function(conversationPartnerUsername) {
		window.location = '/conversation/' + conversationPartnerUsername;
	};
});