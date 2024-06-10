document.addEventListener('DOMContentLoaded',function(){
    document.getElementById('xp').addEventListener('change', function(){
        // Obtenemos el valor de XP del campo de entrada
        const xpInput = document.getElementById('xp');
        const xp = parseInt(xpInput.value);

        // Definimos la tabla de experiencia y PB, no recuerdo si dijiste que habia json para esto, pero por si aca
        const experienceTable = {
            "experience": [
                {"xp": 0, "level": 1, "pb":2},
                {"xp": 300, "level": 2, "pb":2},
                {"xp": 900, "level": 3, "pb":2},
                {"xp": 2700, "level": 4, "pb":2},
                {"xp": 6500, "level": 5, "pb":3},
                {"xp": 14000, "level": 6, "pb":3},
                {"xp": 23000, "level": 7, "pb":3},
                {"xp": 34000, "level": 8, "pb":3},
                {"xp": 48000, "level": 9, "pb":4},
                {"xp": 64000, "level": 10, "pb":4},
                {"xp": 85000, "level": 11, "pb":4},
                {"xp": 100000, "level": 12, "pb":4},
                {"xp": 120000, "level": 13, "pb":5},
                {"xp": 140000, "level": 14, "pb":5},
                {"xp": 165000, "level": 15, "pb":5},
                {"xp": 195000, "level": 16, "pb":5},
                {"xp": 225000, "level": 17, "pb":6},
                {"xp": 265000, "level": 18, "pb":6},
                {"xp": 305000, "level": 19, "pb":6},
                {"xp": 355000, "level": 20, "pb":6}
            ]
        };

        // Iteramos sobre la tabla de experiencia en orden inverso para encontrar el nivel correcto, manejando con la tabla de exp puesta arriba
        for (let i = experienceTable.experience.length - 1; i >= 0; i--) {
            const xpThreshold = experienceTable.experience[i].xp;
            if (xp >= xpThreshold) {
                const level = experienceTable.experience[i].level;
                const pb = experienceTable.experience[i].pb;
                // Si la experiencia es mayor o igual al umbral del nivel actual,
                // establecemos el nivel y salimos del bucle
                document.getElementById('level').textContent = `Nivel: ${level} PB: ${pb}`;
                break;
            }
        }
    });
});