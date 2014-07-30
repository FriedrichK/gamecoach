/* global angular, describe, beforeEach, inject, $, it, expect */
'use strict';
 
describe('conversationService', function() {

	var messsageStreamService;

	beforeEach(angular.mock.module('conversationApp'));

	beforeEach(inject(function(_messsageStreamService_) {
		messsageStreamService = _messsageStreamService_;
	}));

	it('shouldUpdateMessageStreamAsExpected', function() {
		expect(messsageStreamService.updateStream(null, null)).toEqual(1);
	});

});