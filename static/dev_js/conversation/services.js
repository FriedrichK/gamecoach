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
