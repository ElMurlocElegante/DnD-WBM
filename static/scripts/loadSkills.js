document.addEventListener('DOMContentLoaded', function() {
    // Obtener el elementos seleccionados
    var backgroundSelect = document.getElementById('background');
    var classSelect = document.getElementById('class');
    var raceSelect = document.getElementById('race');
    document.getElementById('allSkills').querySelectorAll('input[type="checkbox"]').forEach(function(element) {
        element.checked = false;
        element.disabled = true;
    })
    

    function fetchSkillNames() {
        return fetch('../../data/skills.json')
        .then(response => response.json())
        .then(data => {
            var skillNames = data.skill.map(skill => skill.name.toLowerCase());
            return skillNames
        })
        .catch(error => console.error('Error fetching skills:', error));
    }
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
                }).skillProficiencies[0];

                if (backgroundData) {
                    addProficiencies(backgroundData,'background');
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
                var classData = data.class[0].startingProficiencies.skills[0];
                if (classData) {
                    addProficiencies(classData,'class');
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
                    if(raceData.skillProficiencies){
                        addProficiencies(raceData.skillProficiencies[0], 'race');
                    } else {
                        var skillContainer = document.getElementById('raceSkills');
                        skillContainer.innerHTML = '';
                        skillContainer = document.getElementById('raceRemainingSkills');
                        skillContainer.innerHTML = ''
                    }

                } else {
                    console.log('Raza no encontrado:', selectedRace);
                }
            })
            .catch(error => console.error('Error fetching raza:', error));
    }

    function chooseSetSkills(data, skillContainer, type) {
        var maxSkills = data.choose.count || 1;
        var selectableSkills = data.choose.from;

        remainingSkills = maxSkills;

        document.getElementById(`${type}`).textContent = `Puedes seleccionar ${remainingSkills} skills`;
    
        // Manejar la selección de habilidades con el límite
        skillContainer.querySelectorAll('input[type="checkbox"]').forEach(function(skill) {
    
            skill.addEventListener('change', function() {
                checkedSkills = Array.from(skillContainer.querySelectorAll('input[type="checkbox"]:checked')).filter(function(skill) {
                    return !skill.disabled;
                });
                if (checkedSkills.length > maxSkills) {
                    this.checked = false;
                    checkedSkills = Array.from(skillContainer.querySelectorAll('input[type="checkbox"]:checked')).filter(function(skill) {
                        return !skill.disabled;
                    });
                    checkSkills(this);
                }
                remainingSkills = maxSkills - checkedSkills.length;
                document.getElementById(`${type}`).textContent = `Puedes seleccionar ${remainingSkills} skills`;
            });
        });
    }
    
    function chooseAnySkills(data, skillContainer, type) {
        var maxSkills = data.any
    
        remainingSkills = maxSkills;

        document.getElementById(`${type}`).textContent = `Puedes seleccionar ${remainingSkills} skills`;
    
        // Manejar la selección de habilidades con el límite
        skillContainer.querySelectorAll('input[type="checkbox"]').forEach(function(skill) {
    
            skill.addEventListener('change', function() {
                checkedSkills = Array.from(skillContainer.querySelectorAll('input[type="checkbox"]:checked')).filter(function(skill) {
                    return !skill.disabled;
                });
                if (checkedSkills.length > maxSkills) {
                    this.checked = false;
                    checkedSkills = Array.from(skillContainer.querySelectorAll('input[type="checkbox"]:checked')).filter(function(skill) {
                        return !skill.disabled;
                    });
                }
                remainingSkills = maxSkills - checkedSkills.length;
                document.getElementById(`${type}`).textContent = `Puedes seleccionar ${remainingSkills} skills`;
            });
        });
    }
    function checkSkills(event) {
        if (event.target === undefined){
            var trigger = event.value;
        } else {
            var trigger = event.target.value
        }
        var allSkills = document.getElementById('allSkills').querySelectorAll('input[type="checkbox"]')
        var backgroundSkills = Array.from(document.getElementById('backgroundSkills').querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
        var classSkills = Array.from(document.getElementById('classSkills').querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
        var raceSkills = Array.from(document.getElementById('raceSkills').querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
        var checkedSkills = Array.from(new Set([...backgroundSkills, ...classSkills, ...raceSkills]));

        allSkills.forEach(function(element) {
            if (element.value === trigger) {
                if (element.checked === false) {
                    element.checked = true;
                } else if (element.checked  === true && !checkedSkills.includes(element.value) ) {
                    element.checked = false;
                }


            }

        });


    }

    function createSkillCheckbox(skill, type) {
        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = `${skill.toLowerCase()}-${type}`;
        checkbox.id = `${skill.toLowerCase()}-${type}`;
        checkbox.value = `${skill.toLowerCase()}`;
        checkbox.addEventListener('change', checkSkills);

        var label = document.createElement('label');
        label.htmlFor = `${skill.toLowerCase()}-${type}`;
        label.textContent = `${skill}`;
    
        var container = document.createElement('div');
        container.appendChild(checkbox);
        container.appendChild(label);
    
        return container;
    }
    
    function addProficiencies(dataSkills, type) {
        switch (type) {
            case 'background':
                var id = 'backgroundSkills'
                var textRemaining = 'backgroundRemainingSkills'
                break;
            case 'class':
                var id = 'classSkills'
                var textRemaining = 'classRemainingSkills'
                break;
            case 'race':
                var id = 'raceSkills'
                var textRemaining = 'raceRemainingSkills'
                break;

        }
        var skillContainer = document.getElementById(id);
        skillContainer.innerHTML = '';
        
        Object.keys(dataSkills).forEach(function(element) {
            if (element === 'choose') {
                dataSkills.choose.from.forEach(function(skill) {
                    var skillElement = createSkillCheckbox(skill,type);
                    skillContainer.appendChild(skillElement);
                    skillElement.disabled = false; // Enable for selection
                });
                chooseSetSkills(dataSkills, skillContainer, textRemaining);
            } else if (element === 'any') {
                fetchSkillNames().then(skillNames => {
                    skillNames.forEach(function(skill) {
                        var skillElement = createSkillCheckbox(skill,type);
                        skillContainer.appendChild(skillElement);
                        skillElement.disabled = false; // Enable for selection
                    });
                    chooseAnySkills(dataSkills, skillContainer, textRemaining)

                });
            } else {
                var skillElement = createSkillCheckbox(element,type);
                skillContainer.appendChild(skillElement);
                skillElement.querySelector('input').disabled = true; // Disable specific skills
                skillElement.querySelector('input').checked = true; // Check specific skills
            }
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
