// Karma configuration
// Generated on Mon Jul 28 2014 21:47:09 GMT+0200 (CEST)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'static/dev_js/_libraries/angular.js',
      'static/dev_js/_libraries/angular-route.min.js',
      'static/dev_js/_libraries/angular-file-upload.min.js',
      'static/dev_js/_libraries/angular-mocks.js',
      'static/dev_js/_libraries/jquery-2.1.1.min.js',

      'static/dev_js/shared/*.js',

      'static/dev_js/mentor_contact/_app.js',
      'static/dev_js/mentor_contact/controllers.js',

      'static/dev_js/conversation/_app.js',
      'static/dev_js/conversation/services.js',
      'static/dev_js/conversation/controllers.js',
      
      'static/dev_js/**/*.test.js'
    ],


    // list of files to exclude
    exclude: [
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,
    usePolling: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['PhantomJS'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false
  });
};
