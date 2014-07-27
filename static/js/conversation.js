/* global angular */
var app = angular.module('app', ['gamecoachShared']);
/* global angular, document, window, F */

var app = angular.module('app'); 
app.controller('SubmissionController', function($scope) {
	$scope.submit = function() {
		console.log("click");
	};
});

app.controller('OtherUserProfileController', function($scope) {
});

app.controller('MessageController', function($scope, $element, conversationService) {
	var userId = '123';
	var partnerId = "abcd";
	angular.element($element).ready(function() {
		conversationService.getConversation(userId, partnerId, function(data) {
			console.log(data);
		});
	});
});
/* global angular */
var app = angular.module('app');

app.factory('conversationService', function($http) {
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