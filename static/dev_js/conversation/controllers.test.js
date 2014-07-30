/* global angular, describe, beforeEach, inject, $, it, expect */
'use strict';
 
describe('MessageController', function() {

	var scope, $controller, conversationService, messsageStreamService;

	beforeEach(angular.mock.module('conversationApp'));

	beforeEach(inject(function($controller, $rootScope) {
		scope = $rootScope.$new();
		$controller('MessageController', {$scope: scope, $element: $('<div></div>'), conversationService: conversationService, messsageStreamService: messsageStreamService});
	}));

});