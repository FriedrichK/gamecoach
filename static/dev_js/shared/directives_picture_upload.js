/* global document, angular */

var gamecoachShared = angular.module('gamecoachShared');
gamecoachShared.directive('gcImageUpload', function() {
	return {
		restrict: 'AEC',
		templateUrl: 'imageUploadDialog.html'
	};
});