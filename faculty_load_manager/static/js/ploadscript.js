$(document).ready(function() {
    $("table").each(function() {
        var $this = $(this);
        var newrows = [];
        $this.find("tr").each(function(){
            var i = 0;
            $(this).find("td, th").each(function(){
                i++;
                if(newrows[i] === undefined) { newrows[i] = $("<tr></tr>"); }
                if(i == 1)
                    newrows[i].append("<th>" + this.innerHTML  + "</th>");
                else
                    newrows[i].append("<td>" + this.innerHTML  + "</td>");
            });
        });
        $this.find("tr").remove();
        $.each(newrows, function(){
            $this.append(this);
        });
    });
    
    $("td").click(function(e) {
        var chk = $(this).closest("td").find("input:checkbox").get(0);
        if(e.target != chk)
        {
            chk.checked = !chk.checked;
            if ($(this).closest("td").find("input:checkbox").prop("checked") == true) {
                $(this).closest("td").css("background-color","red");
                console.log($(this).closest("td").find("input:checkbox").prop("checked"));
                console.log($(this).closest("td").find("input:checkbox").prop("value"));
            }
            else {
                $(this).closest("td").css("background-color","white");
                console.log($(this).closest("td").find("input:checkbox").prop("checked"));
                console.log($(this).closest("td").find("input:checkbox").prop("value"));
            }
        }
    });
});