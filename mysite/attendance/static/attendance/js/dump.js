function get_html_sections(all_sections,class_id)
{
    var sections = ""
    sections += '<select class = "col-sm-4 form-control" id = "section_'+class_id+'"><option disabled selected value>--</option>'

    for(let x=0;x<all_sections.length; x++)
    {
        var section_id = "section_"+x;
        sections += '<option value="'+x+'" index="'+x+'" id="'+class_id+'_'+section_id+'">'+all_sections[x]+'</option>'; //add the option element as a string
        
    }
    sections+="</select>"
    $(document).on('change',"#section_"+class_id,function()
    {
        var which_section = $("#section_"+class_id).find(":selected").text()
        console.log(which_section)
        console.log(class_id)
        console.log($("#"+class_id).text())
        which_class = $("#"+class_id).text()
        $.post("/attendance/display",
        {
            "class_name":which_class,
            "section_no":which_section,
            "period_no" :"period1",
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
    return sections

}

$(document).on('click', '#classes',function()
{
    $.post("/attendance/display",
    function(data,status)
    {
        if(status==="success")
        {
            var classes = data.data
            var buttons="<div id='row_classes' class = 'container'>";

            console.log(classes)
            for(let i =0;i<classes.length;i++)
            {
                buttons += '<div id="div_class_'+i+'" style= "padding:2%"> <button type="button" class="btn btn-dark col-sm-4" index="'+i+'" id="class_'+i+'">'+classes[i]+'</button></div>'; //add the option element as a string
                (function()
                {
                    var class_id = "class_"+i;
                    $(document).on('click',"#"+class_id,function()
                    {
                        $.post("/attendance/display",
                        {"section_info":classes[i]},
                        function(response,success)
                        {
                            
                            var all_sections = response.data
                            html_sections = get_html_sections(all_sections,class_id)
                            console.log(html_sections)
                            // $("#section_"+class_id).empty()
                            $("#div_"+class_id).append(html_sections)
                        }
                        )
                    })
                }
                )();
                
            
            }
            buttons+="</div>";
            $("#all_classes").append(buttons);
            
        }
    })
})

