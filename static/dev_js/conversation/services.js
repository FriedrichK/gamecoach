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
