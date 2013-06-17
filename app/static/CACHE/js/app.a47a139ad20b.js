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
]).animation("explode-enter", [
  "$rootScope", function($rootScope) {
    return {
      setup: function(element) {
        var dist;

        dist = ~~(Math.random() * 1 - 1) + "px";
        alert(dist);
        return element.css({
          "opacity": 0,
          "transform": "translate(0, " + dist + ")"
        });
      },
      start: function(element, done) {
        return element.animate({
          "opacity": 1,
          "transform": 'translate(0, 0)'
        }, 1000, function() {
          return done();
        });
      },
      cancel: function(element, done) {}
    };
  }
]);
