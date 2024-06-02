document.addEventListener('DOMContentLoaded', function() {
    // Obtener el elemento select del background
    var backgroundSelect = document.getElementById('background');

    // Ejecutar la función para aplicar las proficiencias cuando cambie la selección
    backgroundSelect.addEventListener('change', function() {
        var selectedBackground = backgroundSelect.value;
        fetch('../../data/backgrounds.json')
            .then(response => response.json())
            .then(data => {
                var backgroundData = data.background.find(function(bg) {
                    return bg.name === selectedBackground;
                });

                if (backgroundData) {
                    applyBackgroundProficiencies(backgroundData);
                } else {
                    console.log('Background no encontrado:', selectedBackground);
                }
            })
            .catch(error => console.error('Error fetching backgrounds:', error));
    });

    // Función para aplicar las proficiencias del background seleccionado
    function applyBackgroundProficiencies(backgroundData) {
        console.log('Aplicando proficiencias del background:', backgroundData);

        var mandatorySkills = [];

        // Deshabilitar todas las habilidades y desmarcarlas
        var skills = document.querySelectorAll('input[type="checkbox"]');
        skills.forEach(function(skill) {
            skill.disabled = true;
            skill.checked = false;
        });
        var checkedBackgroundSkills = 0;
        var nonMandatoryCheckedSkills = 0;
        var remainingSkills = 0;
        // Habilitar y marcar las habilidades correspondientes al nuevo fondo seleccionado
        if (backgroundData.skillProficiencies) {
            Object.keys(backgroundData.skillProficiencies[0]).forEach(function(skill) {
                var skillElement = document.getElementById(skill);

                // Habilitar y marcar las habilidades obligatorias
                if (skillElement && skill !== 'choose') {
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
                }
            });
        }
    }

    // Ejecutar la función una vez al inicio para aplicar las proficiencias del background inicial
    var initialBackground = backgroundSelect.value;
    fetch('../../data/backgrounds.json')
        .then(response => response.json())
        .then(data => {
            var initialBackgroundData = data.background.find(function(bg) {
                return bg.name === initialBackground;
            });

            if (initialBackgroundData) {
                applyBackgroundProficiencies(initialBackgroundData);
            } else {
                console.log('Background inicial no encontrado:', initialBackground);
            }
        })
        .catch(error => console.error('Error fetching backgrounds:', error));
});
