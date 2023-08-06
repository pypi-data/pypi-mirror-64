var tkMaxID = 1;
var tkStartTime = Date.now();
var tkTimeEnable=false;
function tk_id(tk_input) {
    return tk_input.substring(7);
}
function getTrack() {
    $.getJSON("../Track/Last")
            .done(function (json) {
                if (typeof json.Log.Log !== 'undefined') {//This will be false if the Task name itself is "Last"
                    json = json.Log;
                }
                if (typeof json.Start !== 'undefined') {
                    $("#tf_act").text(json.Log);
                    var d=new Date(json.Start*1000);
                    tkStartTime=d.getTime();
                    tkTimeEnable=true;
                    console.log("JSON Data!: " + json.Log + json.Start);
                    
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");

//                alert("Failed");
            });
}
function addTrack(name) {
    $.getJSON("../pTrack/" + encodeURIComponent(name))
            .done(function (json) {
                if (typeof json.Log !== 'undefined') {
                    $("#tf_act").text(json.Log);
                    console.log("JSON Data: " + json.Log + json.Start);
                    tkStartTime = Date.now();
                    tkTimeEnable=true;
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");
//                alert("Failed");
            });
}
function addTask() {
    $.getJSON("../pTask/" + encodeURIComponent(jQuery("#tk_txt").val()))
            .done(function (json) {
                if (typeof json.Log !== 'undefined') {
                    jQuery("#tk_txt").val("");
                    $("#tk_lis").prepend(taskHTML(json.Log));
                    console.log("JSON Data: " + json.Log);
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
toastr.error("Failed");
                //                alert("Failed");
            });
}
function destroyTask() {
    $.getJSON("../dTask/All")
            .done(function (json) {
                emptyTaskList();
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Failed");
//                alert("Failed");
            });
}
function emptyTaskList() {
    $("#tk_lis").html("");
}
function addTaskList(name) {
    $("#tk_lis").append(taskHTML(name));
}
function taskHTML(name) {
    tkMaxID += 1;  //WILL RUN INTO PROBLEMS AT 1000  
    var nexttkID = ('000' + tkMaxID).substr(-3);
    return `<li id="tk_lis_${nexttkID}">
                                                <small class="btn-sm btn-primary tk_ply" id="tk_ply_${nexttkID}"><i class="fa fa-play"></i></small>
                                                <!-- drag handle -->
                                                <span class="handle">
                                                    <i class="fas fa-ellipsis-v"></i>
                                                    <!--<i class="fas fa-ellipsis-v"></i>-->
                                                </span>
                                                
                                                <!-- todo text -->
                                                <span class="text tk_tsk" id="tk_tsk_${nexttkID}">${name}</span>
                                                <!-- Emphasis label -->
                                                <!--<small class="badge badge-danger"><i class="far fa-clock"></i>1</small>-->
                                                <!-- General tools such as edit or delete-->
                                                <div class="tools">
                                                    <i class="fas fa-clock"></i>
                                                    <i class="fas fa-chart-bar"></i>
                                                    <i class="fas fa-trash"></i>
                                                </div>
                                            </li>`;
    `<li>
                                                <!-- drag handle -->
                                                <span class="handle">
                                                    <i class="fas fa-ellipsis-v"></i>
                                                    <i class="fas fa-ellipsis-v"></i>
                                                </span>
                                                <!-- checkbox -->
                                                <div  class="icheck-primary d-inline ml-2">
                                                    <input type="checkbox" value="" name="todo1" id="todoCheck1">
                                                    <label for="todoCheck1"></label>
                                                </div>
                                                <!-- todo text -->
                                                <span class="text">${name}<i class="fas fa-circle-notch fa-spin"></i></span>
                                                <!-- Emphasis label -->
                                                <small class="badge badge-danger"><i class="far fa-clock"></i>1</small>
                                                <!-- General tools such as edit or delete-->
                                                <div class="tools">
                                                    <i class="fas fa-edit"></i>
                                                    <i class="fas fa-trash-o"></i>
                                                </div>
                                            </li>
                                            `;
}
function getTask() {
    $.getJSON("../Task/All")
            .done(function (json) {
                if ((typeof json.Data !== 'undefined') && json.Data !== "Dead") {
                    emptyTaskList();
                    $.each(json.Data, function (i, task) {
                        if (i === 20) {
                            return false;
                        }
                        addTaskList(task.Log);
                        console.log(i + ": " + task.Log);
                    });
                } else {
                    console.log("Couldn't Parse Response Properly");
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed: " + err);
                toastr.error("Couldn't Connect Properly");
//                alert("Couldn't Connect Properly");
            });
}
function reListen() {
    toastr.info('Version 1');
    emptyTaskList();
    getTask();
    getTrack();
    jQuery(document).on('click', '.tk_add', function () {
        addTask();

    });
    jQuery(document).on('keyup', '#tk_txt', function () {
        if (event.keyCode === 13) {
            addTask();
        }
    });
    jQuery(document).on('click', '.tk_ply', function () {
        var tk_current_id = tk_id(jQuery(this).attr('id'));
        if ((parseInt(tk_current_id) || 0) !== 0) {
            txt = jQuery("#tk_tsk_" + tk_current_id).text();
            console.log(txt);
            addTrack(txt);
        } else {
            addTrack(jQuery("#tk_txt").val());
        }


    });
    jQuery(document).on('click', '.tk_dst', function () {
        destroyTask();
    });
    setInterval(updateTimer, 1000);


}
function updateTimer(){
    if (tkTimeEnable){
        var seconds = Math.round((Date.now() - tkStartTime) / 1000); //in ms 
        var hours = ("0" + Math.floor(seconds / 3600)).slice(-2);
        seconds %= 3600;
        var minutes = ("0" + Math.floor(seconds / 60)).slice(-2);
        seconds = seconds % 60;
        seconds =  ("0" + seconds).slice(-2);
        jQuery("#tf_tim").text(hours+":"+minutes+":"+seconds);
    }
}
jQuery(document).ready(function () {
    reListen();


});