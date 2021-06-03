class usuario{
    rut;
    nombrecompleto;
    email;
    fecha;
    //mutadores
    setRut(rut){ 
        this.rut=rut; 
    }
    setNombre(nombre){ this.nombrecompleto=nombre;}
    setEmail(email){ this.email= email;}
    setFecha(fecha){ this.fecha=fecha;}
    //accesadores
    getRut(){ return this.rut;}
    getNombre(){ return this.nombrecompleto;}
    getEmail(){ return this.email;}
    getFecha(){ return this.fecha;}
}