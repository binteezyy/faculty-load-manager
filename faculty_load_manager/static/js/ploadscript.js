$(document).ready(function() {
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