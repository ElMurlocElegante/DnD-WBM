function calculateLevel() {
    // Obtenemos el valor de XP del campo de entrada
    const xpInput = document.getElementById('xp');
    const xp = parseInt(xpInput.value);

    // Definimos la tabla de experiencia y PB, no recuerdo si dijiste que habia json para esto, pero por si aca
    const experienceTable = {
        "experience": [
            {"xp": 0, "level": 1},
            {"xp": 300, "level": 2},
            {"xp": 900, "level": 3},
            {"xp": 2700, "level": 4},
            {"xp": 6500, "level": 5},
            {"xp": 14000, "level": 6},
            {"xp": 23000, "level": 7},
            {"xp": 34000, "level": 8},
            {"xp": 48000, "level": 9},
            {"xp": 64000, "level": 10},
            {"xp": 85000, "level": 11},
            {"xp": 100000, "level": 12},
            {"xp": 120000, "level": 13},
            {"xp": 140000, "level": 14},
            {"xp": 165000, "level": 15},
            {"xp": 195000, "level": 16},
            {"xp": 225000, "level": 17},
            {"xp": 265000, "level": 18},
            {"xp": 305000, "level": 19},
            {"xp": 355000, "level": 20}
        ]
    };

    // Iteramos sobre la tabla de experiencia en orden inverso para encontrar el nivel correcto, manejando con la tabla de exp puesta arriba
    for (let i = experienceTable.experience.length - 1; i >= 0; i--) {
        const xpThreshold = experienceTable.experience[i].xp;
        const level = experienceTable.experience[i].level;
        if (xp >= xpThreshold) {
            // Si la experiencia es mayor o igual al umbral del nivel actual,
            // establecemos el nivel y salimos del bucle
            document.getElementById('level').textContent = `Nivel ${level}`;
            break;
        }
    }
}
