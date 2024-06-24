document.addEventListener('DOMContentLoaded', function() {
    const selectedClass = document.getElementById('class');

    const xp = document.getElementById('xp');

    function fetchClassData (event) {
        if (event.target === undefined){
            var selectedClass = event.value;
        } else  {
            var selectedClass = event.target.value
        }
        
        fetch(`https://dndapi.pythonanywhere.com/api/data/class/class-${selectedClass.toLowerCase()}.json`)
            .then(response => response.json())
            .then(data => {
                var subclassLevel = data.class[0].classFeatures.find(item => typeof item === 'object' && item.gainSubclassFeature).classFeature.match(/\d+$/)[0];
                var subclassList = data.subclass;
                if (subclassLevel && subclassList) {
                    getSubclasses(subclassLevel, subclassList);
                } else {
                    console.log('Clase no encontrada o no tiene subclase disponibles:', selectedClass);
                }
            })
            .catch(error => console.error('Error fetching class data:', error));
    }

    function getSubclasses(subclassLevel, subclassList) {
        const level = document.getElementById('level');
        const subclassSelect = document.getElementById('subclass');
        const subclassContainer = document.getElementById('subclassContainer');
        subclassSelect.innerHTML = ``;
        if (parseInt(level.value) >= subclassLevel) {
            subclassContainer.style.display = 'block';
            subclassText = document.getElementById('classContainer').querySelector('label[for="subclass"]');
            subclassText.innerHTML = `Select a Subclass`;
            subclassList.forEach(function(subclass) {
                const subclassOption = document.createElement('option');
                subclassOption.value = subclass.name;
                subclassOption.innerHTML = subclass.name;

                subclassSelect.appendChild(subclassOption);
            });
        } else {
            const noneSubclass = document.createElement('option');
            noneSubclass.value = "";
            subclassSelect.appendChild(noneSubclass);
            subclassContainer.style.display = 'none';
        }
    }

    selectedClass.addEventListener('change', fetchClassData);
    xp.addEventListener('change', function() {
        fetchClassData(selectedClass);
    });
    fetchClassData(selectedClass);
});