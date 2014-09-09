/* global angular, window */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('timeService', function($filter) {
	return {
		getCurrentDate: function() {
			return new Date();
		},
		isToday: function(d) {
			var now = this.getCurrentDate();
			if(d.getYear() === now.getYear() && d.getMonth() === now.getMonth() && d.getDate() === now.getDate()) {
				return true;
			}
			return false;
		},
		formatMessageDate: function(message) {
			var date = this.convertJsonToDate(message.sent_at);
			var format = 'shortDate';
			if(this.isToday(date)) {
				format = 'shortTime';
			}
			message.sent_at = $filter('date')(date, format);
			return message;
		},
		convertJsonToDate: function(d) {
			return new Date(d.year, d.month - 1, d.day, d.hour, d.minute, d.second, 0);
		}
	};
});

gamecoachShared.factory('redirectLinkService', function($location) {
  return {
	getRedirectUrl: function() {
		return $location.search().next;
	},
	redirect: function(link) {
		window.location = link;
	}
  };
});