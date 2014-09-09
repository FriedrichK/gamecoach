/* global angular, describe, beforeEach, inject, $, it, expect, spyOn */
'use strict';
 
describe('userProfileService', function() {

	var userProfileService, httpBackend, redirectLinkService;
	var redirectUrl = '/somewhere?else=entirely';

	beforeEach(function() {
		module('ngMockE2E');
		module('mentorContactApp');
	});

	beforeEach(angular.mock.module('loginApp'));

	beforeEach(module(function($provide) {
		redirectLinkService = {
			getRedirectUrl: function() {
				return redirectUrl;
			},
			redirect: function(link) {}
		};
		$provide.value("redirectLinkService", redirectLinkService);
	}));

	beforeEach(inject(function(_userProfileService_, _redirectLinkService_, _$httpBackend_) {
		httpBackend = _$httpBackend_;
		httpBackend.expectPOST('/api/mentors/').respond(200, {});

		redirectLinkService = _redirectLinkService_;
		userProfileService = _userProfileService_;
	}));

	it('shouldRedirectToNext', function() {
		spyOn(redirectLinkService, 'redirect');

		userProfileService.submit();
		httpBackend.flush();
		expect(redirectLinkService.redirect).toHaveBeenCalledWith(redirectUrl);
	});

});