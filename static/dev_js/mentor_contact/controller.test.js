/* global angular, describe, beforeEach, inject, $, it, expect */
'use strict';
 
describe('TopHeroController', function() {

	var scope, $controller, heroesService;

	beforeEach(angular.mock.module('mentorContactApp'));

	beforeEach(inject(function($controller, $rootScope) {
		heroesService = {
			getHeroHash: function() {
				return {
					'x': 1,
					'y': 2
				};
			}
		};
		scope = $rootScope.$new();
		$controller('TopHeroController', {$scope: scope, $element: $('<div></div>'), heroesService: heroesService});
	}));

	it('shouldFormatTopHeroesAsExpected', function() {
		expect(scope.topheroes).toEqual([{label: 1, identifier: 'x' }, {label: 2, identifier: 'y' }]);
	});

});