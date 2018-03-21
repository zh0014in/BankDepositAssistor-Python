var gulp = require('gulp');
var concat = require('gulp-concat');

// define tasks here
gulp.task('default', function () {
    // run tasks here
    // set up watch handlers here
    return gulp.src([
            'js/*.js',
            'node_modules/sarsha-loading-spinner/loading-spinner.min.js',
            './app.js',
            'src/*.js',
        ])
        .pipe(concat('module.js'))
        .pipe(gulp.dest('dist'));
});