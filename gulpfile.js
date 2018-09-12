const gulp = require('gulp');
const imageResize = require('gulp-image-resize');
const zip = require('gulp-zip');
const filter = require('gulp-filter');

var DEST = 'gen/';
function dest(x="") { return gulp.dest(DEST+"/"+x); }

gulp.task('js', function() {
	gulp.src('static/*.js')
	    .pipe(dest());
});

gulp.task('images', function() {
	gulp.src('static/images/background-*.png')
	    .pipe(imageResize({width: 64, height:64, crop: false, upscale: false}))
	    .pipe(dest('images'));
	gulp.src('static/images/plane.svg')
	    .pipe(dest('images'));
	gulp.src('static/images/favicon.png')
	    .pipe(dest('images'));
});

gulp.task('html', function() {
	gulp.src('static/*.html')
	    .pipe(dest());
});

gulp.task('css', function() {
	gulp.src('static/*.css')
	    .pipe(dest());
});

gulp.task('default', ['js', 'images', 'html', 'css'], function() {
	gulp.src(['gen/**/*', '*.py', 'README.md'])
	    .pipe(filter('!gen/messy-chat.zip'))
	    .pipe(zip('messy-chat.zip'))
	    .pipe(dest());
});
