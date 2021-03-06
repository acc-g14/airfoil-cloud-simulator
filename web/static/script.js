var preText = {};
preText["n0"] = "NACA1";
preText["n1"] = "NACA2";
preText["n2"] = "NACA3";
preText["n3"] = "NACA4";
preText["min_angle"] = "Angle start";
preText["max_angle"] = "Angle stop";
preText["step"] = "Angle step size";
preText["num_nodes"] = "Number of nodes in airfoil";
preText["refinement_level"] = "Number of refinement steps";
preText["num_samples"] = "Simulation samples";
preText["viscosity"] = "Simulation viscosity";
preText["speed"] = "Simulation speed";
preText["time"] = "Simulation time";
var chartMap = {}
var jobId = "";
function clearArea(id, message) {
    if ($(id).val() == message) {
        $(id).val("");
        $(id).css("color", "#ffffff");
    }
}

function fillArea(id, message) {
    if ($(id).val() == "") {
        $(id).val(message);
        $(id).css("color", "#444444");
    }
}

$(document).ready(function () {
    for (key in preText) {
        var value = preText[key];
        $("#" + key).val(value);
        //$("#" + key).focus(createClojure(key, value, clearArea));
        //$("#" + key).focusout(createClojure(key, value, fillArea));
    }

    $("#airfoil-form").submit(function (e) {
        var data = {}

        for (key in preText) {
            data[key] = $("#" + key).val();
        }

        //$("#airfoil-form").remove();
        $("#sliding_new_job_div").slideUp("fast");

        var job = $.post("job", data);

        job.done(function (data) {
            jobId = data.job_id;
            //$("#content").append("<pre id='jsonDiv'></pre>");
            //TODO: Update correct elements
            //updateJobResult();
        });

        return false;
    });

});

$(document).ready(function () {
    setInterval(function () {
        $.get("/status").success(function (data) {
        $("#workers_active").html(data.num_workers);
        $("#running_tasks").html(data.running_tasks);
    })
    }, 2000)
})


function updateJobResult(jobId) {
    var jobResult = $.get("job/" + jobId + "/result");

    jobResult.done(function (data) {
        $("#results-" + jobId).html(jobId + " " + JSON.stringify(data, null, 4));
        jobInfo = data
        //$("#results-" + jobId).html("Job ID: + " " + jobId + " Finished tasks: " + jobInfo["finished_tasks"] +
        // " Results: " + jobInfo = {results: {angle: angleVal; lift: liftVal; drag: dragVal}} + " "); // RESULTS IS A LIST

        //$(#results-" + jobId).html

        //Updating the results for current job results
        var results_div = $("#results-" + jobId);

        //var tableClass = ???;
        //var trClass = ???;
        //var thClass = ???;
        //var tdClass = ???; //Modify following code to include specific styling.
        var results_table = "<table class='table'>";
        results_table += "<tr><th>Angle</th><th>Lift</th><th>Drag</th></tr>";

        min = Number.MAX_VALUE;
        max = Number.MIN_VALUE;
        liftData = [];
        dragData = [];
        for (i=0; i<jobInfo.results.length; i++) {
            result = jobInfo.results[i];
            results_table += "<tr><td>" + result.angle + "</td><td>" + result.lift + "</td><td>" + result.drag + "</td></tr>";
            liftData.push([result.angle, result.lift]);
            dragData.push([result.angle, result.drag]);
            if (result.angle < min) {
                min = result.angle;
            }
            if (result.angle > max) {
                max = result.angle;
            }
        }
        results_table += "</table>";
        results_div.html(results_table);

        //{finished_tasks: finishedTasksVal; total_tasks: totalTasksVal}
        //Updating the status for current job
        var status_div = $("#status-" + jobId);

        var status_table = "<table class='table'>";
        var total_tasks = jobInfo["total_tasks"];
        var finished_tasks = jobInfo["finished_tasks"];

        var runtime = jobInfo["runtime"];


        status_table += "<tr><td>Total tasks</td><td>" + total_tasks + "</td></tr>";
        status_table += "<tr><td>Finished tasks</td><td>" + finished_tasks + "</td>";
        var progressObj = $('#progress-' + jobId)
        if(total_tasks==finished_tasks) {
            status_table += "<tr><td>Runtime</td><td>" + runtime + "</td>";
            progressObj.removeClass("label-warning")
            progressObj.addClass("label-success")
            progressObj.html("Finished")

        } else {
            status_table += "<tr><td>Runtime</td><td>In progress</td>";
            progressObj.addClass("label-warning")
            progressObj.removeClass("label-success")
            progressObj.html("In Progress")
        }
        status_table += "</table>";

        status_table += "<button type='button' class='btn btn-danger' id='delete-"+jobId+"' >Delete job</button>";

        status_div.html(status_table);

        $("#delete-"+jobId).click(function() {
                $.ajax({
                    url: '/job/' + jobId,
                    type: 'DELETE',
                    success: function () {
                        console.log("element deleted");
                        $("#job-"+jobId).remove();
                    }
                })
        }
        )


        c = chartMap[jobId]
        console.log(c)
        c[0].xAxis[0].setExtremes(min, max, false);
        c[0].series[0].setData(liftData, true);
        c[1].xAxis[0].setExtremes(min, max, false);
        c[1].series[0].setData(dragData, true);
        console.log(data)
        setTimeout(function() {
            updateJobResult(jobId)
        }, 1000);
    });
}

//TODO: When loading the service_status page, update the values.

function createClojure(k, v, f) {
    return function (e) {
        f("#" + k, v);
    }
}

$(function () {
    $("#new_job_btn").click(function () {
            //$("#sliding_new_job_div").css("display", "block")
            $("#sliding_new_job_div").slideToggle("slow")
            //alert('button clicked mmf');
        }
    )
    $("#jobs_list").delegate(".job_id", "click", function () {
        var el = $(this);
        el.parent().toggleClass("panel-primary")
        var job_id = el.find("a").text();
        $.get("job/" + job_id + "/parameters").success(function (data) {
            console.log(el)
            var infoElement = el.parent().find(".job_parameters");
            infoElement.html(data);
            el.parent().find(".panel-body").toggle();
        });
        //TODO: Update for onmousedown to trigger a function that collects the relevant data for selected job-ID and

    });
    var listElements = []
    setInterval(function () {
        $.get("existing_jobs").success(function (data) {
            element = $("#jobs_list");
            data = JSON.parse(data);
            for (var index in data) {
                var obj = data[index];
                if (listElements.indexOf(obj) == -1) {

                    var htmlElement = '<div class="job_item list-group-item" id="job-' + obj + '">';
                    htmlElement += '<div class="panel"><div class="job_id panel-heading"><a>' + obj + '</a><span id="progress-'+obj+'" class="label pull-right" style="margin-top:3px;margin-right:10px;"></span></div>'
                    htmlElement += '<div class="job_item_info panel-body" style="display: none">'
                    htmlElement +=
                        '<div><ul class="nav nav-tabs" role="tablist"> \
                        <li role="presentation" class="active"><a href="#status-'+obj+'" aria-controls="status" role="tab" data-toggle="tab">Status</a></li> \
                        <li role="presentation"><a href="#parameters-'+obj+'" aria-controls="parameters" role="tab" data-toggle="tab">Parameters</a></li>\
                        <li role="presentation"><a href="#results-'+obj+'" aria-controls="results" role="tab" data-toggle="tab">Results</a></li>\
                        <li role="presentation"><a href="#lift_graph-'+obj+'" aria-controls="settings" role="tab" data-toggle="tab">Lift force graph</a> </li>\
                        <li role="presentation"><a href="#drag_graph-'+obj+'" aria-controls="settings" role="tab" data-toggle="tab">Drag force graph</a> </li>\
                        </ul></div>\
                        <div class="tab-content">\
                        <div role="tabpanel" class="tab-pane active" id="status-'+obj+'">Status</div>\
                        <div role="tabpanel" class="tab-pane job_parameters" id="parameters-'+obj+'">Parameters</div>\
                        <div role="tabpanel" class="tab-pane" id="results-'+obj+'">Results</div>\
                        <div role="tabpanel" class="tab-pane" id="lift_graph-'+obj+'"><div id="lift_chart-'+obj+'" style="height:500px"></div></div>\
                        <div role="tabpanel" class="tab-pane" id="drag_graph-'+obj+'"><div id="drag_chart-'+obj+'" style="height:500px"></div></div>\
                        </div></div></div></div>'
                        element.append(htmlElement);
                        var lift_chart = new Highcharts.Chart({
                            chart: {
                                renderTo: 'lift_chart-' + obj,
                                type: 'line'
                            },
                            title: {
                                text: 'Job: ' + obj
                            },
                            xAxis: {
                                title: {
                                    text: 'Angle'
                                }
                            },
                            yAxis: {
                                title: {
                                    text: ''
                                }
                            },
                            series: [{
                                name: 'Lift force (avg)',
                                data: []
                            }]
                        });
                        var drag_chart = new Highcharts.Chart({
                            chart: {
                                renderTo: 'drag_chart-' + obj,
                                type: 'line'
                            },
                            title: {
                                text: 'Job: ' + obj
                            },
                            xAxis: {
                                title: {
                                    text: 'Angle'
                                }
                            },
                            yAxis: {
                                title: {
                                    text: ''
                                }
                            },
                            series: [{
                                name: 'Drag force (avg)',
                                data: []
                            }]
                        });


                        chartMap[obj] = [lift_chart, drag_chart]
                        updateJobResult(obj);
                    listElements.push(data[index])
                }

                //TODO: update chart
            }
        })
    }, 1000)

        });