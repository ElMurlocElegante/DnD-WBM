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
    function checkMandatorySkills(skill, skillElement, mandatorySkills) {
        console.log('Habilitando y marcando:', skill);
        skillElement.disabled = true;
        skillElement.checked = true;
        mandatorySkills.push(skillElement);
        return mandatorySkills
    }

    function chooseSetSkills(skills, checkedSkills, mandatorySkills, nonMandatoryCheckedSkills, remainingSkills, data) {
        var maxSkills = data.choose.count || 1;
        var selectableSkills = data.choose.from;
    
        console.log('Skills a Elegir:', maxSkills);
        console.log('Habilitando:', selectableSkills);
    
        selectableSkills.forEach(function(skillName) {
            var skillElement = document.getElementById(skillName);
            if (skillElement) {
                skillElement.disabled = false;
            }
        });
        remainingSkills = maxSkills;
    
        document.getElementById('remainingSkills').textContent = `Puedes seleccionar ${remainingSkills} skills`;
    
        // Manejar la selección de habilidades con el límite
        skills.forEach(function(skill) {
            // Clonar el nodo para eliminar los event listeners anteriores
            var newSkill = skill.cloneNode(true);
            skill.replaceWith(newSkill);
    
            newSkill.addEventListener('change', function() {
                checkedSkills = document.querySelectorAll('input[type="checkbox"]:checked');
                nonMandatoryCheckedSkills = Array.from(checkedSkills).filter(function(skill) {
                    return !mandatorySkills.includes(skill);
                });
                console.log('Antes', nonMandatoryCheckedSkills.length, maxSkills);
                if (nonMandatoryCheckedSkills.length > maxSkills) {
                    console.log("Maximo Alcanzado");
                    this.checked = false;
                    checkedSkills = document.querySelectorAll('input[type="checkbox"]:checked');
                    nonMandatoryCheckedSkills = Array.from(checkedSkills).filter(function(skill) {
                        return !mandatorySkills.includes(skill);
                    });
                }
                remainingSkills = maxSkills - nonMandatoryCheckedSkills.length;
                console.log('Despues', nonMandatoryCheckedSkills.length, maxSkills);
                document.getElementById('remainingSkills').textContent = `Puedes seleccionar ${remainingSkills} skills`;
            });
        });
    
        return remainingSkills;
    }
    
    function chooseAnySkills(skills, checkedSkills, mandatorySkills, nonMandatoryCheckedSkills, remainingSkills, data) {
        var maxSkills = data.any
    
        console.log('Skills a Elegir:', maxSkills);
        console.log('Habilitando: Todas las Skills');
    
        skills.forEach(function(skill) {
            if (skill) {
                skill.disabled = false;
                console.log('B')
            }
        });
        remainingSkills = maxSkills;
    
        document.getElementById('remainingSkills').textContent = `Puedes seleccionar ${remainingSkills} skills`;
    
        // Manejar la selección de habilidades con el límite
        skills.forEach(function(skill) {
            // Clonar el nodo para eliminar los event listeners anteriores
            var newSkill = skill.cloneNode(true);
            skill.replaceWith(newSkill);
    
            newSkill.addEventListener('change', function() {
                checkedSkills = document.querySelectorAll('input[type="checkbox"]:checked');
                nonMandatoryCheckedSkills = Array.from(checkedSkills).filter(function(skill) {
                    return !mandatorySkills.includes(skill);
                });
                console.log('Antes', nonMandatoryCheckedSkills.length, maxSkills);
                if (nonMandatoryCheckedSkills.length > maxSkills) {
                    console.log("Maximo Alcanzado");
                    this.checked = false;
                    checkedSkills = document.querySelectorAll('input[type="checkbox"]:checked');
                    nonMandatoryCheckedSkills = Array.from(checkedSkills).filter(function(skill) {
                        return !mandatorySkills.includes(skill);
                    });
                }
                remainingSkills = maxSkills - nonMandatoryCheckedSkills.length;
                console.log('Despues', nonMandatoryCheckedSkills.length, maxSkills);
                document.getElementById('remainingSkills').textContent = `Puedes seleccionar ${remainingSkills} skills`;
            });
        });
    
        return remainingSkills;
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
                    mandatorySkills = checkMandatorySkills(skill, skillElement, mandatorySkills)
                }

                // Habilitar las habilidades que se pueden elegir
                else if (skill === 'choose') {
                    remainingSkills = chooseSetSkills(skills, checkedBackgroundSkills, mandatorySkills, 
                                    nonMandatoryCheckedSkills, remainingSkills, backgroundData.skillProficiencies[0]);
                } else if (skill === 'any') {
                    // Todavia hay que hacer la logica si es que permite elegir cualquier skill
                    remainingSkills = chooseAnySkills(skills, checkedBackgroundSkills, mandatorySkills,
                                    nonMandatoryCheckedSkills, remainingSkills, backgroundData.skillProficiencies[0]);
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
