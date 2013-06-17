// Generated by CoffeeScript 1.6.2
var QuestionListCtrl;

QuestionListCtrl = function($scope, $http, $rootElement) {
  return $http.get('/static/questions.json').success(function(data) {
    var opt;

    $scope.questions = data;
    return opt = {
      itemSelector: '.question',
      layoutMode: 'masonryHorizontal'
    };
  });
};

QuestionListCtrl.$inject = ['$scope', '$http', '$rootElement'];
