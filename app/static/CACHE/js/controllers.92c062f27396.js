// Generated by CoffeeScript 1.6.2
var AnswerGraphCtrl, QuestionListCtrl;

QuestionListCtrl = function($scope, $http, $rootElement) {
  return $http.get('/static/questions.json').success(function(data) {
    return $scope.questions = data;
  });
};

QuestionListCtrl.$inject = ['$scope', '$http', '$rootElement'];

AnswerGraphCtrl = function($scope, $http, $rootElement, $routeParams, $location) {
  var dateFormat, insertLinebreaks, parse, render, svg, update, wrapper, wrapperHeight, wrapperWidth, x, y;

  $scope.question = $routeParams.question || "economique";
  $scope.sample = $routeParams.sample || "all";
  $scope.$watch('sample', update);
  $scope.$watch('question', update);
  svg = {};
  parse = d3.time.format("%d/%m/%Y").parse;
  dateFormat = d3.time.format("%b %y");
  wrapper = $rootElement.find(".wrapper");
  wrapperWidth = wrapper.innerWidth();
  wrapperHeight = wrapper.innerHeight() - 20;
  wrapper.jScrollPane({
    hideFocus: true
  });
  x = d3.time.scale();
  y = d3.scale.linear();
  insertLinebreaks = function(d) {
    var el, i, tspan, words, _results;

    el = d3.select(this);
    words = dateFormat(d).split(" ");
    el.text("");
    i = 0;
    _results = [];
    while (i < words.length) {
      tspan = el.append("tspan").text(words[i]);
      if (i > 0) {
        tspan.attr("x", 0).attr("dy", "18");
      }
      _results.push(i++);
    }
    return _results;
  };
  update = function() {
    return $http.get('/static/answers.json').success(render);
  };
  render = function(values) {
    var area, dotGap, gradientW, h, line, maxDate, maxValue, minDate, minGap, minValue, offset, p, w, xAxis, yAxis;

    values = _.filter(values, function(d) {
      return d.question === "Transport" && d.profil === "Femme";
    });
    _.each(values, function(d) {
      d.date = parse(d.date);
      return d.ratio = parseFloat(d.ratio);
    });
    p = [0, 20, 60, 20];
    minGap = $("html").hasClass("lt-ie9") ? 80 : 40;
    dotGap = Math.max(minGap, wrapperWidth / (values.length - 1));
    w = (dotGap * (values.length - 1)) - p[1] - p[3];
    h = wrapperHeight - p[0] - p[2];
    gradientW = (w / (values.length - 1)) * 2;
    x.range([0, w]);
    y.range([h, 0]);
    xAxis = d3.svg.axis().scale(x).tickSize(1).tickPadding(10).tickFormat(dateFormat).ticks(d3.time.months, 2);
    yAxis = d3.svg.axis().scale(y).tickSize(1).orient("right");
    area = d3.svg.area().interpolate("linear").x(function(d) {
      return x(d.date);
    }).y0(h).y1(function(d) {
      return y(d.ratio);
    });
    line = d3.svg.line().interpolate("linear").x(function(d) {
      return x(d.date);
    }).y(function(d) {
      return y(d.ratio);
    });
    minDate = d3.min(values, function(d) {
      return d.date;
    });
    maxDate = d3.max(values, function(d) {
      return d.date;
    });
    minValue = d3.min(values, function(d) {
      return d.ratio;
    });
    maxValue = d3.max(values, function(d) {
      return d.ratio;
    });
    offset = (maxValue - minValue) * 0.3;
    x.domain([minDate, maxDate]);
    y.domain([minValue - offset, maxValue + offset]).nice();
    svg = d3.select($rootElement.find(".chart")[0]).append("svg:svg").attr("width", w + p[1] + p[3]).attr("height", h + p[0] + p[2]).append("g").attr("transform", "translate(" + p[3] + "," + p[0] + ")");
    if (!Modernizr.svg) {
      svg.append("svg:path").attr("class", "area bg").attr("fill", "#ee9807").attr("d", area(values));
    } else {
      svg.append("linearGradient").attr("id", "sequence-gradient").attr("gradientUnits", "userSpaceOnUse").attr("spreadMethod", "repeat").attr("y1", 0).attr("x1", 0).attr("y2", 0).attr("x2", gradientW).selectAll("stop").data([
        {
          offset: "0%",
          color: "#ED9B0B",
          offset: "50%",
          color: "#F2B84D",
          offset: "51%",
          color: "#EA9806",
          offset: "100%",
          color: "#B3750E"
        }
      ]).enter().append("stop").attr("offset", function(d) {
        return d.offset;
      }).attr("stop-color", function(d) {
        return d.color;
      });
      svg.append("svg:path").attr("class", "area bg").attr("fill", "url(#sequence-gradient)").attr("d", area(values));
    }
    svg.selectAll(".data-point").data(values).enter().append("svg:circle").attr("class", "data-point").attr("cx", function(d) {
      return x(d.date);
    }).attr("cy", function(d) {
      return y(d.ratio);
    }).attr("fill", "#EE9807").attr("stroke-width", 3).attr("stroke", "#ffffff").attr("r", 5);
    svg.append("g").attr("class", "x axis").attr("transform", "translate(0, " + (h + 15) + ")").call(xAxis);
    svg.selectAll(".x.axis g text").each(insertLinebreaks);
    return svg.selectAll(".x.axis g text").attr("font-size", 16);
  };
  return update();
};

AnswerGraphCtrl.$inject = ['$scope', '$http', '$rootElement', '$routeParams', '$location'];
