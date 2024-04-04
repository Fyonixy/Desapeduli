$(document).ready(function(){
    comproses("proses")
})

function comproses (con){
    $("#opt").empty()
    $("#data").empty()
    if(con == 'proses'){
        let opt = `<button class="mark" onclick="comproses('proses')">Data Laporan</button>
        <button onclick="comproses('selesai')">Laporan Selesai</button>`
        $("#opt").append(opt)
    }else{
        let opt = `<button onclick="comproses('proses')">Data Laporan</button>
        <button class="mark" onclick="comproses('selesai')">Laporan Selesai</button>`
        $("#opt").append(opt)

    }
    $.ajax({
        url : `/comproses?con=${con}`,
        type : "GET",
        success : function(response){
            let data = response["data"]
            if(con == 'proses'){
                for(let i of data){
                    let id_pengaduan = i["id_pengaduan"]
                    let tanggal_pengaduan = i["tgl_pengaduan"]
                    let status = i["status"]
                    let html = `<tr>
                    <td>${id_pengaduan}</td>
                    <td>${tanggal_pengaduan}</td>
                    <td>${status}</td>
                    <td><a href="/tanggapan/${id_pengaduan}">Tanggapi</a></td>
                </tr>`
                $('#data').append(html)
                }
            
            }else{
                for(let i of data){
                    let id_pengaduan = i["id_pengaduan"]
                    let tanggal_pengaduan = i["tgl_pengaduan"]
                    let status = i["status"]
                    let html = `<tr>
                    <td>${id_pengaduan}</td>
                    <td>${tanggal_pengaduan}</td>
                    <td>${status}</td>
                    <td><a href="/tanggapan/${id_pengaduan}">Cek</a></td>
                </tr>`
                $('#data').append(html)
                }
            }
        }
    })
}