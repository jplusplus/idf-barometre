// Generated by CoffeeScript 1.6.2
var QuestionListCtrl;

QuestionListCtrl = function($scope, $http, $rootElement) {
  return $http.get('/static/questions.json').success(function(data) {
    $scope.questions = data;
    return $rootElement.isotope({
      itemSelector: '.question',
      layoutMode: 'fitRows'
    });
  });
};

QuestionListCtrl.$inject = ['$scope', '$http', '$rootElement'];
