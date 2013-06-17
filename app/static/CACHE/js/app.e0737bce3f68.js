// Generated by CoffeeScript 1.6.2
angular.module('barometre', []).config([
  '$routeProvider', '$interpolateProvider', function($routeProvider, $interpolateProvider) {
    $routeProvider.when('/questions', {
      controller: QuestionListCtrl,
      templateUrl: "partial/questionList.html"
    }).otherwise({
      redirectTo: '/questions'
    });
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  }
]);
