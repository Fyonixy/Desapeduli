function send(){
    let text = $('#input').val()
    if(text){
        let fileInput = $('#gambar').prop('files')[0]
        let form_data = new FormData()
        form_data.append("text" ,text)
        form_data.append("image" ,fileInput)
        $("#send").prop("disabled" , true)
        $.ajax({
            url: `/sendcom`,
            type : 'POST',
            contentType : false,
            processData : false,
            data : form_data,
            success: function(response){
                console.log(response)
                $('#input').val("") 
                $('#gambar').val("")
                $('#labelgambar').text("Tambahkan Gambar")
                $("#gambar").prop("disabled", false)
                $("#send").prop("disabled" , false)
            }
        })
    }else{
        console.log("pengiriman gagal")
    }
    
}
function get(){
    $("#data").empty()
    $(".buttons").empty()
    let buttons = `
    <button onclick="btnpost()" class="off" >Kirim Laporan</button>
    <button onclick="get()" class="on" >Laporan Terkirim</button>
    `
    $(".buttons").append(buttons)
    $.ajax({
        url : "/getcom",
        type : "GET",
        success : function(response){
            if(response["data"]){
                let data = response["data"]
                for(let i of data){
                    let html = `
                        <div class="box-get" >
                            <div class="box-top">                            
                                <p>${i["nik"]}</p>
                                <p>${i["tgl_pengaduan"]}</p>
                            </div>
                            <div class="box-mid">
                                <p>Status : ${i["status"]}</p>
                                <p>Isi_laporan : ${i["isi_laporan"]}</p>
                                <a href="/cektanggapan/${i["id_pengaduan"]}"><button>Cek Tanggapan</button></a>
                            </div>
                            <div class="box-image">
                                <img src="${i["foto"]}">
                            </div>
                        </div>`
                    $("#data").append(html)
                }
            }else{
                let html = `<div><p>${response["error"]}</p></div>`
                $("#data").append(html)
            }
            
        }
    })
}

function btnpost(){
    $("#data").empty()
    $(".buttons").empty()
    let buttons =   `
        <button onclick="btnpost()" class="on" >Kirim Laporan</button>
        <button onclick="get()" class="off" >Laporan Terkirim</button>`
    let html = `
        <textarea id="input" placeholder="Masukan laporan anda di dalam kolom yang sudah diberikan"></textarea>
        <div class="file-upload">
            <input type="file" id="gambar" name="gambar" accept="image/*" multiple="false">
            <label for="gambar">Tambahkan Gambar</label>
            <button onclick="send()">Kirim</button>

        </div>
    `
    $(".buttons").append(buttons)
    $("#data").append(html)
}

function upimage(input) {
    console.log(input.files[0].name)
    if (input.files && input.files[0]) {
        $("#gambar").prop("disabled", true);
        $("#labelgambar").text(input.files[0].name);
    }
}