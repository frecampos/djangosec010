function mensaje() {
    alert('hola mundo');
}

function validarFormulario() {
    var resp = validarRut();
    if (resp==false) {
        return false;
    }
    resp = validaFecha();
    if (resp==false) {
        return false;
    }
    return true;
}

function validaFecha() {
    var fechaUsuario = document.getElementById('txtFechaNaci').value;
    var fechaSistema = new Date();
    console.log('Fecha Usuario:'+fechaUsuario);
    console.log('Fecha Sistema:'+fechaSistema);
    ///////////////////////////////////////////
    var ano = fechaUsuario.slice(0,4);
    var mes = fechaUsuario.slice(5,7);
    var dia = fechaUsuario.slice(8,10);
    console.log('Año:'+ano);
    console.log('Mes:'+mes);
    console.log('Dia:'+dia);
    var fechaNuevaUsuario = new Date(ano,(mes-1),dia);
    console.log('Nueva Fecha Usuario:'+fechaNuevaUsuario);
    ///////////////////////////////////////////
    if ( fechaNuevaUsuario > fechaSistema) {
        //alert('fecha incorrecta, fecha usuario mayor a la del sistema');
        Swal.fire({
            icon: 'error',
            title: 'fecha de nacimiento',
            text: 'fecha incorrecta, fecha usuario mayor a la del sistema'
          });
        return false;
    }
    ///////////////////////////////////////////
    var elDia= 24*60*60*1000;
    var dife =Math.trunc( (fechaSistema.getTime()-fechaNuevaUsuario.getTime())/elDia);
    console.log('Dias:'+dife);
    var anos = Math.trunc( dife / 365);
    console.log('Años:'+anos);
    if (anos<18) {
        //alert('es menor de edad, solo tiene '+anos+' años');
        Swal.fire({
            icon: 'error',
            title: 'fecha de nacimiento',
            text: 'es menor de edad, solo tiene '+anos+' años'
          });
        return false;
    }
    ////////////////////////////////////////////
    return true;
}
function validarRut() {
    var rut = document.getElementById('txtRut').value;
    if (rut.trim().length==0) {
        //alert('rut en blanco');
        Swal.fire({
            icon: 'error',
            title: 'validacion rut',
            text: 'el rut esta en blanco'
          });
        return false;
    }
    console.log('Rut:' + rut);
    var num = 3;
    var suma = 0;
    for (let index = 0; index < 8; index++) {
        var caracter = rut.slice(index,index+1);
        console.log(caracter+ ' x '+ num);
        suma = suma + ( caracter * num );
        num = num - 1;
        if ( num == 1) {
            num = 7;
        }
    }
    console.log(suma);
    var resto = suma % 11;
    var dv = 11 - resto;
    if ( dv > 9 ) {
        if ( dv == 10) {
            dv ='K';
        }else{
            dv = 0;
        }
    }
    var dv_usuario = rut.slice(-1).toUpperCase();
    if (dv != dv_usuario) {
        //alert('rut incorrecto');
        //Swal.fire('el rut es incorrecto');
        Swal.fire({
            icon: 'error',
            title: 'validacion rut',
            text: 'el rut es incorrecto'
          });
        return false;
    }
    console.log(dv);
    return true;
}