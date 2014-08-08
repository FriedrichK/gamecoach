/* global angular */
var conversationApp = angular.module('conversationApp', ['gamecoachShared', 'gamecoachNavigation']);
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
  var formatMessages = function(messages) {
    var formattedMessages = [];
    angular.forEach(messages, function(message) {
      formattedMessages.push(timeService.formatMessageDate(message));
    });
    return formattedMessages;
  };
  return {
    format: function(messages) {
      return formatMessages(messages);
    }
  };
});
