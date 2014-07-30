/* global angular, describe, beforeEach, inject, $, it, expect */
'use strict';
 
describe('LoginController', function() {

	var scope, $controller;

	beforeEach(angular.mock.module('loginApp'));

	beforeEach(inject(function($controller, $rootScope) {
		scope = $rootScope.$new();
		$controller('LoginController', {$scope: scope, $element: $('<div></div>')});
	}));

	it('shouldFormatTopHeroesAsExpected', function() {
		expect(true).toBe(true);
	});

});