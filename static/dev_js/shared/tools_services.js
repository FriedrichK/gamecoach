/* global angular */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('timeService', function($filter) {
	return {
		isToday: function(d) {
			var now = new Date();
			if(d.getYear() === now.getYear() && d.getMonth() === now.getMonth() + 1 && d.getDate() === now.getDate()) {
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
			return new Date(d.year, d.month, d.day, d.hour, d.minute, d.second, 0);
		}
	};
});