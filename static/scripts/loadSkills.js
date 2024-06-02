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
        
        // Deshabilitar todas las habilidades y desmarcarlas
        var skills = document.querySelectorAll('input[type="checkbox"]');
        skills.forEach(function(skill) {
            skill.disabled = true;
            skill.checked = false;
        });

        // Habilitar y marcar las habilidades correspondientes al nuevo fondo seleccionado
        if (backgroundData.skillProficiencies) {
            if (Object.keys(backgroundData.skillProficiencies[0])[0] !== 'choose'){
                Object.keys(backgroundData.skillProficiencies[0]).forEach(function(skill) {
                    console.log('Habilitando y marcando:', skill);
                    var skillElement = document.getElementById(skill);
                    if (skillElement) {
                        skillElement.disabled = true;
                        skillElement.checked = true;
                    }
                });
                // En caso de que haya que elegir skills:
            } else {
                var maxBackgroundSkills = backgroundData.skillProficiencies[0].choose.count
                console.log('Skills a Elegir:', maxBackgroundSkills)
                console.log('Habilitando:', backgroundData.skillProficiencies[0].choose.from)
                backgroundData.skillProficiencies[0].choose.from.forEach(function(skill) {
                    var skillElement = document.getElementById(skill);
                    if (skillElement) {
                        skillElement.disabled = false;
                    }
                })
                skills.forEach(function(skill) {
                    skill.addEventListener('change', function() {
                        var checkedBackgroundSkills = document.getElementById('characterForm').querySelectorAll('input[type="checkbox"]:checked');
                        if (checkedBackgroundSkills.length > maxBackgroundSkills) {
                            this.checked = false;
                            checkedBackgroundSkills = document.getElementById('characterForm').querySelectorAll('input[type="checkbox"]:checked');
                        }
                        document.getElementById('remainingSkills').textContent = `Puedes seleccionar ${maxBackgroundSkills - checkedBackgroundSkills.length } skills`

                    })
                })
            }
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
