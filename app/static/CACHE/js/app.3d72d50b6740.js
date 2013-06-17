// Generated by CoffeeScript 1.6.2
angular.module('barometre', []).config([
  '$interpolateProvider', '$routeProvider', function($interpolateProvider, $routeProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    return $routeProvider.when('/', {
      controller: QuestionListCtrl,
      templateUrl: "/partial/questionList.html"
    }).when('/answers/', {
      controller: AnswerGraphCtrl,
      templateUrl: "/partial/answerGraph.html"
    }).otherwise({
      redirectTo: '/'
    });
  }
]).animation("explode", function() {
  return {
    setup: function(element) {
      return element.css({
        "opacity": 1
      });
    },
    start: function(element, done) {
      return element.animate({
        "opacity": 0
      }, 1000, function() {
        return done();
      });
    },
    cancel: function(element, done) {}
  };
});
