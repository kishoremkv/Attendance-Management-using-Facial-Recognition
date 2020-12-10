const SERVER_URL = "localhost:8000//attendance/"
let attendance_dict = {}
let selected_date,selected_class,selected_period,selected_section;


function drawTable() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Roll No');
    data.addColumn('string', 'Branch');
    data.addColumn('string', 'Section');
    data.addColumn('string', 'Period');
    data.addColumn('string', 'Date');
    data.addColumn('string', 'Time');
    data.addColumn('boolean', 'Status');

    attendance_list  = []

    for(var i=0;i<attendance_dict.length;i++)
    {
        cur_dict = attendance_dict[i]
        cur_list = []
        cur_list.push(cur_dict['roll_no'])
        cur_list.push(cur_dict['branch'])
        cur_list.push(cur_dict['section'])
        cur_list.push(cur_dict['period'])
        cur_list.push(cur_dict['date'])
        cur_list.push(cur_dict['time'])
        cur_list.push(cur_dict['status']=='Absent'?false:true)
        attendance_list.push(cur_list)
    }
    console.log(attendance_list)
    data.addRows(attendance_list);

    var table = new google.visualization.Table(document.getElementById('table_div'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
}



$(document).on('change', '#selected_date',function()
{
    selected_date = $(this).val()
    console.log(selected_date)
    // var temp = "<div id = 'all_classes'><button id ='classes' class = 'btn btn-dark'>Display All Classes</button>";
    // temp+= "<div class = 'container'><div class = 'row' style = 'padding:2%'><div class = 'col-sm-4'><h4>All Classes</h4></div><div class = 'col-lg-4'><h4>Select Section</h4></div></div></div>"
    // $("#side_bar").empty()
    // $("#side_bar").append(temp)
    $("#all-info").css("display","block");

    $.post("/attendance/display",
    function(response,status)
    {
        if(status ==="success")
        {
            var classes = response.data
            var options = " <option  class = 'form-control' disabled selected value>--</option>"
            for(let i =0;i<classes.length;i++)
            {
                options+="<option id = 'classes_"+i+"' index = '"+i+"' class = 'form-control'>"+classes[i]+"</option>"
            }
            $("#classes-info select").empty()
            $("#classes-info select").append(options)
        }
    }
    )
    

})


$(document).on("change","#classes-info select",function()
{
    console.log("classes select")

    selected_class= $("#classes-info select").find(":selected").text()
    console.log("seleted class: "+selected_class)
    $.post("/attendance/display",
    {"section_info":selected_class},
    function(response,success)
    {
        var all_sections = response.data
        var options = " <option  class = 'form-control' disabled selected value>--</option>"
        for(let i =0;i<all_sections.length;i++)
        {
            options+="<option id = 'section_"+i+"' index = '"+i+"' class = 'form-control'>"+all_sections[i]+"</option>"
        }
        $("#section-info select").empty()
        $("#section-info select").append(options)
    }
    )

})

$(document).on("change","#section-info select",function()
{
    selected_section= $("#section-info select").find(":selected").text()
    console.log("seleted section: "+selected_section)
    var options = " <option  class = 'form-control' disabled selected value>--</option>"
    for(let i =0;i<7;i++)
    {
        options+="<option id = 'period_"+i+"' index = '"+i+"' class = 'form-control'>"+(i+1)+"</option>"
    }
    $("#period-info select").empty()
    $("#period-info select").append(options)

})

$(document).on("change","#period-info select",function()
{
    selected_period= $("#period-info select").find(":selected").text()
    console.log("seleted period: "+selected_period)
    $.post("/attendance/display",
    {
        "class_name":selected_class,
        "section_no":selected_section,
        "period_no" :"period"+selected_period,
        "date":selected_date
    },
    function(response,success)
    {
        if(success==="success")
        {
            attendance_dict = response.data
            google.charts.load('current', {'packages':['table']});
            google.charts.setOnLoadCallback(drawTable);
        }
    }
    )

})