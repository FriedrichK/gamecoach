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

conversationApp.factory('messageStreamFormattingService', function($filter) {
  var isToday = function(d) {
    var now = new Date();
    if(d.getYear() === now.getYear() && d.getMonth() === now.getMonth() + 1 && d.getDate() === now.getDate()) {
      console.log("match");
      return true;
    }
    return false;
  };
  var convertJsonToDate = function(d) {
    return new Date(d.year, d.month, d.day, d.hour, d.minute, d.second, 0);
  };
  var formatMessage = function(message) {
    var date = convertJsonToDate(message.sent_at);
    var format = 'shortDate';
    if(isToday(date)) {
      format = 'shortTime';
    }
    message.sent_at = $filter('date')(date, format);
    return message;
  };
  var formatMessages = function(messages) {
    var formattedMessages = [];
    angular.forEach(messages, function(message) {
      formattedMessages.push(formatMessage(message));
    });
    return formattedMessages;
  };
  return {
    format: function(messages) {
      return formatMessages(messages);
    }
  };
});
