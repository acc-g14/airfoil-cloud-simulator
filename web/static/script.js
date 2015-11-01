/**
 * Created by Mange on 01/11/15.
 */
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

$(document).ready(function() {
    for (key in preText) {
        var value = preText[key];
        $("#" + key).val(value);
        //$("#" + key).focus(createClojure(key, value, clearArea));
        //$("#" + key).focusout(createClojure(key, value, fillArea));
    }

    $("#airfoil-form").submit(function(e) {
        var data = {}

        for (key in preText) {
            data[key] = $("#" + key).val();
        }

        //$("#airfoil-form").remove();
        $("#sliding_new_job_div").slideUp("fast");

        var job = $.post( "job", data );

        job.done(function( data ) {
            jobId = data.job_id;
            //$("#content").append("<pre id='jsonDiv'></pre>");
            //TODO: Update correct elements
            updateJobResult();
        });

        return false;
    });

});

//TODO: Adjust for current implementation
function updateJobResult() {
    var jobResult = $.get( "job/" + jobId + "/result");

    jobResult.done(function( data ) {
        //$("#jsonDiv").html(jobId + " " + JSON.stringify(data, null, 4));
        console.log(data)
        setTimeout(updateJobResult, 100);
    });
}

//TODO: When loading the service_status page, update the values.

function createClojure(k, v, f) {
    return function(e) {
        f("#" + k, v);
    }
}

$(function() {
            $("#new_job_btn").click( function() {
                        //$("#sliding_new_job_div").css("display", "block")
                        $("#sliding_new_job_div").slideToggle("slow")
                        //alert('button clicked mmf');
                    }
            );
            $(".job_list_div").mouseover( function() {
                $(this).css("background-color", "#ffffff");
                    }
            );
            $(".job_list_div").mouseout( function() {
                $(this).css("background-color", "#fafafa");
                    }
            );

            //TODO: Update for onmousedown to trigger a function that collects the relevant data for selected job-ID and
            // displays the data in the bottom table.
        });