/* global angular */
var conversationApp = angular.module('conversationApp', ['gamecoachShared', 'gamecoachNavigation']);
/* global angular, document, window, F, BaseProfileController, $, calq */

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
				calq.action.trackSale(
					"Message sent",
					{ "Recipient": mentorId, "Message": message },
					"USD", 
					0.1
				);

				angular.element('textarea[name=field]').val('');
				$rootScope.$broadcast('newMessageSuccessfullySent');
			} else {

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

conversationApp.controller('MessageController', function($scope, $element, $interval, conversationService, messageStreamFormattingService) {
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
	$interval(function(){
		updateMessages();
	}, 3000);
	$scope.$on('newMessageSuccessfullySent', function(event) {
		updateMessages();
	});
});

conversationApp.controller('InboxController', function($scope, $element, $interval, inboxService, messageStreamFormattingService) {
	var updateInbox = function() {
		var mentorId = $('input[type=hidden][name=system_username]').val();
		inboxService.getInbox(function(data) {
			var result = messageStreamFormattingService.format(data, mentorId);
			if(result && result.length > 0) {
				$scope.inbox = result;
			}
		});
	};
	angular.element($element).ready(function() {
		updateInbox();
	});
	$interval(function(){
		updateInbox();
	}, 3000);
	$scope.goToConversation = function(senderUsername, recipientUsername) {
		var mentorId = $('input[type=hidden][name=system_username]').val();
		console.log(senderUsername, recipientUsername, mentorId, (senderUsername === mentorId));
		var conversationPartnerUsername = senderUsername;
		if(senderUsername === mentorId) {
			conversationPartnerUsername = recipientUsername;
		}
		window.location = '/conversation/' + conversationPartnerUsername;
	};
});
/* global angular */
var conversationApp = angular.module('conversationApp');

conversationApp.factory('conversationService', function($http) {
  return {
    getConversation: function(userId, partnerId, callable) {
      return $http({
        url: '/api/conversation/' + partnerId,
        method: "GET",
        params: {ident: userId}
      })
        .then(function(result) {
          callable(result.data);
        }
      );
    }
  };
});

conversationApp.factory('messageService', function($http) {
  return {
    postMessage: function(partnerId, message, callback) {
      return $http({
        url: '/api/conversation/message/',
        method: 'POST',
        data: {recipient: partnerId, message: message}
      })
        .then(function(result) {
          callback(result);
        });
    }
  };
});

conversationApp.factory('inboxService', function($http) {
  return {
    getInbox: function(callback) {
      return $http({
        url: '/api/conversation/',
        method: 'GET'
      })
        .then(function(result) {
          callback(result.data);
        });
    }
  };
});

conversationApp.factory('messageStreamFormattingService', function($filter, timeService) {
  var affixOtherUsernames = function(mentorId, message) {
    message['other_username'] = message.sender.username;
    message['other_username2'] = message.sender.username2;
    if(message.sender.username === mentorId) {
      message['other_username'] = message.recipient.username;
      message['other_username2'] = message.recipient.username2;
    }
    return message;
  };
  var formatMessages = function(messages, mentorId) {
    var formattedMessages = [];
    angular.forEach(messages, function(message) {
      if(mentorId) {
        message = affixOtherUsernames(mentorId, message);
      }
      formattedMessages.push(timeService.formatMessageDate(message));
    });
    return formattedMessages;
  };
  return {
    format: function(mentorId, messages) {
      return formatMessages(mentorId, messages);
    }
  };
});
