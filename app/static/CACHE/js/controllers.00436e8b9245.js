// Generated by CoffeeScript 1.6.2
({
  QuestionListCtrl: function($scope, Question) {
    return $scope.questions = Question.query();
  }
});

QuestionListCtrl.$inject = ['$scope', 'Question'];
