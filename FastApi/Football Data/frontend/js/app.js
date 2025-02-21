new Vue({
    el: "#app",
    data: {
        busqueda: "",
        equipo: {
            jugadores: [] // Inicializa con un array vacío
        }
    },
    methods: {
        async buscarEquipo() {
            if (!this.busqueda) return;
        
            const response = await fetch(`http://127.0.0.1:8000/buscar_equipo/${this.busqueda}`);
        
            if (response.ok) {
                const equipos = await response.json();
        
                if (equipos.length > 0) {
                    // Asignar el equipo encontrado sin borrar sus datos
                    this.equipo = { ...equipos[0] }; // No redefinir jugadores aquí
                    
                    // Obtener jugadores sin perder otros datos
                    await this.obtenerJugadores(this.equipo.id);
                } else {
                    this.equipo = { jugadores: [] };
                    alert("Equipo no encontrado");
                }
            } else {
                this.equipo = { jugadores: [] };
                alert("Error en la búsqueda");
            }
        }
        ,
        async obtenerJugadores(equipo_id) {
            const response = await fetch(`http://127.0.0.1:8000/equipo/${equipo_id}`);
        
            if (response.ok) {
                const data = await response.json();
        
                // Fusionar datos sin perder `fundacion` ni `sitio_web`
                this.equipo = { ...this.equipo, jugadores: data.jugadores || [] };
            } else {
                this.equipo = { ...this.equipo, jugadores: [] };
                alert("No se pudieron obtener los jugadores");
            }
        }        
        
    }
});
