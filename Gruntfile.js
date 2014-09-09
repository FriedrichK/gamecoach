module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      shared: {
        src: ['static/dev_js/shared/**/*.js', '!static/dev_js/shared/**/*.test.js'],
        dest: 'static/js/shared.js'
      },
      navigation: {
        src: ['static/dev_js/navigation/**/*.js', '!static/dev_js/navigation/**/*.test.js'],
        dest: 'static/js/navigation.js'
      },
      generic: {
        src: ['static/dev_js/generic/**/*.js', '!static/dev_js/generic/**/*.test.js'],
        dest: 'static/js/generic.js'
      },
      login: {
        src: ['static/dev_js/login/**/*.js', '!static/dev_js/login/**/*.test.js'],
        dest: 'static/js/login.js'
      },
      student_or_mentor: {
        src: ['static/dev_js/student_or_mentor/**/*.js', '!static/dev_js/student_or_mentor/**/*.test.js'],
        dest: 'static/js/student_or_mentor.js'
      },
      settings: {
        src: ['static/dev_js/settings/**/*.js', '!static/dev_js/settings/**/*.test.js', '!static/dev_js/settings/**/*.test.js'],
        dest: 'static/js/settings.js'
      },
      index: {
        src: ['static/dev_js/index/**/*.js', '!static/dev_js/index/**/*.test.js'],
        dest: 'static/js/index.js'
      },
      mentor_results: {
        src: ['static/dev_js/mentor_results/**/*.js', '!static/dev_js/mentor_results/**/*.test.js'],
        dest: 'static/js/mentor_results.js'
      },
      mentor_profile: {
        src: ['static/dev_js/mentor_profile/**/*.js', '!static/dev_js/mentor_profile/**/*.test.js'],
        dest: 'static/js/mentor_profile.js'
      },
      mentor_signup: {
        src: ['static/dev_js/mentor_signup/**/*.js', '!static/dev_js/mentor_signup/**/*.test.js'],
        dest: 'static/js/mentor_signup.js'
      },
      mentor_contact: {
        src: ['static/dev_js/mentor_contact/**/*.js', '!static/dev_js/mentor_contact/**/*.test.js'],
        dest: 'static/js/mentor_contact.js'
      },
      conversation: {
        src: ['static/dev_js/conversation/**/*.js', '!static/dev_js/conversation/**/*.test.js'],
        dest: 'static/js/conversation.js'
      },
      edit_profile: {
        src: ['static/dev_js/edit_profile/**/*.js', '!static/dev_js/edit_profile/**/*.test.js'],
        dest: 'static/js/edit_profile.js'
      }
    },
    uglify: {
      shared: {
        src: 'static/js/shared.js',
        dest: 'static/js/shared.min.js'
      },
      navigation: {
        src: 'static/js/navigation.js',
        dest: 'static/js/navigation.min.js'
      },
      generic: {
        src: 'static/js/generic.js',
        dest: 'static/js/generic.min.js'
      },
      login: {
        src: 'static/js/login.js',
        dest: 'static/js/login.min.js'
      },
      student_or_mentor: {
        src: 'static/js/student_or_mentor.js',
        dest: 'static/js/student_or_mentor.min.js'
      },
      settings: {
        src: 'static/js/settings.js',
        dest: 'static/js/settings.min.js'
      },
      index: {
        src: 'static/js/index.js',
        dest: 'static/js/index.min.js'
      },
      mentor_results: {
        src: 'static/js/mentor_results.js',
        dest: 'static/js/mentor_results.min.js'
      },
      mentor_profile: {
        src: 'static/js/mentor_profile.js',
        dest: 'static/js/mentor_profile.min.js'
      },
      mentor_signup: {
        src: 'static/js/mentor_signup.js',
        dest: 'static/js/mentor_signup.min.js'
      },
      mentor_contact: {
        src: 'static/js/mentor_contact.js',
        dest: 'static/js/mentor_contact.min.js'
      },
      conversation: {
        src: 'static/js/conversation.js',
        dest: 'static/js/conversation.min.js'
      },
      edit_profile: {
        src: 'static/js/edit_profile.js',
        dest: 'static/js/edit_profile.min.js'
      }
    },
    jshint: {
      files: 'static/dev_js/**/*.js',
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        boss: true,
        eqnull: true,
        node: true,
        ignores: ['static/dev_js/_libraries/*']
      }
    },
    clean: ['static/js', 'static/css', 'static/dev_css'],
    sass: {
      dist: {
        options: {

        },
        files: {
          'static/dev_css/shared.css': 'static/dev_scss/shared/shared.scss',
          'static/dev_css/navigation.css': 'static/dev_scss/navigation/navigation.scss',
          'static/dev_css/generic.css': 'static/dev_scss/generic/generic.scss',
          'static/dev_css/login.css': 'static/dev_scss/login/login.scss',
          'static/dev_css/student_or_mentor.css': 'static/dev_scss/student_or_mentor/student_or_mentor.scss',
          'static/dev_css/settings.css': 'static/dev_scss/settings/settings.scss',
          'static/dev_css/index.css': 'static/dev_scss/index/index.scss',
          'static/dev_css/mentor_results.css': 'static/dev_scss/mentor_results/mentor_results.scss',
          'static/dev_css/mentor_profile.css': 'static/dev_scss/mentor_profile/mentor_profile.scss',
          'static/dev_css/mentor_signup.css': 'static/dev_scss/mentor_signup/mentor_signup.scss',
          'static/dev_css/mentor_contact.css': 'static/dev_scss/mentor_signup/mentor_contact.scss',
          'static/dev_css/conversation.css': 'static/dev_scss/conversation/conversation.scss',
          'static/dev_css/edit_profile.css': 'static/dev_scss/edit_profile/edit_profile.scss'
        }
      }
    },
    cssmin: {
      minify: {
        files: {
          'static/css/shared.css': 'static/dev_css/shared.css',
          'static/css/navigation.css': 'static/dev_css/navigation.css',
          'static/css/generic.css': 'static/dev_css/generic.css',
          'static/css/login.css': 'static/dev_css/login.css',
          'static/css/student_or_mentor.css': 'static/dev_css/student_or_mentor.css',
          'static/css/settings.css': 'static/dev_css/settings.css',
          'static/css/index.css': 'static/dev_css/index.css',
          'static/css/mentor_results.css': 'static/dev_css/mentor_results.css',
          'static/css/mentor_profile.css': 'static/dev_css/mentor_profile.css',
          'static/css/mentor_signup.css': 'static/dev_css/mentor_signup.css',
          'static/css/mentor_contact.css': 'static/dev_css/mentor_contact.css',
          'static/css/conversation.css': 'static/dev_css/conversation.css',
          'static/css/edit_profile.css': 'static/dev_css/edit_profile.css'
        }
      }
    },
    copy: {
      libraries: {
        files: [
          {expand: true, cwd: 'static/dev_js/_libraries/', src: ['**/*'], dest: 'static/js/'},
          {expand: true, cwd: 'static/dev_scss/_libraries/', src: ['**/*.css'], dest: 'static/css/'},
        ]
      }
    },
    watch: {
      scripts: {
        files: ['static/dev_js/**/*.js', 'static/dev_scss/**/*.scss'],
        tasks: ['jshint', 'clean', 'sass', 'cssmin', 'concat', 'uglify', 'copy'],
        options: {
          spawn: false,
        },
      }
    }
  });

  // Default task.
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.registerTask('default', 'runs my tasks', function() {
    var tasks = ['jshint', 'clean', 'sass', 'cssmin', 'concat', 'uglify', 'copy'];
    grunt.option('force', true);
    grunt.task.run(tasks);
  });

};