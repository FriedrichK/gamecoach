/* global angular, describe, beforeEach, inject, $, it, expect */
'use strict';
 
describe('tools_services', function() {

	var timeService;

	beforeEach(angular.mock.module('gamecoachShared'));

	beforeEach(inject(function(_timeService_) {
		timeService = _timeService_;
	}));

	it('shouldConvertJsonToExpectedDate', function() {
		var json = {
			year: 2014,
			month: 8,
			day: 9,
			hour: 18,
			minute: 12,
			second: 20
		};
		var actual = timeService.convertJsonToDate(json);
		expect(actual.toJSON()).toEqual('2014-08-09T16:12:20.000Z');
	});

});