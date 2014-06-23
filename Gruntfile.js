module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      shared: {
        src: ['static/dev_js/shared/**/*.js'],
        dest: 'static/js/shared.js'
      },
      index: {
        src: ['static/dev_js/index/**/*.js'],
        dest: 'static/js/index.js'
      },
      mentor_results: {
        src: ['static/dev_js/mentor_results/**/*.js'],
        dest: 'static/js/mentor_results.js'
      },
      mentor_profile: {
        src: ['static/dev_js/mentor_profile/**/*.js'],
        dest: 'static/js/mentor_profile.js'
      }
    },
    uglify: {
      shared: {
        src: 'static/js/shared.js',
        dest: 'static/js/shared.min.js'
      },
      home: {
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
          'static/dev_css/index.css': 'static/dev_scss/index/index.scss',
          'static/dev_css/mentor_results.css': 'static/dev_scss/mentor_results/mentor_results.scss',
          'static/dev_css/mentor_profile.css': 'static/dev_scss/mentor_profile/mentor_profile.scss'
        }
      }
    },
    cssmin: {
      minify: {
        files: {
          'static/css/shared.css': 'static/dev_css/shared.css',
          'static/css/index.css': 'static/dev_css/index.css',
          'static/css/mentor_results.css': 'static/dev_css/mentor_results.css',
          'static/css/mentor_profile.css': 'static/dev_css/mentor_profile.css'
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