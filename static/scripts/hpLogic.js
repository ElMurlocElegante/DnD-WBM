document.addEventListener('DOMContentLoaded', function(){
    
    function getHitDie(event, func) {
        if (event.target){
            var selectedClass = event.target.value;
        } else  {
            var selectedClass = event.value
        }
        fetch(`../../data/class/class-${selectedClass.toLowerCase()}.json`)
            .then(response => response.json())
            .then(data => {
                const classData = data.class[0].hd.faces;
                if (classData) {
                    func(classData);
                } else {
                    console.log('Clase no encontrada o no tiene hit-die definido:', selectedClass);
                }
            })
            .catch(error => console.error('Error fetching class data:', error));
    }

    function rollHP(die) {
        const hp = document.getElementById('hp');
        const level = document.getElementById('xp');
        const conMod = document.querySelector('input[name="modConstitution"]');

        hp.value = die + parseInt(conMod.value);
        if (level.value - 1 > 0){
            fetch(`roll_dice/${level.value - 1}d${die}`)
                .then(response => response.json())
                .then(data => {
                        const result = data.total;
                        hp.value =  die + parseInt(conMod.value) + result + parseInt(conMod.value) * (level.value - 1)
                })
        }


    }
    function avgHP(die) {
        const hp = document.getElementById('hp');
        const level = document.getElementById('xp');
        const conMod = document.querySelector('input[name="modConstitution"]');

        console.log(die + parseInt(conMod.value))
        var avg = 0;
        for(var i=1; i<=die; i++){
            avg += i;
        }
        avg = Math.round(avg / die);

        hp.value = (die + parseInt(conMod.value)) + ((avg + parseInt(conMod.value))* (level.value-1))

    }

    function maxHP(die) {
        const hp = document.getElementById('hp');
        const level = document.getElementById('xp')
        const conMod = document.querySelector('input[name="modConstitution"]');
        hp.value = (die + parseInt(conMod.value)) * level.value
    }

    const selectedClass = document.getElementById('class');
    const hpRoll = document.getElementById('hpRoll');
    const hpAvg = document.getElementById('hpAvg');
    const hpMax = document.getElementById('hpMax');

    hpRoll.addEventListener('click', function() {
        getHitDie(selectedClass, rollHP);
    });
    hpAvg.addEventListener('click', function() {
        getHitDie(selectedClass, avgHP)
    });
    hpMax.addEventListener('click', function() {
        getHitDie(selectedClass, maxHP)
    });

});