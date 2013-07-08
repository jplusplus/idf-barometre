
QuestionListCtrl = ($scope, $rootElement, Introduction, ArrowColor)->    
    $scope.introductions = Introduction.query()
    # Unable the arrow color service
    ArrowColor.active = false

QuestionListCtrl.$inject = ['$scope', '$rootElement', 'Introduction', 'ArrowColor'];

# the dialog is injected in the specified controller
DialogCtrl = ($scope, dialog)->
  $scope.close = -> dialog.close();
  
DialogCtrl.$inject = ['$scope', 'dialog'];

HeaderCtrl = ($scope, $dialog)->        
    $scope.opts =
        backdrop: true
        keyboard: true
        backdropClick: true
        dialogFade: true
        backdropFade: true
        templateUrl:  './partial/dialog.html'
        controller: 'DialogCtrl'
    
    $scope.openDialog = ->      
        d = $dialog.dialog($scope.opts)
        d.open()

HeaderCtrl.$inject = ['$scope', '$dialog'];

ActiveColorCtrl = ($scope, ArrowColor)->
    $scope.state  = ArrowColor
    $scope.getClass = ->
        return if $scope.state.active then "question-" + $scope.state.question else ""

ActiveColorCtrl.$inject = ['$scope', 'ArrowColor'];
    
AnswerGraphCtrl = ($scope, $rootElement, $routeParams, $location, $filter, Answer, ArrowColor)->
    # Models attributes
    $scope.question = $routeParams.q or "economique"
    $scope.profil   = $routeParams.p or "all"
    # List of active point
    $scope.activePoints = {}
    $scope.activePointsCount = -> _.keys($scope.activePoints).length
    # Unable the arrow color service
    ArrowColor.active = true

    # Graph attributes
    chartSvg   = {}
    yAxisSvg   = {}    
    parse      = d3.time.format("%m/%Y").parse
    dateFormat = (d)-> getMonth(d) + " " + (d.getFullYear()-2000)
    # Empty shortcuts
    wrapper = chart = axis = $(null)    
    # This dead IE required that we create jscrollpane here
    unless Modernizr.svg 
        # Add customise scrollbar
        $rootElement.find(".wrapper").jScrollPane hideFocus: true    
    # Saves wrap
    wrapperWidth  = 549
    wrapperHeight = 330
    tickSize      = 5
    padding       = [10, 18, 60, 18]
    minGap        = 40

    # Scales and axes. Note the inverted domain for the y-scale: bigger is up!
    x = d3.time.scale()
    y = d3.scale.linear()

    
    update = -> 
        params = profil: $scope.profil, question: $scope.question
        $scope.answers = Answer.query params, render
        # Update the ArrowColor service
        ArrowColor.question = $scope.question

    getMonth = (d)->
        return [
            "Jan.",
            "Fév.",
            "Mar.",
            "Avr.",
            "Mai.",
            "Jun.",
            "Jul.",
            "Aoû.",
            "Sep.",
            "Oct.",
            "Nov.",
            "Déc."
        ][d.getMonth()] or d3.time.format("%b")(d)

    loadShortcuts = ->
        wrapper = $rootElement.find(".wrapper")
        chart   = $rootElement.find(".chart")
        axis    = $rootElement.find(".yaxis")

    closestActivePoints = (ref)->
        ref = parseInt(ref)
        # By default the closest key is a very big number
        closestDist = Math.pow(99,99)
        # Get all keys
        keys = _.keys($scope.activePoints)
        # Take the first key by default
        closest = keys[0] 
        # Look every key
        _.each keys, (k)->
            # Distance to the reference index
            dist = Math.abs(parseInt(k)-ref)
            # If the new distance is smaller
            if dist > 0 and dist < closestDist
                closestDist = dist
                # Take the key as closest key
                closest = k
            
        # Return the closest key
        return parseInt(closest)

    point =      
        offset: (d)-> 
            wrapper = $rootElement.find(".wrapper")
            return {
                left : x(d.date) + padding[3]
                top  : y(d.ratio) 
            }
        setTrend: (d)->
            # Keys list sortted by key
            keys = _.sortBy _.keys($scope.activePoints), (d, key)->key
            # Only if there is enougth data
            unless keys.length < 2
                fst = $scope.activePoints[ keys[0] ]
                snd = $scope.activePoints[ keys[1] ]
                # First and second values substracted to know the trend
                val  = snd.ratio
                val -= fst.ratio
                # Sets the trend attribute into the scope
                $scope.trend = val
            else
                # Sets the trend to false to disable it
                $scope.trend = false
        tips:
            update: ()->                
                # Update the existing activePoint
                _.each $scope.activePoints, (d, key)->
                    # Update the data within activePoints
                    $scope.activePoints[key] = $scope.answers.rows[key]
                # Render the tips
                point.tips.clean()
            clean:->
                # For each point's tips
                # look for the useless ones
                $(".point-tips").each (key, tip)-> 
                    $tip  = $(tip) 
                    index = $tip.data("point")
                    # Find its dot
                    dots = chartSvg.selectAll(".data-point")    
                    dot  = d3.select dots[0][index]                     
                    # The point isn active
                    unless $scope.activePoints[index]
                        # Remove the inative point
                        $tip.remove()
                        # Change it dot color
                        dot.attr "fill", $filter("colors")($scope.question)
                    else
                        # Activate the tip
                        $tip.addClass("active")
                        # Change it dot color
                        dot.attr "fill", "#323c45"

                # For each activepoint,
                # look for the missing tips                
                _.each $scope.activePoints, point.tips.add

            empty:->
                $scope.activePoints = {}
                point.tips.clean()
                $scope.$apply()

            add: (d, index)->
                $tips = $(".point-tips[data-point=" + index + "]")
                $point = $(chartSvg.selectAll(".data-point")[0][index]) 
                # tips doenst exist yet
                if $tips.length is 0
                    # Create the tips
                    $tips = $("<div class='point-tips' data-point='" + index + "' />") 
                    # offset of the point according its data
                    offset = point.offset(d);     
                    # add a class to the first point
                    $tips.addClass "js-first" if parseInt(index) == 0 
                    # add a class to the last point
                    $tips.addClass "js-last" if parseInt(index) == $scope.answers.rows.length - 1 
                    # Positionate the tips to under the mouse
                    $tips.css
                        left: offset.left
                        top:  offset.top
                    # Appends the tips to the bodu
                    $tips.appendTo wrapper.find(".jspPane")
                # tips exists
                else        
                    # offset of the point according its data
                    offset = point.offset(d);      
                    # Positionate the tips to under the mouse
                    $tips.css
                        left: offset.left
                        top:  offset.top
                # In any case, change the content of the tip
                $tips.html "<div class='content'>" + ~~d.ratio + "%</div>"

        toggle: (d, index)->              
            p = d3.select this
            if not d.selected? or d.selected isnt true
                d.selected = true
                p.attr "fill", "#323c45"                
                $scope.activePoints[index] = d
                # if there is more than 2 points
                if $scope.activePointsCount() > 2
                    # Get closest point
                    closestIdx = closestActivePoints(index)
                    closestElt = d3.selectAll(".data-point")[0][closestIdx]
                    # If element exists
                    if closestElt
                        # Unselect it
                        d3.select(closestElt).attr "fill", $filter("colors")($scope.question)
                        delete $scope.activePoints[closestIdx].selected
                        delete $scope.activePoints[closestIdx]

                $scope.$apply()
            else
                d.selected = false
                p.attr "fill", $filter("colors")($scope.question)
                delete $scope.activePoints[index].selected
                delete $scope.activePoints[index]             
                $scope.$apply()

    insertLinebreaks = (d) ->
        el = d3.select(this)
        words = dateFormat(d).split(" ")
        el.text ""
        i = 0

        while i < words.length
            tspan = el.append("tspan").text(words[i])
            tspan.attr("x", 0).attr "dy", "12"  if i > 0
            i++

    getGradientStops = (width, stopWidth)->        
        stops = []
        # Size of each step
        stopsCount = (width/stopWidth)
        # Position in percentage of the given pixels
        pos = (px)-> px/width*100 + "%"
        # For each steps
        for i in [0..stopsCount-1]  
            # Calculate the step start          
            start = (i*stopWidth)
            # And the end
            end   = start + stopWidth
            # Then add to stop by step
            stops.push offset: pos(start), color: $filter("colors")($scope.question, if i%2 then "0" else "51")
            stops.push offset: pos(end),   color: $filter("colors")($scope.question, if i%2 then "50" else "100")

        return stops
        

    render = ()-> 
        loadShortcuts()    
        # Empty container
        chart.empty()
        axis.empty()
        # Update tips
        point.tips.update()        
        # Do we stop
        return false unless $scope.answers.rows? and $scope.answers.rows.length isnt 0                    
        # Parse dates and numbers. We assume $scope.answers is sorted by date.
        _.each $scope.answers.rows, (d) ->
            try 
                return d.date = parse(d.date)  
            # Some parsings fail          
            catch error
                return null

        dotGap    = Math.max(minGap, wrapperWidth / ($scope.answers.rows.length - 1))
        w         = (dotGap * ($scope.answers.rows.length - 1)) - padding[1] - padding[3]
        h         = wrapperHeight - padding[0] - padding[2]        
        stopWidth = (w / ($scope.answers.rows.length-1))*2


  
        # An area generator, for the light fill.
        area = d3.svg.area()
            .interpolate("linear")
            .x((d) -> x(d.date))
            .y0(h)
            .y1((d)-> y(d.ratio))

        # A line generator, for the dark stroke.
        line = d3.svg.line()
            .interpolate("linear")
            .x( (d) -> x(d.date))
            .y( (d) -> y(d.ratio))

        # Compute the minimum and maximum date, and the maximum price.
        minDate  = d3.min $scope.answers.rows, (d)-> d.date
        maxDate  = d3.max $scope.answers.rows, (d)-> d.date        
        minRatio = $scope.answers.question_min
        maxRatio = $scope.answers.question_max        
        offset   = (maxRatio - minRatio) * 0.3
        # Edits min and max according the offset;
        # takes care to not overlap 0 and 100
        minRatio = Math.max(0, minRatio-offset)
        maxRatio = Math.min(100, maxRatio+offset)
        # Extend x/y domains according the max values
        x.domain([minDate, maxDate])
        y.domain([minRatio, maxRatio]).nice()
        # Scales and axes. Note the inverted domain for the y-scale: bigger is up!
        x.range [0, w]
        y.range [h, 0]
        # Only tick for the received values
        dates = _.pluck($scope.answers.rows, "date")        
        xAxis = d3.svg.axis().scale(x).tickSize(tickSize).tickPadding(10).tickFormat(dateFormat).tickValues(dates)
        yAxis = d3.svg.axis().scale(y).tickSize(tickSize).tickPadding(5).tickFormat((d)->d+"%").orient("left")


        chart.css("width",  w + padding[1] + padding[3])

        # Add an SVG element with the desired dimensions and margin.
        chartSvg = d3.select( chart[0] )
                .append("svg:svg")
                    .attr("width",  w + padding[1] + padding[3])
                    .attr("height", h + padding[0] + padding[2])
                    .append("g")
                        .attr("transform", "translate(" + padding[3] + "," + padding[0] + ")")

        # Add an another svg presenting the y axis
        yAxisSvg = d3.select( axis[0] )
                        .append("svg:svg")                        
                            .attr("width",  axis.width())
                            .attr("height", h + padding[0] + padding[2])

        unless Modernizr.svg    
            # Add the area path.
            chartSvg.append("svg:path")
                    .attr("class", "area bg")
                    .attr("stroke-width", "0")
                    .attr("fill", $filter("colors")($scope.question))
                    .attr("d", area($scope.answers.rows))
        # Add stripes
        else           
            # Gradient spreadMethod bug on Safari 
            # cf: http://stackoverflow.com/questions/11434971/svg-lineargradiend-spreadmethod-ignored-by-safari-osx-and-ios            
            # So we repeat the gradientStop instead of use the repeat method
            stops = getGradientStops(x(maxDate), stopWidth/2)

            chartSvg.append("linearGradient")
                    .attr("id", "sequence-gradient")
                    .attr("gradientUnits", "userSpaceOnUse")
                    .attr("spreadMethod", "repeat")
                    .attr("y1", 0)
                    .attr("x1", 0)
                    .attr("y2", 0)
                    .attr("x2", x(maxDate))
                    .selectAll("stop")
                        # Get the gradient stops accoring the size of the gradient and its steps
                        .data(stops)
                        .enter()
                        .append("stop")
                            .attr("offset",     (d)-> d.offset)
                            .attr("stop-color", (d)-> d.color)
            # Add the area path.
            chartSvg.append("svg:path")
                .attr("class", "area bg")
                .attr("fill", "url(#sequence-gradient)")
                .attr("d", area($scope.answers.rows))


        # Add an overlay to catch click on the entire graph but not on the svg
        chartSvg.append("svg:rect")
                    .attr("x", 0)            
                    .attr("y", 0)
                    .attr("width", w)
                    .attr("height", h)
                    .attr("fill", "transparent")
                    .on "click", -> 
                        point.tips.empty() if _.keys($scope.activePoints).length > 1


        # Add line dots
        chartSvg.selectAll(".data-point")
            .data($scope.answers.rows)
            .enter()
            .append("svg:circle")
                .attr("class", "data-point")
                .attr("cx", (d)-> x d.date)
                .attr("cy", (d)-> y d.ratio)
                .attr("fill", $filter("colors")($scope.question))
                .attr("r", 5)
                .attr("stroke-width", 3)
                .attr("stroke", "#ffffff")
                .on("mousemove",  point.tips.add)
                .on("mouseleave", point.tips.clean)
                .on("click",      point.toggle)

        trendDisplay = if _.keys($scope.activePoints).length < 2 then "none" else null
        # Create a group to contain the trend circle
        trend = chartSvg.append("g")
                            .style("display", trendDisplay)
                            .attr("class", "trend")
                            .attr("transform", "translate(#{w/2}, -70)")

        # Appends a circle
        trend.append("svg:circle")
            .attr("r", 25)
            .attr("fill", "#cc0e00")

        # Appends a text
        trend.append("svg:text")
            .attr("y", if Modernizr.svg then 5 else 0)
            .attr("text-anchor", "middle")
            .attr("fill", "#fff")
            .style("font-size", 16)
            .style("font-weight", "bold")
            .text $filter("supPercent")("10%", false)


        # Add the x-axis.
        chartSvg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, #{h + 25-tickSize})")            
            .call xAxis

        # Add the y-axis to an other svg
        yAxisSvg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(#{30+tickSize}, #{padding[0]})")
            .call yAxis    

        # Add axis break line
        chartSvg.selectAll(".axis g text").each insertLinebreaks
        # Removes horizontal lines
        chartSvg.selectAll(".axis path").remove()
        yAxisSvg.selectAll(".axis path").remove()
        # Adjust text size
        chartSvg.selectAll(".axis g text").attr "font-size", 10
        yAxisSvg.selectAll(".axis g text").attr "font-size", 10 
        # Draw ticks
        chartSvg.selectAll(".axis g line").attr "stroke", "#aaa"
        chartSvg.selectAll(".axis g line").attr "stroke-width", 1
        yAxisSvg.selectAll(".axis g line").attr "stroke", "#aaa"
        yAxisSvg.selectAll(".axis g line").attr "stroke-width", 1 
        
        # jscrollpane already exists
        if wrapper.data("jsp")?
            # Reinitialize jscrollpane
            wrapper.data("jsp").reinitialise() 
        else        
            # Add customise scrollbar
            wrapper.jScrollPane hideFocus: true

        # This is the end
        return true

    # Watch for model change to update the graph
    $scope.$watch 'profil',       update
    $scope.$watch 'question',     update    
    $scope.$watch 'activePoints', point.tips.clean, true
    $scope.$watch 'activePoints', point.setTrend, true
    # Watch the controller destruction
    $scope.$on '$destroy', ->
        $scope.activePoints = []
        # Force active point removing     
        point.tips.clean()

    $scope.$on '$routeUpdate', ->
        $scope.question = $location.search().q
        $scope.profil   = $location.search().p
            

AnswerGraphCtrl.$inject = ['$scope', '$rootElement', '$routeParams', '$location', '$filter', 'Answer', 'ArrowColor'];
