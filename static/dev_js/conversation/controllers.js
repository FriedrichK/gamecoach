/* global angular, document, window, F */

var conversationApp = angular.module('conversationApp'); 
conversationApp.controller('SubmissionController', function($scope) {
	$scope.submit = function() {
		console.log("click");
	};
});

conversationApp.controller('OtherUserProfileController', function($scope) {
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