var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('css', function () {
    return gulp.src([
            // 'node_modules/angular-ui-bootstrap/dist/ui-bootstrap-csp.css'
        ])
        .pipe(concat('module.css'))
        .pipe(gulp.dest('dist'));
});

// define tasks here
gulp.task('default', ['css'], function () {
    // run tasks here
    // set up watch handlers here
    return gulp.src([
            'js/*.js',
            'node_modules/sarsha-loading-spinner/loading-spinner.min.js',
            'node_modules/angular-sticky-plugin/dist/angular-sticky.min.js',
            // 'node_modules/angular-ui-bootstrap/dist/ui-bootstrap-tpls.js',
            './app.js',
            'src/*.js',
        ])
        .pipe(concat('module.js'))
        .pipe(gulp.dest('dist'));
});