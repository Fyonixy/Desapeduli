function opt(v){
    $("#card-c").empty()
    if(v == 1){
        let html = `    <div class="opt">
        <button onclick="opt(1)" class="on">User</button>
        <button onclick="opt(2)" class="off">Admin/Petugas</button>
    </div>
    <form id="myForm" action="/pushform" method="post">
        <input type="text" id="nik" name="nik" placeholder="NIK" required>
        <input type="password" id="password" name="password" placeholder="Password" required>
        <div class="showpassword">
            <input type="checkbox" onclick="showpassword(this)">
            <p>Show Password</p>
        </div>
        <button type="submit" >Kirim</button>
        <p>Belum punya Akun? Daftar sekarang</p>
    </form>
    <a href="/signup"><button>Signup</button></a>
</div>`
        $("#card-c").append(html)
    }else{
        let html = `    <div class="opt">
        <button onclick="opt(1)" class="off">User</button>
        <button onclick="opt(2)" class="on">Admin/Petugas</button>
    </div>
    <form id="myForm" action="/logadmin" method="post">
        <input type="text" id="id" name="id" placeholder="ID Petugas" required>
        <input type="password" id="password" name="password" placeholder="Password" required>
        <div class="showpassword">
            <input type="checkbox" onclick="showpassword(this)">
            <p>Show Password</p>
        </div>
        <button type="submit" >Kirim</button>
</form>`

        $("#card-c").append(html)
    }
}

function showpassword(toogle){
    if(toogle.checked){
        $("#password").attr("type" , "text")
    }else{
        $("#password").attr("type" , "password")
    }
}