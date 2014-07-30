/* global angular, describe, beforeEach, inject, $, it, expect */
'use strict';
 
describe('conversationService', function() {

	var redirectLinkService, location;
	var expectedUrl = '/this/is/the/next/url';

	beforeEach(angular.mock.module('loginApp'));

	beforeEach(module(function($provide) {
		location = {
			search: function() {
				return {
					next: expectedUrl
				};
			}
		};
		$provide.value("$location", location);
	}));

	beforeEach(inject(function(_redirectLinkService_, _$location_) {
		redirectLinkService = _redirectLinkService_;
	}));

	it('shouldGetExpectedRedirectLinkFromUrl', function() {
		expect(redirectLinkService.getRedirectUrl()).toEqual(expectedUrl);
	});

});