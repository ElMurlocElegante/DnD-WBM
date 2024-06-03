document.addEventListener('DOMContentLoaded', function() {
    // Obtener el elementos seleccionados
    var backgroundSelect = document.getElementById('background');
    var classSelect = document.getElementById('class');
    var raceSelect = document.getElementById('race');

    // Fetching y aplicacion de proficiencias
    function fetchBackgroundData (event) {
        
        if (event.target === undefined){
            var selectedBackground = event.value;
        } else  {
            var selectedBackground = event.target.value
        }
        fetch('../../data/backgrounds.json')
            .then(response => response.json())
            .then(data => {
                var backgroundData = data.background.find(function(bg) {
                    return bg.name === selectedBackground;
                });

                if (backgroundData) {
                    applyBackgroundProficiencies(['classSkills'], ['raceSkills'], backgroundData);   // Hay que hacer la logica para enviar la lista de skills seleccionadas para cada caso
                } else {
                    console.log('Background no encontrado:', selectedBackground);
                }
            })
            .catch(error => console.error('Error fetching backgrounds:', error));
    }

    function fetchClassData (event) {
        if (event.target === undefined){
            var selectedClass = event.value;
        } else  {
            var selectedClass = event.target.value
        }
        
        fetch(`../../data/class/class-${selectedClass.toLowerCase()}.json`)
            .then(response => response.json())
            .then(data => {
                var classData = data;
                if (classData) {
                    applyClassProficiencies(['backgroundSkills'], ['raceSkills'], classData); // Hay que hacer la logica para enviar la lista de skills seleccionadas para cada caso
                } else {
                    console.log('Clase no encontrada o no tiene habilidades definidas:', selectedClass);
                }
            })
            .catch(error => console.error('Error fetching class data:', error));
    }

    function fetchRaceData (event) {
        if (event.target === undefined){
            var selectedRace = event.value;
        } else {
            var selectedRace = event.target.value;
        }
        var [raceName, raceSource] = selectedRace.split('-');

        fetch('../../data/races.json')
            .then(response => response.json())
            .then(data => {
                var raceData = data.race.find(function(rc) {
                    return rc.name === raceName && rc.source === raceSource;
                });

                if (raceData) {
                    applyRaceProficiencies(['backgroundSkills'], ['classSkills'], raceData); // Hay que hacer la logica para enviar la lista de skills seleccionadas para cada caso
                } else {
                    console.log('Raza no encontrado:', selectedRace);
                }
            })
            .catch(error => console.error('Error fetching backgrounds:', error));
    }

    // Función para aplicar las proficiencias del background seleccionado
    function applyBackgroundProficiencies(classSkills, raceSkills, backgroundData) {

        var mandatorySkills = [];
        var checkedBackgroundSkills = [];
        var nonMandatoryCheckedSkills = [];
        var remainingSkills = 0;

        console.log('Aplicando proficiencias del background:', backgroundData);

        // Deshabilitar todas las habilidades y desmarcarlas
        var skills = document.querySelectorAll('input[type="checkbox"]');
        skills.forEach(function(skill) {
            skill.disabled = true;
            skill.checked = false;
        });

        // Habilitar y marcar las habilidades correspondientes al nuevo fondo seleccionado
        if (backgroundData.skillProficiencies) {
            Object.keys(backgroundData.skillProficiencies[0]).forEach(function(skill) {
                var skillElement = document.getElementById(skill);

                // Habilitar y marcar las habilidades obligatorias
                if (skillElement && skill !== 'choose' && skill !== 'any') {
                    console.log('Habilitando y marcando:', skill);
                    skillElement.disabled = true;
                    skillElement.checked = true;
                    mandatorySkills.push(skillElement);
                }

                // Habilitar las habilidades que se pueden elegir
                else if (skill === 'choose') {
                    var maxBackgroundSkills = backgroundData.skillProficiencies[0].choose.count || 1;
                    var selectableSkills = backgroundData.skillProficiencies[0].choose.from;

                    console.log('Skills a Elegir:', maxBackgroundSkills);
                    console.log('Habilitando:', selectableSkills);

                    selectableSkills.forEach(function(skillName) {
                        var skillElement = document.getElementById(skillName);
                        if (skillElement) {
                            skillElement.disabled = false;
                        }
                    });
                    remainingSkills = maxBackgroundSkills

                    document.getElementById('remainingSkills').textContent = `Puedes seleccionar ${remainingSkills} skills`;

                    // Manejar la selección de habilidades con el límite
                    skills.forEach(function(skill) {
                        skill.addEventListener('change', function() {
                            checkedBackgroundSkills = document.querySelectorAll('input[type="checkbox"]:checked');
                            nonMandatoryCheckedSkills = Array.from(checkedBackgroundSkills).filter(function(skill) {
                                return !mandatorySkills.includes(skill);
                            });
                            if (nonMandatoryCheckedSkills.length > maxBackgroundSkills) {
                                console.log("Maximo Alcanzado")
                                this.checked = false;
                                checkedBackgroundSkills = document.querySelectorAll('input[type="checkbox"]:checked');
                                nonMandatoryCheckedSkills = Array.from(checkedBackgroundSkills).filter(function(skill) {
                                    return !mandatorySkills.includes(skill);
                                });
                            }
                            remainingSkills = maxBackgroundSkills - nonMandatoryCheckedSkills.length;
                            document.getElementById('remainingSkills').textContent = `Puedes seleccionar ${remainingSkills} skills`;
                        });
                    });
                } else if (skill === 'any') {
                    // Todavia hay que hacer la logica si es que permite elegir cualquier skill
                }
            });
        }

    }

    
    function applyClassProficiencies(backgroundSkills, racesSkills, classData) {
        var classSkills = [];
        var checkedClassSkills = [];
        var remainingSkills = 0;
    
        console.log('Aplicando proficiencias de la clase:', classData);
    
        var skills = document.querySelectorAll('input[type="checkbox"]');
        skills = Array.from(skills).filter(function(skill) {
            return !backgroundSkills.includes(skill) && !racesSkills.includes(skill);
        });
    

    }
    
    function applyRaceProficiencies(backgroundSkills, classSkills, raceData) {
        var raceSkills = [];
        var checkedRaceSkills = [];
        var remainingSkills = 0;

        console.log('Aplicando proficiencias de la raza:', raceData);
    
        var skills = document.querySelectorAll('input[type="checkbox"]');
        skills = Array.from(skills).filter(function(skill) {
            return !backgroundSkills.includes(skill) && !classSkills.includes(skill);
        });
    }

    // Ejecutar la función para aplicar las proficiencias cuando cambie la selección
    backgroundSelect.addEventListener('change', fetchBackgroundData);
    classSelect.addEventListener('change', fetchClassData);
    raceSelect.addEventListener('change', fetchRaceData);

    // Ejecutar la función para aplicar las proficiencias cuando se carga la pagina
    fetchBackgroundData(backgroundSelect);
    fetchClassData(classSelect);
    fetchRaceData(raceSelect);


});
