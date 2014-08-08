/* global angular, describe, beforeEach, inject, $, it, expect */
'use strict';
 
describe('tools_services', function() {

	var timeService;

	beforeEach(angular.mock.module('gamecoachShared'));

	beforeEach(inject(function(_timeService_) {
		timeService = _timeService_;
		timeService.getCurrentDate = function() {
			return new Date(2014, 7, 5, 12, 12, 20);
		};
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

	it('shouldRecognizeDateIsToday', function() {
		var mockToday = {
			year: 2014,
			month: 8,
			day: 9,
			hour: 6,
			minute: 13,
			second: 4
		};
		var mockDate = new Date(2014, 7, 5, 18, 12, 20);
		var actual = timeService.isToday(mockDate);
		expect(actual).toBe(true);
	});

});