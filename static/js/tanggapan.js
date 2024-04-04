function send(id){
    let text = $("#input").val()
    $.ajax({
        url : "/sendtanggapan",
        type : "POST",
        data : {
            text : text,
            id : id
        },
        success : function(response){
            location.reload()
        }
    })
}